import logging

from DataRepository import DataRepository


if __name__ == '__main__':
    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
    dataRepo = DataRepository('ftp.haraldmueller.ch', 'schoolerinvoices', 'Berufsschule8005!', '/out/AP18dGuettinger')
    dataRepo.load_data('rechnung21003.data')
