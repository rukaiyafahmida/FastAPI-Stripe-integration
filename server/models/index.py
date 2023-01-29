from models.user import Users
from models.order import Orders
from models.order_details import OrderDetails
from models.product import Products


from sqlalchemy.orm import relationship


Users.orders = relationship("Orders", order_by=Orders.id, back_populates="users")
Orders.order_details = relationship(
    "OrderDetails", order_by=OrderDetails.id, back_populates="orders"
)
Products.order_details = relationship(
    "OrderDetails", order_by=OrderDetails.id, back_populates="product"
)
