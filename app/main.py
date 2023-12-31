import time
from fastapi import Body, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from random import randrange
import psycopg2 as pg
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    #rating: int | None = None

while True: 
    try:
        conn = pg.connect(host='localhost',database='fastapi',
                        user='postgres',password='ysf12345',
                        cursor_factory=RealDictCursor)
        curr = conn.cursor()
        print("Database connection successfull.")
        break
    except Exception as error:
        print("Connecting to database failed.")
        print("Error:",error)
        time.sleep(2)


my_posts = [{"id":1,"title":"california dream","content":"hell yeah"},
            {"id":2,"title":"los angelos","content":"lets think about it"}]

def find_post(id:int):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_post_index(id:int):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/")
def root():
    return {"message":"Hello World"}

@app.get("/posts")
def get_posts():
    
    curr.execute("""SELECT * FROM posts""")
    posts = curr.fetchall()
    return {"data":posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
    
    curr.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *"""
                 ,(post.title, post.content, post.published))
    new_post = curr.fetchone()
    conn.commit()
    return {"data":new_post}

@app.get("/posts/{id}")
def get_post(id:int):
    
    curr.execute("""SELECT * FROM posts WHERE id=%s""",str(id))
    post = curr.fetchone()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not exist.")
    return {"post details": post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete(id):
    
    curr.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",str(id))
    post = curr.fetchone()
    conn.commit()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not exist.")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    
    curr.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    (post.title, post.content, post.published, str(id)))
    updated_post = curr.fetchone()
    conn.commit()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not exist.")
    
    return {"data": updated_post}    




