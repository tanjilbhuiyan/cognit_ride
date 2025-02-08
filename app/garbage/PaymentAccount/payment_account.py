from sqlalchemy.orm import Session
from app.garbage.models import PaymentAccount, PaymentMethod
from app.garbage.interfaces import IPaymentAccountRepository
from typing import List, Optional


class PaymentAccountRepository(IPaymentAccountRepository):
    def __init__(self, db: Session):
        self.db = db

    def create_payment_account(self, user_id: int):
        payment_account = PaymentAccount(user_id=user_id)
        self.db.add(payment_account)
        self.db.commit()
        self.db.refresh(payment_account)
        return payment_account

    def add_payment_method(self, payment_account_id: int, name: str, payment_method_type: str, details: dict):
        payment_method = PaymentMethod(
            payment_account_id=payment_account_id,
            name=name,
            payment_method_type=payment_method_type,
            details=details
        )
        self.db.add(payment_method)
        self.db.commit()
        self.db.refresh(payment_method)
        return payment_method

    def get_payment_methods(self, payment_account_id: int) -> List[PaymentMethod]:
        return self.db.query(PaymentMethod).filter(PaymentMethod.payment_account_id == payment_account_id).all()

    def set_default_payment_method(self, payment_account_id: int, payment_method_id: int):
        payment_account = self.db.query(PaymentAccount).filter(PaymentAccount.id == payment_account_id).first()
        if payment_account:
            payment_account.default_payment_method_id = payment_method_id
            self.db.commit()
            self.db.refresh(payment_account)
        return payment_account

    def get_default_payment_method(self, payment_account_id: int) -> Optional[PaymentMethod]:
        payment_account = self.db.query(PaymentAccount).filter(PaymentAccount.id == payment_account_id).first()
        if payment_account:
            return self.db.query(PaymentMethod).filter(PaymentMethod.id == payment_account.default_payment_method_id).first()
        return None