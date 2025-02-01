from pydantic import BaseModel


class ReceivedPayment(BaseModel):
    user_id: str
    ride_id: str
