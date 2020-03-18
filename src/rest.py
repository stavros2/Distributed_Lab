import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from argparse import ArgumentParser
import json


import block
import node
import blockchain
import wallet
import transaction
import wallet
import constants;


### JUST A BASIC EXAMPLE OF A REST API WITH FLASK

thisNode = node.node(None, None, None, None, None, None);

app = Flask(__name__)
CORS(app)


#.......................................................................................



@app.route('/viewTransactions', methods=['GET'])
def viewTransactions():
    response = {'transactions': 'working on it...' };
    return jsonify(response), 200;

@app.route('/newTransaction', methods=['POST'])
def newTranscation():
    requestData = request.data
    requestData = json.loads(requestData);
    nodeID = requestData['id'];
    amount = requestData['amount'];
    response = {'id': nodeID, 'amount': amount };
    return jsonify(response), 200;

@app.route('/getBalance', methods=['GET'])
def getBalance():
    balance = thisNode.myWallet.balance();
    response = {'balance': balance};
    return jsonify(response), 200

# run it once fore every node

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-a', '--address', default = '127.0.0.1', help='public accessible ip address');
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    parser.add_argument('-b', '--bootstrap', action='store_true', help='is this the bootstrap node?')
    args = parser.parse_args()
    port = args.port
    isIt = args.bootstrap;
    address = args.address;
    thisNode = node.node(address, port, isIt, '127.0.0.1', '5000', constants.NODES);
    app.run(host='127.0.0.1', port=port)