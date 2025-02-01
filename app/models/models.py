from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric, Boolean
from sqlalchemy.orm import relationship
from app.repository.database import Base
from datetime import datetime

class PassengersInfo(Base):
    __tablename__ = "passengers_info"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationships
    payment_methods = relationship("PaymentMethod", back_populates="passenger")
    payment_accounts = relationship("PaymentAccount", back_populates="passenger")

class DriversInfo(Base):
    __tablename__ = "drivers_info"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True)
    password_hash = Column(String, nullable=False)
    license_number = Column(String, unique=True, nullable=False)
    vehicle_info = Column(String)
    rating = Column(Numeric(3, 2), default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    is_available = Column(Boolean, default=True)

class PaymentMethod(Base):
    __tablename__ = "payment_method"

    id = Column(Integer, primary_key=True, index=True)
    passenger_id = Column(Integer, ForeignKey("passengers_info.id"))
    method_type = Column(String, nullable=False)  # e.g., "credit_card", "debit_card", "mobile_banking"
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    passenger = relationship("PassengersInfo", back_populates="payment_methods")
    payment_accounts = relationship("PaymentAccount", back_populates="payment_method")

class PaymentAccount(Base):
    __tablename__ = "payment_account"

    id = Column(Integer, primary_key=True, index=True)
    passenger_id = Column(Integer, ForeignKey("passengers_info.id"))
    payment_method_id = Column(Integer, ForeignKey("payment_method.id"))
    account_details = Column(String, nullable=False)  # Encrypted account details
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    passenger = relationship("PassengersInfo", back_populates="payment_accounts")
    payment_method = relationship("PaymentMethod", back_populates="payment_accounts")
