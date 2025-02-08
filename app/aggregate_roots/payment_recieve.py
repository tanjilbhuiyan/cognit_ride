class PaymentAggregateRoot:
    def __init__(self, data):
        self.data = data
        self.populated_data = []
        pass

    def validate_data(self):
        pass

    def create(self):
        self.validate_data()

        pass
