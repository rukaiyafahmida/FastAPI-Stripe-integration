import sqlalchemy
from config.db import engine, Base
from decouple import config


def create_db_tables():
    ## bools for checking if the following tables exists
    user_exist = sqlalchemy.inspect(engine).has_table(config("USER_TABLE"))
    product_exist = sqlalchemy.inspect(engine).has_table(config("PRODUCT_TABLE"))
    order_exist = sqlalchemy.inspect(engine).has_table(config("ORDER_TABLE"))
    order_details_exist = sqlalchemy.inspect(engine).has_table(
        config("ORDER_DETAIL_TABLE")
    )

    ## if user table doesnt exits, creates it
    if user_exist == False:
        print("= user Table doesn't exist=")
        Base.metadata.tables[config("USER_TABLE")].create(engine)
        print("= user Table was created=")
    else:
        print("= user Table exists=")

    ## if product table doesnt exits, creates it
    if product_exist == False:
        print("=product Table doesn't exist=")
        Base.metadata.tables[config("PRODUCT_TABLE")].create(engine)
        print("=product Table was created=")
    else:
        print("=product Table exists=")

    ## if oder table doesnt exits, creates it
    if order_exist == False:
        print("=order Table doesn't exist=")
        Base.metadata.tables[config("ORDER_TABLE")].create(engine)
        print("=order Table was created=")
    else:
        print("=order Table exists=")

    ## if order_detail table doesnt exits, creates it
    if order_details_exist == False:
        print("=order_details Table doesn't exist=")
        Base.metadata.tables[config("ORDER_DETAIL_TABLE")].create(engine)
        print("=order_details Table was created=")
    else:
        print("=order_details Table exists=")
