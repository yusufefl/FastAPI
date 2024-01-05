from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, models, oauth2

router = APIRouter(prefix="/vote", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    votedata: schemas.VoteCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == votedata.post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {votedata.post_id} does not exist.",
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == votedata.post_id,
        models.Vote.user_id == current_user.id,
    )
    found_vote = vote_query.first()

    if votedata.like == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {current_user.id} already voted on post {votedata.post_id}",
            )
        new_vote = models.Vote(post_id=votedata.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message": "Successfully added vote."}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist."
            )
        vote_query.delete(synchronize_session=False),
        db.commit()
        return {"message": "Vote successfully deleted."}
