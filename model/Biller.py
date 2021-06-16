class Biller:
    def __init__(
            self,
            client_id,
            name,
            street,
            zip,
            location,
            company_id,
            mail,
    ):
        self.client_id = client_id
        self.name = name
        self.street = street
        self.zip = zip
        self.location = location
        self.company_id = company_id
        self.mail = mail

    def __repr__(self):
        return f'Client_id: {self.client_id};\n' \
               f'Name: {self.name};\n' \
               f'Street: {self.street};\n' \
               f'Zip: {self.zip};\n' \
               f'Location: {self.location};\n' \
               f'Company_id: {self.company_id};\n' \
               f'Mail: {self.mail};'

    def __str__(self):
        return f'Client_id: {self.client_id};\n' \
               f'Name: {self.name};\n' \
               f'Street: {self.street};\n' \
               f'Zip: {self.zip};\n' \
               f'Location: {self.location};\n' \
               f'Company_id: {self.company_id};\n' \
               f'Mail: {self.mail};'
