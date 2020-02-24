import block

class blockchain():
    def __init__(self):
        self.listOfBlocks = [];
        
        
    def add_block(self, blockItem):
        self.listOfBlocks.append(blockItem);
