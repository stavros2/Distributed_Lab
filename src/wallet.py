from Crypto.PublicKey import RSA
import binascii

class wallet:
    def __init__(self):
        # create an RSA key pair
        self.transactions = [];
        temp = RSA.generate(2048)
        self.private_key = binascii.hexlify(temp.exportKey()).decode();
        self.public_key = binascii.hexlify(temp.publickey().exportKey()).decode();
        self.address = self.public_key;

    def balance(self):
        # return the balance of the wallet by adding all the available UTXO's
        sum = 0;
        for transaction in self.transactions:
            sum += transaction['amount'];
        return sum;