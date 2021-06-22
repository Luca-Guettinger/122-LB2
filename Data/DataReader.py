import logging

from datetime import datetime, timedelta

from model.Bill import Bill
from model.BillPosition import BillPosition
from model.Biller import Biller
from model.Client import Client


class DataReader:
    current: Bill
    list: list

    def __init__(self):
        self.list = list()

    def handle_line(self, line: str):
        if line.startswith('Rechnung'):
            self.__handle_bill(line)
        if line.startswith("Herkunft"):
            self.__handle_biller(line)
        if line.startswith("Endkunde"):
            self.__handle_client(line)
        if line.startswith("RechnPos"):
            self.__handle_pos(line)

    def print_list(self):
        print(self.list)

    def __handle_bill(self, line: str):
        current_bill = Bill(None, None, None, None, None, None)
        segmented_line = str.split(line, ";")
        if len(segmented_line) != 6:
            logging.error('error with line: ' + line + " please use the correct Format.")
            return False

        bill_id = segmented_line[0]
        if len(bill_id.split('_')) != 2:
            logging.error('error on line ' + line + " no '_' found in the bill ID.")
            return False

        current_bill.bill_id = bill_id.split('_')[1]

        order_id = segmented_line[1]
        if len(order_id.split('_')) != 2:
            logging.error('error on line ' + line + " no '_' found in the Order ID.")
            return False

        current_bill.order_id = order_id.split('_')[1]

        current_bill.sender_location = segmented_line[2]

        date_string = segmented_line[3] + " " + segmented_line[4]
        try:
            current_bill.date = datetime.strptime(date_string, "%d.%m.%Y %H:%M:%S")
        except:
            logging.error("invalid date or time (dd.MM.yyyy) (hh:mm:ss) for bill with id " + bill_id + ": "
                          + date_string + ".")
            return False

        payment_target = segmented_line[5]
        if len(payment_target.split('_')) != 2:
            logging.error("error on line " + line + "\n "
                                                    "no '_' found in the Payment Target. "
                                                    "Expected: 'ZahlungszielInTagen_<days>")
            return False

        days_to_pay_as_string = payment_target.split("_")[1]
        try:
            days_to_pay = int(days_to_pay_as_string)
            current_bill.days_to_pay = days_to_pay
            current_bill.payment_target = datetime.now() + timedelta(days=days_to_pay)
            self.list.append(current_bill)
            self.current = current_bill
            return True
        except:
            logging.error("Error while converting Payment Target to a valid Date, trying to convert: "
                          + days_to_pay_as_string)
            return False

    def __handle_biller(self, line: str):
        biller = Biller(None, None, None, None, None, None, None)
        segmented_line = str.split(line, ";")

        if len(segmented_line) != 8:
            logging.error("error with line: '" + line + "' please use the correct Format.")
            return False

        biller.party_id = segmented_line[1]
        biller.account_id = segmented_line[2]
        biller.name = segmented_line[3]
        biller.street = segmented_line[4]
        biller.zip = segmented_line[5]
        biller.company_id = segmented_line[6]
        biller.mail = segmented_line[7]

        if self.current is None:
            logging.error("error with line: '" + line + "', no bill found.")

        self.current.biller = biller

    def __handle_client(self, line: str):
        client = Client(None, None, None, None)
        segmented_line = str.split(line, ";")
        if len(segmented_line) != 5:
            logging.error("error with line: '" + line + "' please use the correct Format.")
            return False

        client.account_id = segmented_line[1]
        client.name = segmented_line[2]
        client.street = segmented_line[3]
        client.zip = segmented_line[4]

        if self.current is None:
            logging.error("error with line: '" + line + "', no bill found.")

        self.current.client = client

    def __handle_pos(self, line: str):
        pos = BillPosition(None, None, None, None, None, None)
        segmented_line = str.split(line, ";")
        if len(segmented_line) != 7:
            logging.error("error with line: '" + line + "' please use the correct Format.")
            return False

        pos.number = segmented_line[1]
        pos.name = segmented_line[2]
        pos.amount = segmented_line[3]
        pos.price = segmented_line[4]
        pos.total = segmented_line[5]
        pos.mwst = segmented_line[6]

        if self.current is None:
            logging.error("error with line: '" + line + "', no bill found.")

        self.current.positions.append(pos)

