from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #for password encryption

def hash(passowrd: str):
    return pwd_context.hash(passowrd)