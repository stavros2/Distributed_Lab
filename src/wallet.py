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
        self.private_key = RSA.generate(2048);
        self.public_key = self.private_key.publickey();
        self.address = self.public_key.exportKey();

    def balance(self):
        sum = 0;
        for transaction in self.transactions:
            sum += transaction.amount;
        return sum;

