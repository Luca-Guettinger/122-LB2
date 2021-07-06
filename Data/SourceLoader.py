import logging
import os
from ftplib import FTP
from pathlib import Path

from Data.DataReader import DataReader
from model.Config import Config


class SourceLoader:
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
            logging.info(
                "ftp directory on server " + self.config.ftp_source_server + " now " + self.config.ftp_source_path)
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
        logging.info("found bills: " + len(result).__str__())
        return result

    def read_file(self, file_name: str):
        if self.ftp is None:
            return None

        self.ftp.cwd(self.config.ftp_source_path)
        logging.info(
            "ftp directory on server " + self.config.ftp_source_server + " now " + self.config.ftp_source_path)

        bill_id = file_name.replace("rechnung", "").replace(".data", "")
        local_dir = self.config.temp_output_path + "\\" + bill_id

        data_reader = DataReader()

        read_lines = self.ftp.retrlines("RETR " + file_name, callback=data_reader.handle_line)
        logging.info("downloading file " + file_name)

        if read_lines != "226 Transfer complete":
            logging.error("error reading data from file  " + self.config.ftp_source_path + "/" + file_name)
            return None

        result = []
        for bill in data_reader.list:
            if len(bill.positions) > 0:
                Path(local_dir).mkdir(parents=True, exist_ok=True)
                logging.info("creating directory " + local_dir)

                with open(local_dir + "/" + file_name, "wb") as file:
                    copy_file = self.ftp.retrbinary("RETR " + file_name, file.write)
                    logging.info("downloading file " + file_name)
                    if copy_file != "226 Transfer complete":
                        logging.error("error downloading file " + self.config.ftp_source_path + "/" + file_name)
                        return None

                data_file = "rechnung" + bill.bill_id.__str__() + ".data"
                logging.info("deleting file from " + self.config.ftp_source_server + " with name " + data_file)
                self.ftp.delete(data_file)
                result.append(bill)

        logging.info("found " + len(data_reader.list).__str__() + " bills.")
        return result

    def upload_zip_and_delete_files(self):
        self.ftp.cwd(self.config.ftp_source_path_in)
        logging.info(
            "ftp directory on server " + self.config.ftp_source_server + " now " + self.config.ftp_source_path_in)
        for path in os.scandir(self.config.temp_output_path):
            zip_name = ""
            for file_name in os.listdir(path):
                if file_name.endswith(".zip"):
                    zip_name = file_name
                    break

            if zip_name == "":
                continue

            with open(os.path.join(path, zip_name), "rb") as file_txt:
                self.ftp.storbinary("STOR %s" % zip_name, file_txt)
                logging.info("saving zip file to ftp server " + self.config.ftp_source_server + ": " + zip_name)

            for f in os.listdir(path):
                os.remove(os.path.join(path, f))
            os.rmdir(path)
            logging.info("deleting directory " + path.name)

        pass
