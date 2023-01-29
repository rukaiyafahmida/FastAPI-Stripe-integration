from datetime import datetime

from config.db import session
from fastapi import APIRouter
from models.index import Products
from schema.index import Product

product_router = APIRouter()


@product_router.get("/all_product")
async def read_all_product():
    return session.query(Products).all()


@product_router.get("/fetch_product")
async def read_product(id: int):
    try:
        res = session.query(Products).filter(Products.id == id).first().__dict__
    except Exception:
        res = []
    return res


@product_router.post("/add_product")
async def write_product(products: Product):
    to_be_inserted = Products(
        name=products.product_name,
        description=products.description,
        unit_label=products.unit_label,
        images=products.images,
        default_price=products.default_price,
        currency=products.currency,
        created=datetime.now().timestamp(),
        updated=datetime.now().timestamp(),
    )
    session.add(to_be_inserted)
    session.commit()
    return session.query(Products).all()


@product_router.put("/update_product")
async def update_product(
    id: int,
    name: str = None,
    description: str = None,
    unit_label: str = None,
    images: str = None,
    default_price: float = None,
    currency: str = None,
):
    to_be_updated = session.query(Products).filter(Products.id == id).first()
    if name:
        to_be_updated.product_name = name
        to_be_updated.updated = datetime.now().timestamp()
    if description:
        to_be_updated.description = description
        to_be_updated.updated = datetime.now().timestamp()
    if unit_label:
        to_be_updated.unit_label = unit_label
        to_be_updated.updated = datetime.now().timestamp()
    if images:
        to_be_updated.images = images
    if default_price:
        to_be_updated.default_price = default_price
        to_be_updated.updated = datetime.now().timestamp()
    if currency:
        to_be_updated.currency = currency
        to_be_updated.updated = datetime.now().timestamp()

    session.commit()
    return session.query(Products).all()


@product_router.get("/delete_product")
async def delete_product(id: int):
    try:
        session.query(Products).filter(Products.id == id).delete(
            synchronize_session="evaluate"
        )
        session.commit()
    except Exception:
        print("Not Found")
    return session.query(Products).all()
