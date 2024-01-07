from datetime import datetime
from pydantic import BaseModel, EmailStr, validator


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: int | None = None


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class PostResponse(Post):
    id: int
    created_at: datetime
    owner: UserResponse


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None


class VoteCreate(BaseModel):
    post_id: int
    like: int

    @validator("like")
    def zero_or_one(cls, value):
        if value not in (0, 1):
            raise ValueError("Must be either 1 or 0")
        return value


# class PostVoteResponse(Post):
#     Post: Post
#     votes: int

#     class config:
#         orm_mode = True
