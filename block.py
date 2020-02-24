#import blockchain
from time import time;
import hashlib
import json



class Block:
    def __init__(self, previousHash, prevIndex):
        self.previous_hash = previousHash;
        self.timestamp = time();
        self.index = prevIndex + 1;
        self.listOfTransactions = [];
        self.nonce = 0;
        self.current_hash = 0; # dummy value in order for myHash() to execute properly 
        self.current_hash = self.myHash();
        
    def myHash(self):
        # calculating the hash value of the block
        blockDict = self.__dict__;
        blockDict.pop('current_hash');
        string = json.dumps(blockDict);
        string = string.encode('utf-8');
        return hashlib.sha256(string).hexdigest();
		#calculate self.hash
        
    def add_transaction(self, transaction):
        # adding a transaction to the block
        self.listOfTransactions.append(transaction);