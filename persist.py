from app.models import Student, Comment
from app.database import get_db
from sqlalchemy.orm import Session
from app.database import engine

# from fastapi import APIRouter

session = Session(bind=engine)

# router = APIRouter(tags=["Deneme"])

# @router.post("/persist")
# def create_newthings(studet: Student):

student1 = Student(
    name="Yusuf",
    email="yusuf@gmail.com",
    comments=[Comment(text="Hello"), Comment(text="naber")],
)

yasin = Student(
    name="Yusuf",
    email="yasin@gmail.com",
    comments=[Comment(text="I am Yasin"), Comment(text="It is for tryouts")],
)

mehmet = Student(
    name="Mehmet",
    email="mehmet@gmail.com",
)


session.add_all([student1, yasin, mehmet])
session.commit()
