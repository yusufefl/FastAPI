from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int | None = None 

@app.get("/")
def root():
    return {"message":"Hello World"}

@app.get("/posts")
def get_posts():
    return {"message":"Here is all posts"}

@app.post("/posts")
def create_post(new_post:Post):
    print(new_post)
    print(new_post.model_dump())
    return {"new post":f"title is {new_post.title}, content is {new_post.content}"}

