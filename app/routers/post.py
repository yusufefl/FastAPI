from typing import List
from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, models

router = APIRouter()

@router.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    
    posts = db.query(models.Post).all()
    return posts

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post:schemas.Post, db: Session = Depends(get_db)):

    new_post = models.Post(**post.model_dump())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

@router.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id:int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not exist.")
    return post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)
    
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not exist.")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/posts/{id}", response_model= schemas.PostResponse)
def update_post(id:int, post:schemas.Post, db: Session = Depends(get_db)):
 
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not exist.")

    post_query.update(post.model_dump(),synchronize_session=False)
    db.commit()
    
    return post_query.first()