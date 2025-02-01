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

    def create_payment_account(self, user_id: int):
        return self.repository.create_payment_account(user_id)

    def add_payment_method(self, payment_account_id: int, name: str, payment_method_type: str, details: Dict):
        return self.repository.add_payment_method(payment_account_id, name, payment_method_type, details)

    def get_payment_methods(self, payment_account_id: int) -> List[PaymentMethod]:
        return self.repository.get_payment_methods(payment_account_id)

    def set_default_payment_method(self, payment_account_id: int, payment_method_id: int):
        return self.repository.set_default_payment_method(payment_account_id, payment_method_id)

    def get_default_payment_method(self, payment_account_id: int) -> Optional[PaymentMethod]:
        return self.repository.get_default_payment_method(payment_account_id)



def get_payment_account_service(db: Session = Depends(get_db)):
    repository = PaymentAccountRepository(db)
    return PaymentAccountService(repository)