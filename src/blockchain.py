import block

class blockchain():
    def __init__(self):
        self.listOfBlocks = [];
        self.length = 0;
        
        
    def add_block(self, blockItem):
        self.listOfBlocks.append(blockItem);
        self.length += 1;