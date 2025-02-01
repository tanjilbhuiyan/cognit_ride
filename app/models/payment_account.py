from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from app.repository.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    payment_accounts = relationship("PaymentAccount", back_populates="user")


class PaymentAccount(Base):
    __tablename__ = "payment_account"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    account_status = Column(Enum("active", "disabled", "pending", name="account_status"), default="pending")
    default_payment_method_id = Column(Integer, ForeignKey("payment_method.id"), nullable=True)
    # Relationship to User
    user = relationship("User", back_populates="payment_accounts")

    # Relationship to PaymentMethod
    payment_methods = relationship("PaymentMethod", back_populates="payment_account")



class PaymentMethod(Base):
    __tablename__ = "payment_method"

    id = Column(Integer, primary_key=True, index=True)
    payment_account_id = Column(Integer, ForeignKey("payment_account.id"), nullable=False)
    name = Column(String, nullable=False)
    payment_method_type = Column(String, nullable=False)  # e.g., "credit_card", "digital_wallet"
    details = Column(JSON, nullable=False)  # Stores payment method details (e.g., card number, wallet ID)

    # Relationship to PaymentAccount
    payment_account = relationship("PaymentAccount", back_populates="payment_methods")