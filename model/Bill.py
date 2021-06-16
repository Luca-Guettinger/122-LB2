from datetime import datetime


class Bill:
    def __init__(
            self,
            bill_id,
            order_id,
            sender_location,
            date: datetime,
            payment_target,
    ):
        self.bill_id = bill_id
        self.order_id = order_id
        self.sender_location = sender_location
        self.date = date
        self.payment_target = payment_target

    def is_valid(self):
        return True

    def __repr__(self):
        return f'Bill_id: {self.bill_id};\n' \
               f'Order_id: {self.order_id};\n' \
               f'Location: {self.sender_location};\n' \
               f'Date: {self.date};\n' \
               f'Time: {self.time};\n' \
               f'Days2Pay: {self.days_to_pay};'

    def __str__(self):
        return f'Bill_id: {self.bill_id};\n' \
               f'Order_id: {self.order_id};\n' \
               f'Location: {self.sender_location};\n' \
               f'Date: {self.date};\n' \
               f'Time: {self.time};\n' \
               f'Days2Pay: {self.days_to_pay};'
