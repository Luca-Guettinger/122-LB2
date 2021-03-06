class Client:
    def __init__(
            self,
            account_id,
            name,
            street,
            zip,
            location,
    ):
        self.account_id = account_id
        self.name = name
        self.street = street
        self.zip = zip
        self.location = location

    def __repr__(self):
        return f'Account_id: {self.account_id};\n' \
               f'Name: {self.name};\n' \
               f'Street: {self.street};\n' \
               f'Zip: {self.zip};\n' \
               f'Location: {self.location};'

    def __str__(self):
        return f'Account_id: {self.account_id};\n' \
               f'Name: {self.name};\n' \
               f'Street: {self.street};\n' \
               f'Zip: {self.zip};\n' \
               f'Location: {self.location};'
