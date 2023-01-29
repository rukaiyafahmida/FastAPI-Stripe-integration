from config.db import session
from fastapi import APIRouter
from models.index import Orders, OrderDetails, Products, Users

from sqlalchemy.sql import label

details_router = APIRouter()


def check_class(table: str):
    if table == "Orders":
        return Orders
    if table == "Users":
        return Users
    if table == "Products":
        return Products
    if table == "OrderDetails":
        return OrderDetails


@details_router.get("/all_details")
async def get_order_all_details(id: int, table: str = None):
    opt = check_class(table)
    result = (
        session.query(
            OrderDetails.quantity,
            label("total", (Products.default_price * OrderDetails.quantity)),
            Products.product_name,
            Products.description,
            Products.images,
            Products.unit_label,
            Products.default_price,
            Orders.status,
            Orders.posted_at,
            Users.first_name,
            Users.last_name,
            Users.user_email,
        )
        .join(OrderDetails.product)
        .join(OrderDetails.orders)
        .join(Orders.users)
        .filter(opt.id == id)
    )

    ordered_list = list(result)
    return ordered_list
