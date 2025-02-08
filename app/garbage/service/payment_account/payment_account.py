from app.garbage.interfaces import IPaymentAccountRepository


class PaymentAccountService:
    def __init__(self, repository: IPaymentAccountRepository):
        self.repository = repository

    def received_payment(self, payment_data):
        return self.repository.create_payment_account(payment_data)
