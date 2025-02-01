from fastapi import APIRouter, Depends
from app.repository.database import get_db
from app.scalars.payment_recieved_scalars import ReceivedPayment

payment_receiver_router = r = APIRouter()


@r.post("offline_payment")
def received_payment(data: ReceivedPayment, db = Depends(get_db)):
    data = "mim"
    return "Success"
