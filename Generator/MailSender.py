import logging
import zipfile
import os

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from Data.DataReader import DataReader
from Util import FileUtils
from model.Bill import Bill
from model.Config import Config


class MailSender:
    def __init__(self, config: Config):
        self.config = config

    def send_mails(self):
        base_path = self.config.temp_output_path

        bills = []
        for dir in os.scandir(base_path):
            data_name = ""
            has_receipt = False
            for file_name in os.listdir(dir):
                if file_name.startswith("quittungsfile"):
                    has_receipt = True
                    continue
                if file_name.endswith(".data"):
                    data_name = file_name
            if not has_receipt:
                logging.info(dir + " has no receipt file")
                continue
            local_data_file = os.path.join(dir, data_name)
            logging.info("loading file " + local_data_file)

            file = open(local_data_file, "r")
            lines = file.readlines()
            file.close()

            data_reader = DataReader()
            for line in lines:
                data_reader.handle_line(line)

            if len(data_reader.list) != 1:
                logging.error("there are multiple bills in one file: " + local_data_file)
                return None

            for bl in data_reader.list:
                bills.append(bl)

        self.__send_mails__(bills)

    def __send_mails__(self, bills: []):
        smtp = smtplib.SMTP(host=self.config.smtp_host, port=self.config.smtp_port)
        smtp.starttls()
        try:
            logging.info(
                "Try to login to SMTP Server: " + self.config.smtp_host + ":" + self.config.smtp_port.__str__())
            smtp.login(self.config.mail_username, self.config.mail_password)
        except:
            logging.error("Can't login to " + self.config.mail_username + " with provided password")
            return False

        for bill in bills:
            if not self.__send_mail(bill, smtp):
                return False
        return True

    def __send_mail(self, bill: Bill, smtp: smtplib.SMTP):
        logging.info("starting to send mail for bill with id " + bill.bill_id)

        msg = MIMEMultipart()
        message = FileUtils.read_template(self.config.mail_template_path).substitute(
            BILLER_NAME=bill.biller.name,
            DATE=bill.date,
            BILL_ID=bill.bill_id,
            FTP_OUT_ADDRESS=self.config.ftp_output_server
        )

        msg['From'] = self.config.mail_username
        msg['To'] = bill.biller.mail
        msg['Subject'] = "Erfolgte Verarbeitung Rechnung " + bill.bill_id
        msg.attach(MIMEText(message, 'plain'))

        # TODO attach zip
        base_dir = self.config.temp_output_path + "\\" + bill.bill_id
        zip_file_name = base_dir + "\\Rechnung " + bill.bill_id + ".zip"
        zipf = zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED)
        for f in os.listdir(base_dir):
            if f.endswith(".data"):
                continue
            if f.endswith(".zip"):
                continue
            zipf.write(base_dir + "\\" + f)
        zipf.close()

        archive = open(f'{zip_file_name}', 'rb')
        part = MIMEApplication(archive.read(), Name=zip_file_name)
        part['Content-Disposition'] = f"attachement; filename={zip_file_name}"
        msg.attach(part)

        try:
            smtp.send_message(msg)
            return True
        except:
            logging.error("error sending mail for bill: " + bill.bill_id)
            return False

