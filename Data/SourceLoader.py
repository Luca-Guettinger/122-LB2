import logging
import os
from ftplib import FTP
from pathlib import Path

from Data.DataReader import DataReader
from model.Config import Config


class DataLoader:
    ftp: FTP

    def __connect_source(self):
        self.ftp = FTP(self.config.ftp_source_server)
        logging.info(
            "starting to login into the server " + self.config.ftp_source_server + " with the username " + self.config.ftp_source_username)
        self.ftp.login(self.config.ftp_source_username, self.config.ftp_source_password)

    def __init__(self, config: Config):
        self.config = config
        try:
            self.__connect_source()
        except:
            self.ftp = None
            logging.error(
                "error connecting to ftp server '" + self.config.ftp_source_server + "' with username: '" + self.config.ftp_source_username + "'")

    def load_data(self):
        files = []
        result = []
        try:
            self.ftp.cwd(self.config.ftp_source_path)
            files = self.ftp.nlst()
        except:
            logging.error("error navigating to directory: " + self.config.ftp_source_path)

        for file_name in files:
            if not file_name.startswith("rechnung") and not file_name.endswith(".data"):
                if file_name.startswith("."):
                    continue

                logging.warning("file " + file_name + " can not be processed. ")
                continue
            for bill in self.read_file(file_name):
                result.append(bill)
        return result

    def read_file(self, file_name: str):
        if self.ftp is None:
            return None

        bill_id = file_name.replace("rechnung", "").replace(".data", "")
        local_dir = self.config.temp_output_path + "\\" + bill_id
        Path(local_dir).mkdir(parents=True, exist_ok=True)

        with open(local_dir + "/" + file_name, "wb") as file:
            data_reader = DataReader()
            copy_file = self.ftp.retrbinary("RETR " + file_name, file.write)
            if copy_file != "226 Transfer complete":
                logging.error("error downloading file " + self.config.ftp_source_path + "/" + file_name)
                return None

        read_lines = self.ftp.retrlines("RETR " + file_name, callback=data_reader.handle_line)

        if read_lines != "226 Transfer complete":
            logging.error("error reading data from file  " + self.config.ftp_source_path + "/" + file_name)
            return None

        result = []
        for bill in data_reader.list:
            if len(bill.positions) > 0:
                result.append(bill)

        return result
