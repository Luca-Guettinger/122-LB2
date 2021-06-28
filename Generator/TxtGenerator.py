import logging
import math
from datetime import datetime, date

from Util import FileUtils, BillUtils
from model.Bill import Bill
from model.BillPosition import BillPosition
from model.Config import Config


class TxtGenerator:
    def __init__(self, config: Config):
        self.config = config

    def write_bills(self, bills: []):
        for bill in bills:
            if not self.__write_txt(bill):
                return False
        return True

    def __write_txt(self, bill: Bill):
        out_path = f'{self.config.temp_output_path}\\{bill.bill_id}\\{bill.biller.account_id}_{bill.bill_id}_invoice.txt'

        # try:
        place_date = bill.sender_location + ", den " + date.today().strftime("%d.%m.%Y")
        total_bill_amount = BillUtils.sum_positions_totals(bill)
        total_decimal = str(total_bill_amount - int(total_bill_amount))[1:]

        if total_decimal == "" or total_decimal.startswith(",") or total_decimal.startswith("."):
            total_decimal = "0"

        bill_positions = ""
        for pos_a in bill.positions:
            pos: BillPosition
            pos = pos_a
            bill_positions += "{:>3} {:35} {:>3} {:>10}  CHF {:>11}  {:1}\n".format(pos.number, pos.name, pos.amount,
                                                                                    pos.price, pos.total,
                                                                                    pos.mwst.split("_")[1])

        xml = FileUtils.read_template(self.config.txt_template_path).substitute(
            BILL_POSITIONS=bill_positions,
            BILL_PLACE_DATE=place_date,
            BILLER_COMPANY=bill.biller.company_id,
            BILLER_NAME=bill.biller.name,
            BILLER_STREET=bill.biller.street,
            BILLER_ZIP=bill.biller.zip,
            CLIENT_NAME=bill.client.name,
            CLIENT_STREET=bill.client.street,
            CLIENT_ZIP=bill.client.zip,
            BILLER_CLIENT_ID=bill.biller.account_id,
            BILL_PAYMENT_TARGET=bill.payment_target.strftime("%d.%m.%Y"),
            BILLER_ACCOUNT_ID=bill.biller.party_id,
            BILL_ORDER_ID=bill.order_id,
            BILL_ID=bill.bill_id
        ).format(
            total_bill_amount,
            BillUtils.sum_mwst_totals(bill),
            math.trunc(total_bill_amount),
            total_decimal,
            math.trunc(total_bill_amount),
            total_decimal,
            bill.client.name,
            bill.client.street,
            bill.biller.party_id,
            bill.client.zip
        )
        FileUtils.write_to_file(xml, out_path)
        return True
    # except:
    #     logging.error("Couldn't write xml for bill " + bill.bill_id)
    #     return False
