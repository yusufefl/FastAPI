from datetime import datetime
from pydantic import BaseModel, EmailStr

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    #rating: int | None = None
        
class PostResponse(Post):
    id: int
    created_at: datetime
    owner_id: int
    
    class Config:
        from_attributes = True
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str 

class TokenData(BaseModel):
    id: int | None = None
    
