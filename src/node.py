import block
import wallet
import constants
import blockchain
import requests
import transaction

from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import binascii
import hashlib
import copy
import json
import threading
from time import sleep


class node:
    def __init__(self, myIp, myPort, imeBootstrap, ipBootstrap, portBootstrap, N):
        self.otherNodeMined = threading.Event();
        self.otherNodeMined.clear();
        self.mining = False;
        self.letsMine = threading.Thread(target = self.dummy);
        self.ip = myIp;
        self.port = myPort;
        self.ipBootstrap = ipBootstrap;
        self.portBootstrap = portBootstrap;
        self.number = N;
        self.myWallet = self.create_wallet()
        self.current_id_count = 1;
        
        if imeBootstrap:
            self.id = 0;
            self.chain = blockchain.blockchain();
            self.ring = dict();
            genesis = block.Block(1, 0);
            genesisTransaction = transaction.Transaction('0', '0', self.myWallet.address, N * 100, receiverID = '0', genesis = True);
            genesis.add_transaction(genesisTransaction);
            genesisUTXO = genesisTransaction.transaction_outputs[0]
            self.myWallet.transactions.append(genesisUTXO)
            tempDict = dict();
            tempDict['ip'] = self.ip;
            tempDict['port'] = self.port;
            tempDict['address'] = self.myWallet.address;
            tempDict['utxos'] = [genesisUTXO];
            self.ring['0'] = tempDict;
            self.chain.add_block(genesis);
            self.currentBlock = self.create_new_block()
            
        else:
            url = "http://" + ipBootstrap + ":" + str(portBootstrap) + "/registerNewNode"
            requestData = '{"ip":"' + myIp + '", "port":' + str(myPort) + ', "address":"' + str(self.myWallet.address) +'"}';
            response = requests.post(url, data = requestData);
            responseDict = json.loads(response.json());
            self.id = responseDict['id'];
            self.chain = self.reconstructChain(responseDict['chain']);
            self.ring = json.loads(responseDict['ring'])
            self.currentBlock = self.create_new_block()

    def verify_transaction(self, trans):
        transDict = trans.to_dict();
        transDict.pop('signature');
        transString = json.dumps(transDict);
        transString = transString.encode();
        hTrans = SHA.new(transString);
        verifier = PKCS1_v1_5.new(RSA.importKey(binascii.unhexlify(trans.sender_address)));
        return verifier.verify(hTrans, binascii.unhexlify(trans.signature))
        
        
    def create_new_block(self):
        #create a new block based on the last one of the chain
        newBlock = block.Block(self.chain.listOfBlocks[self.chain.length - 1].current_hash, self.chain.listOfBlocks[self.chain.length - 1].index);
        return newBlock;

    def create_wallet(self):
		#create a wallet for this node, with a public key and a private key
        new_wallet = wallet.wallet();
        return new_wallet;
    
    def validate_transaction(self, trans):
		 #verification of signature and enough NBC's
         asked = '0';
         for k in self.ring:
             if self.ring[k]['address'] == trans.sender_address:
                 asked = k;
         
         askedBalance = 0;
         
         for utxo in self.ring[asked]['utxos']:
             askedBalance += utxo['amount'];
             
         if not self.verify_transaction(trans):
             print("not a valid signature");
             return False;
         elif askedBalance < trans.amount:
             print("not enough NBC's");
             return True;
         else:
             return True;
         
    def dummy(self, receiver, amount):
        sleep(3)
        self.create_transaction(receiver, 100)
    
    def register_node_to_ring(self, newNodeIp, newNodePort, newNodeAddress):
		#add this node to the ring, only the bootstrap node can add a node to the ring after checking his wallet and ip:port address
		#bottstrap node informs all other nodes and gives the request node an id and 100 NBCs
        if self.current_id_count == self.number:
            return("{message: ring full}");
        
        tempDict = dict();
        tempDict['ip'] = newNodeIp;
        tempDict['port'] =  newNodePort;
        tempDict['address'] = newNodeAddress;
        tempDict['utxos'] = [];
        self.ring[str(self.current_id_count)] = tempDict;
        
        message = {'id': self.current_id_count, 'chain': self.chain.to_json(), 'ring': json.dumps(self.ring)};
        message = json.dumps(message);
        
        crT = threading.Thread(target=self.dummy, args = (self.current_id_count, 100, ))
        crT.start();
        #self.create_transaction(self.current_id_count, 100);
        self.current_id_count += 1;
        return message;
        
    
    def reconstructChain(self, chainJson):
        #input is a dictionary. outputs a Blockchain Object
        chainDict = json.loads(chainJson);
        newL = chainDict['length'];
        newList = chainDict['listOfBlocks']
        temp = [];
        
        for blockStr in newList:
            blockDict = json.loads(blockStr)
            tempBlock = self.reconstructBlock(blockDict);
            temp.append(tempBlock);
                
        return blockchain.blockchain(newL, temp)
    
    def reconstructBlock(self, blockDict):
        #input is a dictionary. outputs a Block Object
        tempBlock = block.Block();
        tempBlock.current_hash = blockDict['current_hash'];
        tempBlock.index = blockDict['index'];
        tempBlock.nonce = blockDict['nonce'];
        tempBlock.previous_hash = blockDict['previous_hash'];
        tempBlock.timestamp = blockDict['timestamp'];
        tempBlock.listOfTransactions = [];
        for transDict in blockDict['listOfTransactions']:
            tempTrans = self.reconstructTrans(transDict);
            tempBlock.listOfTransactions.append(tempTrans)
        return tempBlock;
    
    def reconstructTrans(self, transDict):
        #input is a dictionary. outputs a Transaction Object
        tempTrans = transaction.Transaction('0', '0', self.myWallet.address, 0);
        tempTrans.amount = transDict['amount'];
        tempTrans.receiver_address = transDict['receiver_address'];
        tempTrans.sender_address = transDict['sender_address'];
        tempTrans.signature = transDict['signature'];
        tempTrans.transaction_id = transDict['transaction_id'];
        tempTrans.transaction_inputs = transDict['transaction_inputs'];
        tempTrans.transaction_outputs = transDict['transaction_outputs'];
        return tempTrans;
        
    def create_transaction(self, receiver, amount):
		#remember to broadcast it
        #REMEMBER TO ADD UTXOS
        inputUTXOS = [];
        outputUTXOS = [];
        myAmount = 0;
        for utxo in self.myWallet.transactions:
            myAmount += utxo['amount'];
            inputUTXOS.append(utxo);
            if myAmount >= amount:
                break;
        
        for utxo in inputUTXOS:
            self.myWallet.transactions.remove(utxo);
        
        
        newTrans = transaction.Transaction(self.myWallet.address, self.myWallet.private_key, self.ring[str(receiver)]['address'], amount, receiverID = str(receiver), senderID = str(self.id), inputs = inputUTXOS);
        outputUTXOS = newTrans.transaction_outputs;
        print(newTrans);
        print(outputUTXOS)
        for utxo in outputUTXOS:
            self.ring[utxo['id']]['utxos'].append(utxo);
            if utxo['id'] == str(self.id):
                
                self.myWallet.transactions.append(utxo);
        
        self.broadcast_transaction(newTrans);
        self.currentBlock.add_transaction(newTrans);
        if len(self.currentBlock.listOfTransactions) == constants.CAPACITY:
            self.mine_block();
            
    def broadcast_transaction(self, trans):
        for k in self.ring:
            if k != str(self.id):
                url = "http://" + self.ring[k]['ip'] + ":" + str(self.ring[k]['port']) +"/receiveTransaction";
                requestData = json.dumps(trans.to_dict());
                requests.post(url, data = requestData);
                
                
    def add_transaction_to_block(self, transDict):
		#if enough transactions  mine
        newTrans = self.reconstructTrans(transDict);
        print(newTrans);
        print(newTrans.transaction_outputs)
        if self.validate_transaction(newTrans):
            self.currentBlock.add_transaction(newTrans);
            for utxo in newTrans.transaction_inputs:
                self.ring[utxo['id']]['utxos'].remove(utxo);
            for utxo in newTrans.transaction_outputs:
                self.ring[utxo['id']]['utxos'].append(utxo);
                if utxo['id'] == str(self.id):
                    self.myWallet.transactions.append(utxo)
        if len(self.currentBlock.listOfTransactions) == constants.CAPACITY:
            self.mine_block();
            
            
    def mine_block(self):
        self.mining = True;
        self.otherNodeMined.clear();
        while self.currentBlock.current_hash[:constants.MINING_DIFFICULTY] != '0' * constants.MINING_DIFFICULTY and not self.otherNodeMined.is_set():
            self.currentBlock.nonce +=1;
            self.currentBlock.current_hash = self.currentBlock.myHash();
        self.mining = False;
        if not self.otherNodeMined.is_set():
            self.chain.add_block(self.currentBlock)
            self.broadcast_block();
            self.currentBlock = self.create_new_block();
        
    
    
    def broadcast_block(self):
        for k in self.ring:
            if k != self.id:
                url = "http://" + self.ring[k]['ip'] + ":" + str(self.ring[k]['port']) +"/receiveBlock";
                requestData = self.currentBlock.to_json();
                requests.post(url, data = requestData);
    
    
    def valid_proof(self, blockToCheck):
        return blockToCheck.current_hash[:constants.MINING_DIFFICULTY] == '0' * constants.MINING_DIFFICULTY and blockToCheck.previous_hash == self.chain.lastBlock().current_hash;


	#concencus functions

#	def valid_chain(self, chain):
		#check for the longer chain accroose all nodes


#	def resolve_conflicts(self):
		#resolve correct chain



