from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import hashlib
import copy
import json
import binascii

class Transaction:

    def __init__(self, sender_address, sender_private_key, recipient_address, value, senderID = 0, receiverID = 0, genesis = False, inputs = [], outputs =[]):
        self.sender_address = sender_address;
        self.receiver_address = recipient_address;
        self.amount = value;
        self.transaction_outputs = outputs;
        self.transaction_inputs = inputs;
        self.transaction_id = self.myHash();
        if genesis:
            self.transaction_outputs = [{'id': receiverID, 'tid':self.transaction_id, 'amount':value}]
        else:
            self.outputUTXOS(receiverID, senderID);
        if (sender_address == '0'):
            self.signature = None;
        else:
            self.signature = self.sign_transaction(sender_private_key);
            


    def myHash(self):
        # calculating the hash value of the transaction
        string = json.dumps(self.to_dict());
        string = string.encode();
        return hashlib.sha256(string).hexdigest();


    def outputUTXOS(self, receiverID, senderID):
        # calculating the transaction outputs
        mysum = 0;
        temp = [];
        for utxo in self.transaction_inputs:
            mysum += utxo['amount'];
        if mysum - self.amount > 0:
            temp.append({'id': str(senderID), 'tid': self.transaction_id, 'amount': mysum - self.amount})
        temp.append({'id': str(receiverID), 'tid': self.transaction_id, 'amount': self.amount})
        self.transaction_outputs = temp;
        
    def add_utxos(self, utxos):
        # adding the transaction inputs for this transaction
        self.transaction_inputs = utxos;
        
    def to_dict(self):
        # return a dictionary representation of the object
        return copy.deepcopy(self.__dict__)

    def sign_transaction(self, keyBytes):
        # signing the transaction with the private key given in __init__
        key = RSA.importKey(binascii.unhexlify(keyBytes))
        message = self.to_dict();
        string = json.dumps(message)
        string = string.encode()
        h = SHA.new(string);
        signer = PKCS1_v1_5.new(key);
        signature = signer.sign(h);
        return binascii.hexlify(signature).decode();
        
