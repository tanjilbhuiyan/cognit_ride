from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Nested models
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
    collected_by: str
    cash_collected: float
    change_amount: float


# Main model
class ReceivedPayment(BaseModel):
    user_id: str
    ride_id: str
    trip_details: TripDetails
    fare_breakdown: FareBreakdown
    amount: float
    transaction_status: str
    created_at: int
    payment_method: str
    transaction_id: str
    payment_details: PaymentDetails
