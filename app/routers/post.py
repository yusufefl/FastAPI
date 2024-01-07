from typing import List
from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, models, oauth2
from sqlalchemy.sql.expression import func, select


router = APIRouter(prefix="/posts", tags=["Posts"])


# @router.get("/", response_model=List[schemas.PostVoteResponse])
@router.get("/")
def get_posts(
    limit: int | None = None,
    skip: int | None = None,
    search: str | None = "",
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    posts = (
        db.query(models.Post)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    # subq = select(models.Vote.post_id).distinct().where(models.Vote.user_id == current_user.id)

    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(
            models.Vote,
            and_(
                models.Vote.post_id == models.Post.id,
                models.Vote.user_id == models.Post.owner_id,
            ),
            isouter=True,
        )
        .group_by(models.Post.id, models.Vote.post_id, models.Vote.user_id)
        .all()
    )

    # stmt = (
    #     select(models.Post.id, func.count(models.Vote.post_id).label("votes"))
    #     .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
    #     .group_by(models.Post.id)
    # )

    # print(stmt)
    # results = db.execute(statement=stmt)

    # rows = results.fetchall()

    # for row in rows:
    #     print(row)

    # results = (
    #     db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
    #     .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
    #     .group_by(models.Post.id)
    #     .all()
    # )

    return results


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def create_post(
    post: schemas.Post,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):  # user needs to provide an access token
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    print(current_user)
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not exist.",
        )
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    print(current_user)
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not exist.",
        )

    if post.first().owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not  authorized to delete post with id {id}. ",
        )

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(
    id: int,
    post: schemas.Post,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    print(current_user)
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not exist.",
        )

    if post_query.first().owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not  authorized to update post with id {id}. ",
        )

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()
