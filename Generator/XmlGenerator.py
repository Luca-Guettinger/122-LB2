import logging
from datetime import datetime

from Util import FileUtils, BillUtils
from model.Bill import Bill
from model.Config import Config


class XmlGenerator:
    def __init__(self, config: Config):
        self.config = config

    def write_bills(self, bills: []):
        for bill in bills:
            if not self.__write_xml(bill):
                return False
        return True

    def __write_xml(self, bill: Bill):
        out_path = f'{self.config.temp_output_path}\\{bill.biller.account_id}_{bill.bill_id}_invoice.xml'

        try:
            xml = FileUtils.read_template(self.config.xml_template_path).substitute(
                BILLER_ACCOUNT=bill.biller.party_id,
                BILLER_COMPANY=bill.biller.company_id,
                BILLER_NAME=bill.biller.name,
                BILLER_STREET=bill.biller.street,
                BILLER_ZIP=bill.biller.zip,
                CLIENT_ACCOUNT=bill.client.account_id,
                CLIENT_NAME=bill.client.name,
                CLIENT_STREET=bill.client.street,
                CLIENT_ZIP=bill.client.zip,
                TIMESTAMP=datetime.now().timestamp(),
                DATE=bill.date,
                BILL_ID=bill.bill_id,
                ORDER_ID=bill.order_id,
                TOTAL_SUM=BillUtils.sum_positions_totals(bill),
                DAYS2PAY=bill.days_to_pay,
                DAYS2PAYANDONE=int(bill.days_to_pay) + 1,
                DUE_DATE=bill.payment_target,
            )
            FileUtils.write_to_file(xml, out_path)
            return True
        except:
            logging.error("Couldn't write xml for bill " + bill.bill_id)
            return False
