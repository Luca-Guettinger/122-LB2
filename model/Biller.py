class Biller:

    def __init__(
            self,
            party_id,
            client_id,
            name,
            street,
            zip,
            company_id,
            mail
    ):
        self.party_id = party_id
        self.client_id = client_id
        self.name = name
        self.street = street
        self.zip = zip
        self.company_id = company_id
        self.mail = mail

    def __repr__(self):
        return \
               f'Party_id: {self.party_id};\n' \
               f'Client_id: {self.client_id};\n' \
               f'Name: {self.name};\n' \
               f'Street: {self.street};\n' \
               f'Zip: {self.zip};\n' \
               f'Company_id: {self.company_id};\n' \
               f'Mail: {self.mail};\n'

    def __str__(self):
        return \
               f'Party_id: {self.party_id};\n' \
               f'Client_id: {self.client_id};\n' \
               f'Name: {self.name};\n' \
               f'Street: {self.street};\n' \
               f'Zip: {self.zip};\n' \
               f'Company_id: {self.company_id};\n' \
               f'Mail: {self.mail};\n'
