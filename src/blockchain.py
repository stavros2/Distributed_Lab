import block;
import copy;
import json;

class blockchain():
    def __init__(self, myLength = 0, myList = []):
        self.listOfBlocks = myList;
        self.length = myLength;
        
        
    def add_block(self, blockItem):
        # add a block to the chain. Update length accordingly
        self.listOfBlocks.append(blockItem);
        self.length += 1;
        
    def to_json(self):
        # create a JSON message of the blockchain to be send
        blockchainDict = copy.deepcopy(self.__dict__);
        return json.dumps(blockchainDict, default = block.Block.to_json)
    
    def lastBlock(self):
        # return the last block of the chain
        return self.listOfBlocks[self.length - 1]