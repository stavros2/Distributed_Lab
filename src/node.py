import block
import wallet
import json
import requests
import blockchain
import threading
import transaction

import binascii
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import sys
import threading
import time
from urllib.parse import urlparse
from uuid import uuid4
import copy
from flask import Flask, jsonify, request

no_mine = threading.Event()
no_mine.set()

class node():
    def __init__(self, bootstrap, number,port, ipbootstrap, ip_dikia_mou):
        self.port=port
        self.chain = blockchain.Blockchain()
        self.current_id_count = 0 #register_node_to_ring()
        self.wallet = wallet.wallet()
        #self.NBCs = self.wallet.balance()
        temp = "http://" + ipbootstrap + ":5000"
        self.ring = [temp]#here we store information for every node, as its id, its address (ip:port) its public key and its balance
        self.nei = number
        self.public_key_list = []
        self.myip = ip_dikia_mou

        if(bootstrap == "0"):
            self.public_key_list = [self.wallet.public_key]
            self.id = 0
            self.chain.create_genesis(number, self.public_key_list[0])
            #print("my chain list " , self.chain.list[0].output())
            self.wallet.add_genesis(self.chain.list[0].output())
            self.e = threading.Event()
            self.e.clear()
            t2 = threading.Thread( target = self.init)
            t2.start()
        else:
            self.my_reg()

    def init(self):
        self.e.wait()
        time.sleep(3)
        for i, a in enumerate(self.ring[1:]):
        	self.send(i+1, a)
        time.sleep(3)

        self.chain.get_addresses(self.ring, self.id)

        for i, a in enumerate(self.ring[1:]):
            self.wallet_dict={}
            for public_key in self.public_key_list:
                self.wallet_dict[public_key] = []
            if not no_mine.isSet():
                no_mine.wait()
            self.send_trans(i+1, a,self.public_key_list[i+1])
            #time.sleep(4)




    def send_trans(self,i, a,receiver_address):
        print("sending transaction to each node")
        self.create_transaction(self.public_key_list[0],receiver_address,100)
        print("my balance father", self.wallet.mybalance())
        return self




    def send(self,i, a):
        print("sending info to each node")

        """
        message = {'id': i, 'ring': self.ring,'public_key_list':self.public_key_list,'gen_index': self.chain.list[0].index,
                'gen_timestamp': self.chain.list[0].timestamp,
                'gen_transactions': self.chain.list[0].listOfTransactions,
                'gen_nonce': self.chain.list[0].nonce,
                'gen_previous_hash': self.chain.list[0].previousHash}
        """
        message = {'id': i, 'ring': self.ring,'public_key_list':self.public_key_list,'genesis':self.chain.list[0].output()}
        m = json.dumps(message)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        res=requests.post(a + '/nodes/register', data = m,headers = headers)
        print(res)
        return self

    def recieve(self, i, ring,keys,genesis):
        print("receiving info!")
        self.ring = copy.deepcopy(ring)
        self.id = i
        self.chain.get_addresses(self.ring, self.id)
        #print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        self.public_key_list = copy.deepcopy(keys)
        self.wallet_dict={}
        for public_key in self.public_key_list:
            self.wallet_dict[public_key] = []

        new = block.Block(genesis['index'], genesis['nonce'], genesis['previous_hash'])
        new.timestamp = genesis['timestamp']
        new.listOfTransactions = genesis['transactions']
        new.myHash()
        self.chain.list.append(new)
        mylist = new.listOfTransactions

        tr = mylist[0]
        print("transaction" , tr)

        t1 = {'myid': tr['transaction_id'], 'value' : tr['value'] , 'receiver' : tr['receiver_address']}
        self.wallet_dict[self.public_key_list[0]].append(t1)

        return self

    def my_reg(self):
    	message = {'address' : "http://" + self.myip + ":" + self.port ,'public_key':self.wallet.public_key}
    	r = requests.post(self.ring[0]+"/nodes/reg_dad", data = message)
    	return r

    def reg_a_node(self,a,mykey):
        self.ring.append(a)
        self.public_key_list.append(mykey)
        self.current_id_count = self.current_id_count + 1
        if(self.current_id_count == self.nei):
            self.e.set()
            print("geia xixi")


    def create_transaction(self, sender, receiver, amount):
        lista = self.wallet.transactions
        my_sum = 0
        utxo = []
        ids = []
        for i in range(0, len(lista)):
            my_sum = my_sum + lista[i]['value']
            utxo.append(lista[i]['myid'])
            ids.append(lista[i])
            if(my_sum >=amount):
                break
        if(my_sum < amount):
            print("not enough nbc")
            return
        for i in ids:
            #print(i)
            lista.remove(i)

        new = transaction.Transaction(sender, self.wallet.private_key, receiver, amount,copy.deepcopy(utxo))
        #print("i am the new transaction hi", new.transaction_id)
        t1 = {'myid': new.transaction_id, 'value' : amount , 'receiver' : receiver}
        new.transaction_outputs = [t1]

        if(my_sum>amount):
            t2 = {'myid': new.transaction_id, 'value' : my_sum - amount , 'receiver' : sender}
            new.transaction_outputs.append(t2)
            lista.append(t2)

        self.wallet.transactions = copy.deepcopy(lista)
        self.wallet_dict[receiver].append(new.transaction_outputs[0])
        self.wallet_dict[sender] = copy.deepcopy(lista)
        new.Signature = new.sign_transaction(self.wallet.private_key)
        self.broadcast_transaction(new)
        self.chain.add_transaction(new)




    def receive_trans(self,sender,receiver,value,myid,in_list,out_list,sign):

        new=transaction.Transaction(sender,"0" , receiver, value,in_list)

        new.transaction_outputs = out_list
        new.Signature = sign
        new.transaction_id=myid

        if self.validate_transaction(new,sender,sign):
            self.chain.add_transaction(new)
            mylist = self.wallet_dict[sender]
            for input_trans in new.transaction_inputs:
                for index,utxoid in enumerate(mylist):
                    if( input_trans==utxoid['myid']):
                        mylist.remove(mylist[index])

            self.wallet_dict[sender] = copy.deepcopy(mylist)
            self.wallet_dict[receiver].append(new.transaction_outputs[0])
            if(len(new.transaction_outputs)==2):
                self.wallet_dict[sender].append(new.transaction_outputs[1])

            if(receiver == self.wallet.public_key):
                self.wallet.transactions.append(new.transaction_outputs[0])
            print("my balance kid", self.wallet.mybalance())
        print(self.wallet.transactions)

        return



    def validate_transaction(self, trans,sender,sign):
        print("validating transaction...")
        mylist = self.wallet_dict[sender]
        cnt=0
        for input_trans in trans.transaction_inputs:
            for index,utxoid in enumerate(mylist):
                if  input_trans==utxoid['myid']:
                    cnt+=1

        if cnt==len(trans.transaction_inputs) and self.verify_transaction_signature(sender,sign,trans):
            print("Transaction validated")
            return True

        return False


    def verify_transaction_signature(self, sender_address, signature, transaction):
        """
        Check that the provided signature corresponds to transaction
        signed by the public key (sender_address)
        """
        public_key = RSA.importKey(binascii.unhexlify(sender_address))
        verifier = PKCS1_v1_5.new(public_key)
        temp = transaction.to_dict2()
        h = SHA.new(str(temp).encode('utf8'))
        print("verify_transaction_signature ",verifier.verify(h, binascii.unhexlify(signature)))
        return verifier.verify(h, binascii.unhexlify(signature))


    def broadcast_transaction(self,trans):
        print("Broadcast_transaction to all except me")
        message = { 'sender':trans.sender_address, 'receiver' : trans.receiver_address, 'value': trans.value, 'myid': trans.transaction_id, 'inputs':trans.transaction_inputs, 'outputs':trans.transaction_outputs, 'sign': trans.Signature}
        m = json.dumps(message)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        for rin in self.ring:
            if not(rin == self.ring[self.id]):
                requests.post(rin+"/transactions/new", data = m , headers=headers)
        return

    def verify_and_add_block(self, orderedInfoBlock):
        if not orderedInfoBlock['previous_hash'] == self.chain.list[-1].hash:
            return False
        else:
            new = block.Block(orderedInfoBlock['index'], orderedInfoBlock['nonce'], orderedInfoBlock['previous_hash'])
            new.timestamp = orderedInfoBlock['timestamp']
            new.listOfTransactions = orderedInfoBlock['transactions']
            if new.verify_hash(orderedInfoBlock['current_hash']):
                # have verified block, so we set this flag before we add it to our blockchain
                self.chain.e.set()

                self.chain.list.append(new)
                return True
            else:
                return False