import uuid

from app.aggregate_roots.payment_recieve import PaymentAggregateRoot
from app.queue.publisher.payment_success import PublishPaymentSuccess
from app.repository.payment_received.payment_recieved import PaymentReceivedRepository



class PaymentCommandHandler:
    def _init_(self):
        self.publisher = PublishPaymentSuccess()

    def handle_received_payment(self, data):
        aggregate_root = PaymentAggregateRoot(data)
        aggregate_root.create()
        repo = PaymentReceivedRepository()
        repo.save_payment(aggregate_root)
        # Make success message
        success_payload = {
            "id": uuid.uuid4()[:8]
        }
        # publish success
        self.publisher.publish_success_message(success_payload)
        pass
