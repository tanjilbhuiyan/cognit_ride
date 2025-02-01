from app.repository.interfaces import IPaymentAccountRepository
from typing import List, Dict, Optional
from app.models.payment_account import PaymentMethod
from fastapi import Depends
from sqlalchemy.orm import Session
from app.repository.PaymentAccount.payment_account import PaymentAccountRepository
from app.repository.database import get_db


class PaymentAccountService:
    def __init__(self, repository: IPaymentAccountRepository):
        self.repository = repository

    def received_payment(self, payment_data):
        return self.repository.create_payment_account(payment_data)
