from sqlalchemy import String, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal
from .base import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(500))
    price: Mapped[Decimal] = mapped_column(Numeric(10,2))
    quantity: Mapped[int] = mapped_column()
    seller_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    def __repr__(self):
        return f"ID:{self.id}, NAME:{self.name}, DESCRIPTION:{self.description}, PRICE:{self.price}, LEFT:{self.quantity}, SELLER:{self.seller_id}"