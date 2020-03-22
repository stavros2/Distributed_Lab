#import blockchain
from time import time;
import hashlib
import json
import copy;
import transaction;

class Block:
    def __init__(self, previousHash = 0 , prevIndex = 0, creator = 0):
        self.creator = creator;
        self.previous_hash = previousHash;
        self.timestamp = time();
        self.index = prevIndex + 1;
        self.listOfTransactions = [];
        self.nonce = 0;
        self.current_hash = 0; # dummy value in order for myHash() to execute properly 
        self.current_hash = self.myHash();
        
    def myHash(self):
        # calculating the hash value of the block
        blockDict = copy.deepcopy(self.__dict__);
        blockDict.pop('current_hash');
        string = json.dumps(blockDict, default = transaction.Transaction.to_dict);
        string = string.encode();
        return hashlib.sha256(string).hexdigest();
        
    def add_transaction(self, transaction):
        # adding a transaction to the block
        self.listOfTransactions.append(transaction);
        self.current_hash = self.myHash();
        
    def to_json(self):
        #create a json representation of the block object. 
        blockDict = copy.deepcopy(self.__dict__);
        string = json.dumps(blockDict, default = transaction.Transaction.to_dict);
        return string