import logging

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from Util import FileUtils
from model.Bill import Bill
from model.Config import Config


class MailSender:
    def __init__(self, config: Config):
        self.config = config

    def send_mails(self, bills: []):
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

        try:
            smtp.send_message(msg)
            return True
        except:
            logging.error("error sending mail for bill: " + bill.bill_id)
            return False