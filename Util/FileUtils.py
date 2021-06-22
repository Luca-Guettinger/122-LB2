import logging
from string import Template


def read_template(file: str):
    with open(file, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def write_to_file(content: str, file_path: str):
    try:
        logging.info("Writing to file {file_path}")
        file = open(file_path, 'w+', encoding='utf-8')
        file.write(content)
        file.close()
    except:
        logging.error("Couldn't write xml to file {file_path}")
