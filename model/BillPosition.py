class BillPosition:
    def __init__(
            self,
            number,
            name,
            amount,
            price,
            total,
    ):
        self.number = number
        self.name = name
        self.amount = amount
        self.price = price
        self.total = total

    def __repr__(self):
        return f'Position: {self.number};\n' \
               f'Name: {self.name};\n' \
               f'Amount: {self.amount};\n' \
               f'Price: {self.price};\n' \
               f'Total: {self.total};'

    def __str__(self):
        return f'Position: {self.number};\n' \
               f'Name: {self.name};\n' \
               f'Amount: {self.amount};\n' \
               f'Price: {self.price};\n' \
               f'Total: {self.total};'
