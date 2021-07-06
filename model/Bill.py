from datetime import datetime

from model.Biller import Biller
from model.Client import Client


class Bill:
    biller: Biller = None
    client: Client = None
    positions: []

    def __init__(
            self,
            bill_id,
            order_id,
            sender_location,
            date: datetime,
            payment_target: datetime,
            days_to_pay,
    ):
        self.bill_id = bill_id
        self.order_id = order_id
        self.sender_location = sender_location
        self.date = date
        self.payment_target = payment_target
        self.days_to_pay = days_to_pay
        self.positions = []

    def __repr__(self):
        return f'Bill_id: {self.bill_id};\n' \
               f'Order_id: {self.order_id};\n' \
               f'Location: {self.sender_location};\n' \
               f'Date: {self.date};\n' \
               f'Payment_target: {self.payment_target};\n' \
               f'Days2Pay: {self.days_to_pay};\n' \
               f'Biller: {self.biller};\n' \
               f'Client: {self.client};\n' \
               f'Positions: {self.positions};\n' \


    def __str__(self):
        return f'Bill_id: {self.bill_id};\n' \
               f'Order_id: {self.order_id};\n' \
               f'Location: {self.sender_location};\n' \
               f'Date: {self.date};\n' \
               f'Payment_target: {self.payment_target};\n' \
               f'Days2Pay: {self.days_to_pay};\n' \
               f'Biller: {self.biller};\n' \
               f'Client: {self.client};\n' \
               f'Positions: {self.positions};\n' \
