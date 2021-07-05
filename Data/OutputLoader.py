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
            last_file_path = ""
            last_file_name = ""
            has_receipt = False
            for file_name in os.listdir(path):
                if has_receipt:
                    continue
                if file_name.endswith(".data"):
                    continue
                if file_name.startswith("quittungsfile"):
                    has_receipt = True
                    continue
                last_file_path = self.config.temp_output_path + "\\" + file_name.split("_")[1]
                last_file_name = file_name

            if not has_receipt:
                txt_file_name = last_file_name.split(".")[0] + ".txt"
                with open(last_file_path + "\\" + txt_file_name, "rb") as file_txt:
                    self.ftp.storbinary("STOR %s" % txt_file_name, file_txt)

                xml_file_name = last_file_name.split(".")[0] + ".xml"
                with open(last_file_path + "\\" + xml_file_name, "rb") as file_txt:
                    self.ftp.storbinary("STOR %s" % xml_file_name, file_txt)

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

            if not os.path.isfile(local_data_file):
                logging.error("no local data file found, exiting process: " + local_data_file)
                return None

            with open(base_path + "\\" + receipt.bill_id + "\\" + receipt.file_name, "wb") as file:
                copy_file = self.ftp.retrbinary("RETR " + receipt.file_name, file.write)
                if not copy_file.startswith("226"):
                    logging.error("error downloading file " + self.config.ftp_source_path + "/" + receipt.file_name)
                    return None
        deleted = []
        for rec_to_delete_key in self.receipts:
            rec_to_delete = self.receipts[rec_to_delete_key]
            if rec_to_delete.file_name in deleted:
                continue
            deleted.append(rec_to_delete.file_name)
            self.ftp.delete(rec_to_delete.file_name)

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

    def upload_zip_and_delete_files(self):
        for path in os.scandir(self.config.temp_output_path):
            zip_name = ""
            for file_name in os.listdir(path):
                if file_name.endswith(".zip"):
                    zip_name = file_name
                    break
            #TODO do this

        pass
