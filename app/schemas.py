
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
    
    class Config:
        from_attributes = True
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime