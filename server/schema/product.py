from pydantic import BaseModel


class Product(BaseModel):
    product_name: str
    default_price: float
    currency: str
    description: str
    images: str
    unit_label: str
