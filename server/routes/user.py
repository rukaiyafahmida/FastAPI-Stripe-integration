from datetime import datetime

from config.db import session
from fastapi import APIRouter
from models.index import Users
from schema.index import User


user_router = APIRouter()


@user_router.get("/all_user")
async def read_all_user():
    return session.query(Users).all()


@user_router.get("/fetch_user")
async def read_user(id: int):
    try:
        res = session.query(Users).filter(Users.id == id).first().__dict__
    except Exception:
        res = []
    return res


@user_router.post("/add_user")
async def write_user(user: User):
    to_be_inserted = Users(
        first_name=user.first_name,
        last_name=user.last_name,
        user_email=user.user_email,
        created_at=datetime.now().timestamp(),
        last_updated_at=datetime.now().timestamp(),
    )
    session.add(to_be_inserted)
    session.commit()
    return session.query(Users).all()


@user_router.put("/update_user")
async def update_user(
    id: int, first_name: str = None, last_name: str = None, user_email: str = None
):

    to_be_updated = session.query(Users).filter(Users.id == id).first()

    if first_name:
        to_be_updated.first_name = first_name
        to_be_updated.last_updated_at = datetime.now().timestamp()

    if last_name:
        to_be_updated.last_name = last_name
        to_be_updated.last_updated_at = datetime.now().timestamp()

    if user_email:
        to_be_updated.user_email = user_email
        to_be_updated.last_updated_at = datetime.now().timestamp()

    session.commit()
    return session.query(Users).all()


@user_router.get("/delete_user")
async def delete_user(id: int):
    try:
        session.query(Users).filter(Users.id == id).delete(
            synchronize_session="evaluate"
        )
        session.commit()
    except Exception:
        print("Not Found")
    return session.query(Users).all()
