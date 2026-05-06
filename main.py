from fastapi import FastAPI
from pydantic import BaseModel

from tables import create_tables
from verify import create_user, get_user_data, verify_user

app = FastAPI()
create_tables()


class RegisterUser(BaseModel):
    username: str
    enrollment_number: str
    password: str


class LoginUser(BaseModel):
    username: str
    password: str


@app.get("/")
def home():
    return {"message": "Trial auth API is running"}


@app.post("/register")
def register(user: RegisterUser):
    db_user = create_user(user.username, user.enrollment_number, user.password)

    if not db_user:
        return {"status": "error", "message": "User already exists"}

    return {
        "status": "success",
        "message": "User created successfully",
        "user": get_user_data(user.username),
    }


@app.post("/login")
def login(user: LoginUser):
    db_user = verify_user(user.username, user.password)

    if not db_user:
        return {
            "status": "error",
            "message": "please use the real credentials that you used on the college portal",
        }

    return {
        "status": "success",
        "message": "Login successful",
        "user": get_user_data(user.username),
    }
