from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi_utils.tasks import repeat_every
from src.models.model import User, UserLogin, OtpUser, OtpToken
from src.utils.utils import get_hashed_password, verify_password, create_access_token
from src.conf.config import Config
from src.app.db import check_user, create_new_user, insert_new_otp_for_user, retrieve_otp, load_sqlfile, remove_expired_tokens
from src.app.otp import get_random_char, send_email
from fastapi_asyncpg import configure_asyncpg
from datetime import timedelta

conf = Config()
pg_url = conf.get_db_url()

app = FastAPI()
database = configure_asyncpg(app, pg_url)


@database.on_init
async def initialization(conn):
    await load_sqlfile(conn, conf.get_table_user_declaration())
    await load_sqlfile(conn, conf.get_table_otp_declaration())

@app.on_event("startup")
@repeat_every(seconds=60 * 5, wait_first=True)
async def remove_expired_tokens_task() -> None:
    await remove_expired_tokens(database=Depends(database.connection))


@app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')

@app.post('/signup', summary="Create new user", status_code=status.HTTP_201_CREATED)
async def create_user(data: User, database=Depends(database.connection)):
    user = await check_user(database=database, username = data.username)
    if user:
        raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Account for user {data.username} already exist",
        headers={"WWW-Authenticate": "Bearer"}
        )
    user = {
        'username': data.username,
        'password': get_hashed_password(data.password),
        'name': data.name,
        'surname': data.surname,
        'two_factors_login_enabled': data.two_factors_login_enabled
    }
    await create_new_user(database=database, user=user)

    return user


@app.post('/login', summary="Login for users")
async def login(data: UserLogin, database=Depends(database.connection)):
    user = await check_user(database=database, username = data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {data.username} not found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    login  = dict(user)

    if not verify_password(data.password, login['password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Incorrect password for user {login['username']}",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token = create_access_token( 
              data={"sub": login['username']}, expires_delta=timedelta(minutes=int(conf.get_jwt_access_token_expires_minutes() ) ) 
    )

    return {"access_token": access_token, "token_type": "bearer"}

@app.post('/generate_otp', summary="Generate one time password for users")
async def generate_otp(data: OtpUser, database=Depends(database.connection)):
    user = await check_user(database=database, username = data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {data.username} not found",
            headers={"WWW-Authenticate": "Bearer"}
        )

    login  = dict(user)

    if not login['two_factors_login_enabled']:
                raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Two factors login not enabled for user {login['username']}",
            headers={"WWW-Authenticate": "Bearer"}
        )

    length = int(conf.get_otp_length())
    otp = ""
    for i in range(length):
        char = get_random_char()
        otp += char

    hashed_otp = get_hashed_password(otp)
    await insert_new_otp_for_user(database, login['username'], hashed_otp)
    send_email(otp)

    return f"Email sent to user {login['username']}"

@app.post('/validate_otp', summary="Validate one time password for users")
async def validate_otp(data: OtpToken, database=Depends(database.connection)):
    token = await retrieve_otp(database, data.username)
    if not token:
            raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Your one time password has been expired and is not anymore active. Please generate another one",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token_result = dict(token)
    hashed_token = token_result['token']

    if not verify_password(data.otp, hashed_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect one time password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return f"One time password validated for user {data.username}"
