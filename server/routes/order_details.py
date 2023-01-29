from datetime import datetime

from config.db import session
from fastapi import APIRouter
from models.index import OrderDetails, Orders
from schema.index import Order_detail

order_details_router = APIRouter()


@order_details_router.get("/all_order_details")
async def read_all_order_details():
    return session.query(OrderDetails).all()


@order_details_router.get("/fetch_order_details")
async def read_order_details(id: int):

    try:
        res = list(
            session.query(OrderDetails).filter(OrderDetails.id == id)
        )  # .first().__dict__
        print(res[0].product)
        print(type(res[0].product))
    except Exception as e:
        print(f"oops {e}")
        res = []
    return res


@order_details_router.post("/add_order_details")
async def write_order_details(order_detail: Order_detail):
    # price_per_unit = session.query(Products)
    # .filter(Products.id==order_detail.product_id).first().__dict__["default_price"]
    # t_price = price_per_unit * order_detail.quantity
    to_be_inserted = OrderDetails(
        order_id=order_detail.order_id,
        product_id=order_detail.product_id,
        quantity=order_detail.quantity,
        # total_price = t_price,
        placed_at=datetime.now().timestamp(),
    )
    session.add(to_be_inserted)
    session.commit()
    return session.query(OrderDetails).all()


@order_details_router.put("/update_order_details")
async def update_order_details(
    id: int,
    order_id: int = None,
    product_id: int = None,
    quantity: int = None,
):

    to_be_updated = session.query(OrderDetails).filter(OrderDetails.id == id).first()
    if order_id:
        to_be_updated.order_id = order_id
        to_be_updated.updated_at = datetime.now().timestamp()
    if product_id:
        to_be_updated.product_id = product_id
        to_be_updated.updated_at = datetime.now().timestamp()
    if quantity:
        to_be_updated.quantity = quantity
        to_be_updated.updated_at = datetime.now().timestamp()

    respective_order = session.query(Orders).filter(Orders.id == id).first()
    respective_order.updated_at = datetime.now().timestamp()

    session.commit()
    return session.query(OrderDetails).all()


@order_details_router.get("/delete_order_details")
async def delete_order_details(id: int):
    try:
        session.query(OrderDetails).filter(OrderDetails.id == id).delete(
            synchronize_session="evaluate"
        )
        session.commit()
    except Exception:
        print("Not Found")
    return session.query(OrderDetails).all()
