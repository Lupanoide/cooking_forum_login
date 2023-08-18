from pydantic import BaseModel, EmailStr, Field

class UserLogin(BaseModel):
    username: EmailStr = Field(description="user email")
    password: str = Field(min_length=6, max_length=24, description="user password")

class User(BaseModel):
    username: EmailStr = Field(description="user email")
    password: str = Field(min_length=6, max_length=24, description="user password")
    name: str
    surname: str
    two_factors_login_enabled: bool = False

class OtpUser(BaseModel):
    username: EmailStr = Field(description="user email")

class OtpToken(BaseModel):
    username: EmailStr = Field(description="user email")
    otp: str


