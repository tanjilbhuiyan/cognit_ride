from abc import ABC, abstractmethod


class IPaymentAccountRepository(ABC):
    @abstractmethod
    def create_payment_account(self, user_id: int):
        pass
