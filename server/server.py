import os
from typing import Optional
from fastapi import FastAPI, Header, status, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import stripe
from decouple import config
import uvicorn
from test_request import make_line_items, add_orders_to_db


stripe.api_key = config("STRIPE_SECRET_KEY")
domain_url = config("DOMAIN")

static_dir = str(os.path.abspath(os.path.join(__file__, "..", config("STATIC_DIR"))))

templates = Jinja2Templates(directory=static_dir)

app = FastAPI()
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
def get_example(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# table = [
#     {"prod_id": "prod_NBVakPxU1l9YbW", "price_id": "price_1MR8YqCJwyo8UAtARGVzKF16"},
#     {"prod_id": "prod_NBXqhX9LKpilwo", "price_id": "price_1MRAlCCJwyo8UAtAo2GipZWm"},
# ]


@app.post("/create-checkout-session")
async def create_checkout_session(request: Request):
    content_type = request.headers.get("Content-Type")
    if content_type is None:
        return "No Content-Type provided."
    elif content_type == "application/json":
        try:
            product_info = await request.json()
            print(type(product_info))
            items = make_line_items(product_info)

        except Exception as e:
            print(e)
            print("Invalid JSON data.")
    else:
        print("Content-Type not supported.")
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=items,
            mode="payment",
            success_url=domain_url
            + "/static/success.html?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "/static/canceled.html",
        )
        print("success")
        add_orders_to_db(checkout_session)

        return {"status_code": status.HTTP_200_OK, "detail": checkout_session}
    except Exception as e:
        return {"status_code": status.HTTP_403_FORBIDDEN, "detail": str(e)}


# @app.post("/update-database")
# async def update_database(session : stripe.checkout.Session.id):
#     x = stripe.PaymentIntent.retrieve(session.payment_intent,)
#     return x


class WebHookData(BaseModel):
    data: dict
    type: str


@app.post("/webhook")
def webhook_received(
    request_data: WebHookData, stripe_signature: Optional[str] = Header(None)
):
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    webhook_secret = config("STRIPE_WEBHOOK_SECRET")
    # request_data = json.loads(request.data)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret
        # if webhook signing is configured.
        signature = stripe_signature
        try:
            event = stripe.Webhook.construct_event(
                payload=request_data, sig_header=signature, secret=webhook_secret
            )
            data = event["data"]
        except Exception as e:
            return e
        # Get the type of webhook event sent
        # - used to check the status of PaymentIntents.
        event_type = event["type"]
    else:
        data = request_data["data"]
        event_type = request_data["type"]
    data_object = data["object"]

    print("event " + event_type)
    print("data = " + data_object)

    if event_type == "checkout.session.completed":
        print("🔔 Payment succeeded!")
        # Note: If you need access to the line items, for instance to
        # automate fullfillment based on the the ID of the Price, you'll
        # need to refetch the Checkout Session here, and expand the line items:
        #
        # session = stripe.checkout.Session.retrieve(
        #     data['object']['id'], expand=['line_items'])
        #
        # line_items = session.line_items
        #
        # Read more about expand here: https://stripe.com/docs/expand
    return {"status": "success"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)
