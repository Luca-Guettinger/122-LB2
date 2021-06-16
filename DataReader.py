import logging

from datetime import datetime, timedelta

from model.Bill import Bill


class DataReader:
    current: Bill
    list: list

    def __init__(self):
        self.list = list()

    def handle_line(self, line: str):
        if line.startswith('Rechnung'):
            self.__handle_bill(line)
        print(line)

    def __handle_bill(self, line: str):
        self.current = Bill(None, None, None, None, None)
        split = str.split(line, ";")
        if len(split) != 6:
            logging.error('error with line: ' + line + " please use the correct Format.")
            return False

        bill_id = split[0]
        if len(bill_id.split('_')) != 2:
            logging.error('error on line ' + line + " no '_' found in the bill ID.")
            return False

        self.current.bill_id = bill_id.split('_')[1]

        order_id = split[1]
        if len(order_id.split('_')) != 2:
            logging.error('error on line ' + line + " no '_' found in the Order ID.")
            return False

        self.current.order_id = order_id.split('_')[1]

        self.current.sender_location = split[2]

        split_ = split[3] + " " + split[4]
        self.current.date = datetime.strptime(split_, "'%d.%m.%Y %H:%M:%S")
        try:
            pass
        except:
            logging.error('error on line ' + line + " invalid date.")
            return False

        payment_target = split[5]
        if len(payment_target.split('_')) != 2:
            logging.error('error on line ' + line + " no '_' found in the Payment Target.")
            return False

        try:
            days_to_pay = int(payment_target[5].split("_")[1])
            self.current.days_to_pay = days_to_pay
            self.current.payment_target = datetime.now() + timedelta(days=days_to_pay)
            self.list.append(self.current)
            return True
        except:
            logging.error('error on line ' + line + ". Payment Target is not a number.")
            return False

    def __is_bill_valid(self):
        if self.current is None:
            return True
        if not self.current.is_valid():
            return False
        else:
            return True







