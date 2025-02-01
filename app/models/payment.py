from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class PaymentMethod(str, Enum):
    CARD = "CARD"
    CASH = "CASH"
    MFS = "MFS"

class TransactionStatus(str, Enum):
    COMPLETED = "COMPLETED"
    PENDING = "PENDING"
    FAILED = "FAILED"

class Location(BaseModel):
    address: str
    latitude: float
    longitude: float

class TripDetails(BaseModel):
    pickup_location: Location
    dropoff_location: Location
    distance_km: float
    duration_minutes: int
    wait_time_minutes: int

class FareBreakdown(BaseModel):
    base_fare: float
    distance_fare: float
    wait_time_fare: float
    surge_multiplier: float
    surge_amount: float
    vat_percentage: float
    vat_amount: float
    platform_fee: float
    total_fare: float

class PaymentDetails(BaseModel):
    # For Cash payments
    collected_by: Optional[str] = None
    cash_collected: Optional[float] = None
    change_amount: Optional[float] = None
    
    # For Card payments
    card_type: Optional[str] = None
    last_four: Optional[str] = None
    payment_gateway: Optional[str] = None
    
    # For MFS payments
    provider: Optional[str] = None
    provider_transaction_id: Optional[str] = None
    sender_number: Optional[str] = None
    payment_type: Optional[str] = None
    gateway_fee: Optional[float] = None

class Payment(BaseModel):
    transaction_id: str
    user_id: str
    ride_id: str
    trip_details: TripDetails
    fare_breakdown: FareBreakdown
    amount: float
    transaction_status: TransactionStatus
    payment_method: PaymentMethod
    payment_details: PaymentDetails
    created_at: int  # timestamp in milliseconds
