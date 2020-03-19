import block
import wallet
import constants
import blockchain
import requests
import transaction

from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import hashlib
import copy
import json


class node:
    def __init__(self, myIp, myPort, imeBootstrap, ipBootstrap, portBootstrap, N):
        self.ip = myIp;
        self.port = myPort;
        self.ipBootstrap = ipBootstrap;
        self.portBootstrap = portBootstrap;
        self.number = N;
        self.myWallet = self.create_wallet()
        self.current_id_count = 0;
        
        if imeBootstrap:
            self.id = 0;
            self.chain = blockchain.blockchain();
            self.ring = dict();
            tempDict = dict();
            tempDict['id'] = 0;
            tempDict['ip'] = self.ip;
            tempDict['port'] = self.port;
            tempDict['address'] = self.myWallet.address;
            tempDict['utxos'] = [];
            self.ring[0] = tempDict;
            genesis = block.Block(1, 0);
            genesisTransaction = transaction.Transaction(0, 0, self.myWallet.address, N * 100);
            genesis.add_transaction(genesisTransaction);
            self.chain.add_block(genesis);
            self.currentBlock = block.Block(genesis.current_hash, genesis.index)
            
        else:
            url = "http://" + ipBootstrap + ":" + str(portBootstrap) + "/registerNewNode"
            requestData = '{"ip":' + myIp + ', "port":' + str(myPort) + ', "address":' + str(self.myWallet.address) +'}';
            response = requests.post(url, data = requestData);
            responseDict = json.loads(response.json());
            self.id = responseDict['id'];
            self.chain = responseDict['chain'];
            self.currentBlock = block.Block(self.chain[self.chain.length - 1].current_hash, self.chain[self.chain.length - 1].index)
            self.ring = dict();

    def verify_transaction(self, trans):
        transDict = trans.to_dict();
        transDict.pop('signature');
        transString = str(transDict);
        transString = transString.encode();
        hTrans = SHA.new(transString);
        verifier = PKCS1_v1_5.new(RSA.importKey(trans.sender_address));
        return verifier.verify(hTrans, trans.signature)
        
        
    def create_new_block(self, lastBlock):
        #create a new block based on the last one of the chain
        newBlock = block.Block(lastBlock.current_hash, lastBlock.index);
        return newBlock;

    def create_wallet(self):
		#create a wallet for this node, with a public key and a private key
        new_wallet = wallet.wallet();
        return new_wallet;
    
    def validate_transaction(self, trans):
		 #verification of signature and enough NBC's
         asked = 0;
         for k,v in self.ring:
             if v['address'] == trans.sender_address:
                 asked = k;
         
         askedBalance = 0;
         
         for utxo in self.ring[asked]['utxos']:
             askedBalance += utxo['amount'];
             
         if not self.verify_transaction(trans):
             print("not a valid signature");
             return False;
         elif askedBalance < trans.amount:
             print("not enough NBC's");
         else:
             return True;
         

   # def create_transaction(sender, receiver, signature):
		#remember to broadcast it

#	def register_node_to_ring():
		#add this node to the ring, only the bootstrap node can add a node to the ring after checking his wallet and ip:port address
		#bottstrap node informs all other nodes and gives the request node an id and 100 NBCs


	#def create_transaction(sender, receiver, signature):
		#remember to broadcast it


#	def broadcast_transaction():







#	def add_transaction_to_block():
		#if enough transactions  mine
        



#	def mine_block():



#	def broadcast_block():


		


#	def valid_proof(.., difficulty = constants.MINING_DIFFICULTY):




	#concencus functions

#	def valid_chain(self, chain):
		#check for the longer chain accroose all nodes


#	def resolve_conflicts(self):
		#resolve correct chain



