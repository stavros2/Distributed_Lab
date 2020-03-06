import block
import wallet
import constants
import blockchain

from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import hashlib
import copy


class node:
    def __init__():
        self.NBC=100;
        self.chain = blockhain.blockchain();
		#self.chain
		#self.current_id_count
		#self.NBCs
        self.myWallet = self.create_wallet()

		#slef.ring[]   #here we store information for every node, as its id, its address (ip:port) its public key and its balance 

    def verify_transaction(trans):
        transDict = trans.to_dict();
        transDict.pop('signature');
        transString = str(transDict);
        transString = transString.encode();
        hTrans = SHA.new(transString);
        verifier = PKCS1_v1_5.new(RSA.importKey(trans.sender_address));
        return verifier.verify(hTrans, transString)
        
        
    def create_new_block(lastBlock):
        #create a new block based on the last one of the chain
        newBlock = block.Block(lastBlock.current_hash, lastBlock.index);
        return newBlock;

    def create_wallet():
		#create a wallet for this node, with a public key and a private key
        new_wallet = wallet.wallet();
        return new_wallet;

	def register_node_to_ring():
		#add this node to the ring, only the bootstrap node can add a node to the ring after checking his wallet and ip:port address
		#bottstrap node informs all other nodes and gives the request node an id and 100 NBCs


	def create_transaction(sender, receiver, signature):
		#remember to broadcast it


	def broadcast_transaction():





	def validdate_transaction():
		#use of signature and NBCs balance


	def add_transaction_to_block():
		#if enough transactions  mine



	def mine_block():



	def broadcast_block():


		

	def valid_proof(.., difficulty=MINING_DIFFICULTY):




	#concencus functions

	def valid_chain(self, chain):
		#check for the longer chain accroose all nodes


	def resolve_conflicts(self):
		#resolve correct chain



