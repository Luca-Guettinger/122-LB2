import logging
from datetime import datetime, date

from Util import FileUtils
from model.Bill import Bill
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
        out_path = f'{self.config.temp_output_path}\\{bill.biller.account_id}_{bill.bill_id}_invoice.txt'

        #try:
        place_date = bill.sender_location + ", den " + date.today().strftime("%d.%m.%Y")
        xml = FileUtils.read_template(self.config.txt_template_path).substitute(
            BILL_PLACE_DATE=place_date,
            BILLER_COMPANY=bill.biller.company_id,
            BILLER_NAME=bill.biller.name,
            BILLER_STREET=bill.biller.street,
            BILLER_ZIP=bill.biller.zip,
            CLIENT_NAME=bill.client.name,
            CLIENT_STREET=bill.client.street,
            CLIENT_ZIP=bill.client.zip,
            BILLER_CLIENT_ID=bill.biller.account_id,
            BILL_ORDER_ID=bill.order_id,
            BILL_ID=bill.bill_id
        )
        FileUtils.write_to_file(xml, out_path)
        return True
       # except:
       #     logging.error("Couldn't write xml for bill " + bill.bill_id)
       #     return False
