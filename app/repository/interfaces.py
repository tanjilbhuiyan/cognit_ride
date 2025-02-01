from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from app.models.payment_account import PaymentMethod


class IPaymentAccountRepository(ABC):
    @abstractmethod
    def create_payment_account(self, user_id: int):
        pass

    @abstractmethod
    def add_payment_method(self, payment_account_id: int, name: str, payment_method_type: str, details: dict):
        pass

    @abstractmethod
    def get_payment_methods(self, payment_account_id: int) -> List[PaymentMethod]:
        pass

    @abstractmethod
    def set_default_payment_method(self, payment_account_id: int, payment_method_id: int):
        pass

    @abstractmethod
    def get_default_payment_method(self, payment_account_id: int) -> Optional[PaymentMethod]:
        pass