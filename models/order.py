from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date
from .base import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column()
    

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_date: Mapped[date] = mapped_column(Date)
    customer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    def __repr__(self):
        return f"ID:{self.id}, DATE:{self.order_date}, ORDERED BY:{self.customer_id}"
    