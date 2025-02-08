from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from app.repository.database import Base

class PassengersInfo(Base):
    __tablename__ = "passengers_info"

    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True)
    presentAddress = Column(String)
    status = Column(Boolean, default=True)
    rating = Column(Numeric(3, 2), default=0.0)
    createdAt = Column(DateTime, default=datetime.utcnow)

    # Relationships
    payment_methods = relationship("PaymentMethod", back_populates="passenger")
    payment_accounts = relationship("PaymentAccount", back_populates="passenger")

class DriversInfo(Base):
    __tablename__ = "drivers_info"

    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True)
    presentAddress = Column(String)
    status = Column(Boolean, default=True)
    rating = Column(Numeric(3, 2), default=0.0)
    createdAt = Column(DateTime, default=datetime.utcnow)
    
    # Driver specific fields
    licenseType = Column(String, nullable=False)
    vehicleType = Column(String, nullable=False)
    isAvailable = Column(Boolean, default=True)

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