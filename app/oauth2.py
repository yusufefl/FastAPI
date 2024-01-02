from jose import JWTError, jwt
from datetime import datetime, timedelta
from app import schemas, database, models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oath2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token:str, credential_exeption):
    
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
        id = payload.get("user_id")
        
        if id is None:
            raise credential_exeption
        
        token_data = schemas.TokenData(id=id)
        
    except JWTError:
        raise credential_exeption
    
    return token_data
    
def get_current_user(token:str = Depends(oath2_scheme), 
                     db: Session = Depends(database.get_db)) -> models.User:

    credentials_exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                         detail=f"Could not validate credentials.",
                                         headers={"WWW-Authenticate":"Bearer"})
    
    tokendata = verify_access_token(token=token, credential_exeption= credentials_exeption)
    
    user = db.query(models.User).filter(models.User.id == tokendata.id).first()
    
    return user

 
    