from Crypto.PublicKey import RSA

class wallet:
    def __init__(self):
        self.transactions = [];
        temp = RSA.generate(2048)
        self.private_key = temp.exportKey();
        self.public_key = temp.publickey().exportKey();
        self.address = self.public_key;

    def balance(self):
        sum = 0;
        for transaction in self.transactions:
            sum += transaction.amount;
        return sum;