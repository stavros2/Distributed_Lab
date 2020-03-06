import binascii

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4


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