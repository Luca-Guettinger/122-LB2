import logging
import os
from ftplib import FTP

from Data.DataReader import DataReader
from model.Config import Config
from model.ReceiptInformation import ReceiptInformation


class OutputLoader:
    ftp: FTP
    receipts = {}
    current_receipt_file = ""

    def __connect_output(self):
        self.ftp = FTP(self.config.ftp_output_server)
        logging.info(
            "starting to login into the server " + self.config.ftp_output_server + " with the username " + self.config.ftp_output_username)
        self.ftp.login(self.config.ftp_output_username, self.config.ftp_output_password)

    def __init__(self, config: Config):
        self.config = config
        try:
            self.__connect_output()
        except:
            self.ftp = None
            logging.error(
                "error connecting to ftp server '" + self.config.ftp_output_server + "' with username: '" + self.config.ftp_output_username + "'")

    # uploads the generated files to FTP Server
    def upload_files(self):
        files = []

        try:
            self.ftp.cwd(self.config.ftp_output_path)
        except:
            logging.error("error navigating to directory: " + self.config.ftp_output_path)
            return None

        for path in os.scandir(self.config.temp_output_path):
            for file_name in os.listdir(path):
                if (file_name.endswith(".data")):
                    continue
                dir = self.config.temp_output_path + "\\" + file_name.split("_")[1] + "\\" + file_name
                with open(dir, "rb") as file:
                    self.ftp.storbinary("STOR %s" % file_name, file)

    def handle_receipts(self):
        try:
            self.ftp.cwd(self.config.ftp_output_receipt_path)
        except:
            logging.error("error navigating to directory: " + self.config.ftp_output_path)
            return None

        for file_name in self.ftp.nlst():
            if not file_name.startswith("quittungsfile"):
                logging.warning("file " + file_name + " will be ingored.")
                continue
            self.current_receipt_file = file_name
            retrlines = self.ftp.retrlines("RETR " + file_name, callback=self.__read_receipt_line)

        base_path = self.config.temp_output_path
        for rec in self.receipts:
            receipt: ReceiptInformation
            receipt = self.receipts[rec]

            if not receipt.txt_found and not receipt.xml_found:
                logging.error("Fehler beim bearbeiten der Quitting für die Rechnung " + receipt.bill_id)
                continue

            local_data_file = base_path + "\\" + receipt.bill_id + "\\rechnung" + receipt.bill_id + ".data"
            logging.info("loading file " + local_data_file)

            file = open(local_data_file, "r")
            lines = file.readlines()
            file.close()

            data_reader = DataReader()
            for line in lines:
                data_reader.handle_line(line)
            bills = data_reader.list

            if len(bills) != 1:
                logging.error("there are multiple bills in one file: " + local_data_file)
                return None

            if not os.path.isfile(local_data_file):
                logging.error("no local data file found, exiting process: " + local_data_file)
                return None
            os.remove(local_data_file)

            with open(base_path + "\\" + receipt.bill_id + "\\" + receipt.file_name, "wb") as file:
                copy_file = self.ftp.retrbinary("RETR " + receipt.file_name, file.write)
                if copy_file != "226 Transfer complete":
                    logging.error("error downloading file " + self.config.ftp_source_path + "/" + receipt.file_name)
                    return None
                self.ftp.delete(receipt.file_name)

    def __read_receipt_line(self, line: str):
        bill_id = "NONE"
        file_name = ""
        for arg in line.split(" "):
            if not arg.endswith(".txt") and not arg.endswith(".xml"):
                continue
            bill_id = arg.split("_")[1]
            file_name = arg

        if bill_id == "NONE":
            return False

        if bill_id not in self.receipts:
            information = ReceiptInformation()
            information.bill_id = bill_id
            information.file_name = self.current_receipt_file
            self.receipts[bill_id] = information

        receipt: ReceiptInformation

        receipt = self.receipts[bill_id]

        if file_name.endswith("txt"):
            receipt.txt_found = True
        if file_name.endswith("xml"):
            receipt.txt_found = True
        return True
