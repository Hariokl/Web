from passlib.context import CryptContext
from fastapi_jwt_auth import AuthJWT
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def secure_pwd(raw_password):
    return pwd_context.hash(raw_password)

def verify_pwd(plain, hash):
    return pwd_context.verify(plain, hash)
