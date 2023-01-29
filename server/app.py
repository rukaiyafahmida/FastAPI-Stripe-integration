from fastapi import FastAPI
from routes.index import (
    user_router,
    product_router,
    order_router,
    order_details_router,
    details_router,
)
from config.utils import create_db_tables

app = FastAPI(title="Fashion")

create_db_tables()


app.include_router(user_router, tags=["User Methods"])
app.include_router(product_router, tags=["Product Methods"])
app.include_router(order_router, tags=["Order Methods"])
app.include_router(order_details_router, tags=["Order Details Methods"])
app.include_router(details_router, tags=["Details Methods"])


# if __name__ == "__main__":
