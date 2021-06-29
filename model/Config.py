class Config:
    log_path: str

    smtp_host: str
    smtp_port: int

    mail_password: str
    mail_username: str
    mail_template_path: str

    ftp_source_server: str
    ftp_source_username: str
    ftp_source_password: str
    ftp_source_path: str

    ftp_output_server: str
    ftp_output_username: str
    ftp_output_password: str
    ftp_output_path: str

    ftp_output_receipt_path: str

    temp_output_path: str

    xml_template_path: str
    txt_template_path: str
