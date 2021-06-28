import logging
import os
from ftplib import FTP

from model.Config import Config


class OutputLoader:
    ftp: FTP

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

    def copy_files(self):
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
                print(file_name)

                dir = self.config.temp_output_path + "\\" + file_name.split("_")[1] + "\\" + file_name
                with open(dir, "rb") as file:
                    self.ftp.storbinary("STOR %s" % file_name, file)

