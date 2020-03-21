from Crypto.PublicKey import RSA
import binascii

class wallet:
    def __init__(self):
        self.transactions = [];
        temp = RSA.generate(2048)
        self.private_key = binascii.hexlify(temp.exportKey()).decode();
        self.public_key = binascii.hexlify(temp.publickey().exportKey()).decode();
        self.address = self.public_key;

    def balance(self):
        sum = 0;
        for transaction in self.transactions:
            sum += transaction['amount'];
        return sum;