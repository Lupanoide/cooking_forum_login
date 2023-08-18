

async def check_user(database, username: str):
    user = await database.fetchrow(f"SELECT username, password, two_factors_login_enabled FROM users WHERE username = '{username}'")
    return user

async def create_new_user(database, user: dict):
    result = await database.execute(f"INSERT INTO users (username, password, name, surname, two_factors_login_enabled) VALUES ('{user['username']}', '{user['password']}', '{user['name']}', '{user['surname']}', '{user['two_factors_login_enabled']}' )")
    return result

async def insert_new_otp_for_user(database, username: str, otp: str):
    result = await database.execute(f"INSERT INTO otp (username, token) VALUES ('{username}', '{otp}' )")
    return result

async def retrieve_otp(database, username: str):
    otp = await database.fetchrow(f"SELECT token FROM otp WHERE username = '{username}'")
    return otp

async def load_sqlfile(db, file: str):
    with open(file,"r") as f:
        data = f.read()
        await db.execute(data)

async def remove_expired_tokens(db):
    await database.execute("DELETE from otp  WHERE timestamp < NOW() - interval '5' minute;")
