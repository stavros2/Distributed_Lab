import Crypto
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import hashlib
import copy


class Transaction:

    def __init__(self, sender_address, sender_private_key, recipient_address, value, utxo):
        self.sender_address = sender_address;
        self.receiver_adress = recipient_address;
        self.amount = value;
        self.transaction_id = 0;
        self.transaction_outputs = [];
        self.transaction_inputs = utxo;
        self.transaction_id = self.myHash();
        self.signature = self.sign_transaction(sender_private_key);


    
    def myHash(self):
        # calculating the hash value of the transaction
        transDict = self.to_dict();
        transDict.pop('transaction_id');
        string = str(transDict);
        string = string.encode('utf-8');
        return hashlib.sha256(string).hexdigest();

    def to_dict(self):
        return copy.deepcopy(self.__dict__)

    def sign_transaction(self, keyBytes):
        """
        Sign transaction with private key
        """
        key = RSA.importKey(keyBytes)
        message = self.to_dict();
        string = str(message);
        string = string.encode('utf-8')
        h = SHA.new(string);
        signer = PKCS1_v1_5.new(key);
        signature = signer.sign(h);
        return signature;
    
        
       