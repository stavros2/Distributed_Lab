import block;
import copy;
import json;

class blockchain():
    def __init__(self, myLength = 0, myList = []):
        self.listOfBlocks = myList;
        self.length = myLength;
        
        
    def add_block(self, blockItem):
        self.listOfBlocks.append(blockItem);
        self.length += 1;
        
    def get_transactions(self):
        trans = [];
        for blockItem in self.listOfBlocks:
            for tran in blockItem.listOfTransactions:
                trans.append(tran);
        return trans;
    
    def to_json(self):
        blockchainDict = copy.deepcopy(self.__dict__);
        return json.dumps(blockchainDict, default = block.Block.to_json)
    
    def lastBlock(self):
        return self.listOfBlocks[self.length - 1]