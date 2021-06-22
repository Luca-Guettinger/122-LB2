import logging
from ftplib import FTP

from Data.DataReader import DataReader
from model.Config import Config


class DataLoader:
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
        if self.ftp is None:
            return None

        file_name = self.config.ftp_source_file_name
        try:
            self.ftp.cwd(self.config.ftp_source_path)
        except:
            logging.error("error loading file " + file_name + " in directory " + self.config.ftp_source_path)

        data_reader = DataReader()

        read_lines = self.ftp.retrlines("RETR " + file_name, callback=data_reader.handle_line)

        if read_lines != "226 Transfer complete":
            return None

        result = []
        for bill in data_reader.list:
            if len(bill.positions) > 0:
                result.append(bill)

        return result
