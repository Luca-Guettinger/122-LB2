import json
import logging
import sys
from types import SimpleNamespace

from Data.OutputLoader import OutputLoader
from Data.SourceLoader import DataLoader
from Generator.MailSender import MailSender
from Generator.TxtGenerator import TxtGenerator
from Generator.XmlGenerator import XmlGenerator
from model.Config import Config

if __name__ == '__main__':
    log_path = "lb2.log"
    config: Config

    if len(sys.argv) != 2:
        logging.basicConfig(filename=log_path, encoding='utf-8', level=logging.DEBUG)
        logging.error("no valid start parameter found: config path needed!")
        exit(-1)

    try:
        config_path = sys.argv[1]
        with open(config_path) as config_file:
            config = json.load(config_file, object_hook=lambda d: SimpleNamespace(**d))
    except:
        logging.basicConfig(filename=log_path, encoding='utf-8', level=logging.DEBUG)
        logging.error("could not load JSON file: " + config_path)
        exit(-1)

    logging.basicConfig(filename=config.log_path, encoding='utf-8', level=logging.DEBUG)

    dataLoader = DataLoader(config)
    data = dataLoader.load_data()

    xml_generator = XmlGenerator(config)
    xml_generator.write_bills(data)

    txt_generator = TxtGenerator(config)
    txt_generator.write_bills(bills=data)

    output_load = OutputLoader(config)
    output_load.copy_files()