import stripe
from decouple import config

# Setup Stripe python client library.
stripe.api_key = config("STRIPE_SECRET_KEY")


# Create specific keys for the product and prices
def generate_product_price(product: dict):

    starter_product = stripe.Product.create(
        name=product["name"], description=product["description"]
    )
    starter_product_price = stripe.Price.create(
        unit_amount=product["price"],
        currency=product["currency"],
        # recurring={"interval": "month"},
        product=starter_product["id"],
    )
    return {
        "product_id": starter_product["id"],
        "product_price": starter_product_price["id"],
    }
