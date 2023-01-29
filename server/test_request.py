import requests
from decouple import config
from config.db import session
from models.index import Products

domain_url = config("DOMAIN")


def make_request(url, data):
    try:
        x = requests.post(url, json=data)
        print(x.json())
    except Exception as e:
        print(e)


url = domain_url + "/create-checkout-session"


def make_line_items(product_list: list):
    result = []
    for prod in product_list:
        try:
            temp = (
                session.query(Products)
                .filter(Products.id == prod["product_id"])
                .first()
                .__dict__
            )
            result.append(
                {
                    "price_data": {
                        "currency": temp["currency"],
                        "unit_amount": int(temp["default_price"]) * 100,
                        "product_data": {
                            "name": temp["product_name"],
                            "images": [temp["images"]],
                        },
                    },
                    "quantity": prod["quantity"],
                }
            )
        except Exception as e:
            print(e)
    return result


# def add_orders_to_db(session):
#     print(session)
#     pass
# print(make_request(url, result))
