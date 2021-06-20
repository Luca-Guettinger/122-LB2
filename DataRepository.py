import logging
from ftplib import FTP

from DataReader import DataReader


class DataRepository:

    def _connect(self):
        self.ftp = FTP(self.server)
        logging.info("starting to login into the server " + self.server + " with the username " + self.username)
        self.ftp.login(self.username, self.password)

    def __init__(self, server: str, username: str, password: str, path: str):
        self.server = server
        self.username = username
        self.password = password
        self.path = path
        try:
            self._connect()
        except:
            self.ftp = None
            logging.error("error connecting to ftp server '" + self.server + "' with username: '" + self.username + "'")

    def load_data(self, filename: str):
        if self.ftp is None:
            return None

        try:
            self.ftp.cwd(self.path)
        except:
            logging.error("error loading file " + filename + " in directory " + self.path)

        data_reader = DataReader()

        read_lines = self.ftp.retrlines("RETR " + filename, callback=data_reader.handle_line)

        if read_lines != "226 Transfer complete":
            return None

        result = []
        for bill in data_reader.list:
            if len(bill.positions) > 0:
                result.append(bill)

        return result
