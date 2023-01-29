from datetime import datetime

from config.db import session
from fastapi import APIRouter
from models.index import Orders
from schema.index import Order

order_router = APIRouter()


@order_router.get("/all_order")
async def read_all_order():
    return session.query(Orders).all()


@order_router.get("/fetch_order")
async def read_order(id: int):
    try:
        res = session.query(Orders).filter(Orders.id == id).first().__dict__
    except Exception:
        res = []
    return res


@order_router.post("/add_order")
async def write_order(orders: Order):
    to_be_inserted = Orders(
        user_id=orders.user_id,
        status=orders.status,
        posted_at=datetime.now().timestamp(),
        transacted_at=datetime.now().timestamp(),
        updated_at=datetime.now().timestamp(),
    )
    session.add(to_be_inserted)
    session.commit()
    return session.query(Orders).all()


@order_router.put("/update_order")
async def update_order(id: int, user_id: int = None, status: str = None):
    to_be_updated = session.query(Orders).filter(Orders.id == id).first()
    if user_id:
        to_be_updated.user_id = user_id
        to_be_updated.updated_at = datetime.now().timestamp()
    if status:
        to_be_updated.status = status
        to_be_updated.updated_at = datetime.now().timestamp()

    session.commit()
    return session.query(Orders).all()


@order_router.get("/delete_order")
async def delete_order(id: int):
    try:
        session.query(Orders).filter(Orders.id == id).delete(
            synchronize_session="evaluate"
        )
        session.commit()
    except Exception:
        print("Not Found")
    return session.query(Orders).all()
