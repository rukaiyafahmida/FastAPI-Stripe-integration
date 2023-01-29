from pydantic import BaseModel


class Order_detail(BaseModel):
    order_id: int
    product_id: int
    quantity: int
