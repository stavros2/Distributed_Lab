class blockchain():
    def __init__(self):
        self.listOfBlocks = [];
        self.length = 0;
        
        
    def add_block(self, blockItem):
        self.listOfBlocks.append(blockItem);
        self.length += 1;
        
    def get_transactions(self):
        trans = [];
        for blockItem in self.listOfBlocks:
            for tran in blockItem.listOfTransactions:
                trans.append(tran);
        return trans;