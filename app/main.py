from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from app.api.db import metadata, database, engine
from datetime import datetime, timedelta, timezone
from app.api.models import User
from app.utils.password import verify_pwd, secure_pwd
import jwt

# TODO: relocate
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

@app.get('/')
async def index():
    return {"Real": "A"}

def get_user(username: str):
    if username in database:
        user_dict = database[username]
        return User(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_pwd(password, user.hashed_password):
        return False
    return user

def create_access_token(uuid, expiresAt):
    to_encode = {"uuid": uuid}
    to_encode.update({"exp": expiresAt})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user
