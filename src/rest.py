from flask import Flask, jsonify, request
from flask_cors import CORS
from argparse import ArgumentParser
import json


import node
import constants;

thisNode = None;

app = Flask(__name__)
CORS(app)


#.......................................................................................



@app.route('/viewTransactions', methods=['GET'])
def viewTransactions():
    lastBlock = thisNode.chain.listOfBlocks[thisNode.chain.length - 1];
    text = ''; 
    for trans in lastBlock.listOfTransactions:
        #text += json.dumps(trans.to_dict())
        text += str(trans.transaction_id);
        text += ' ';
        text += str(trans.amount)
        text += ' ';
    response = {'transactions': text};
    return jsonify(response), 200;

@app.route('/newTransaction', methods=['POST'])
def newTranscation():
    requestData = request.data
    requestData = json.loads(requestData);
    nodeID = int(requestData['id'][2::]);
    amount = int(requestData['amount']);
    bal = thisNode.myWallet.balance();
    
    if bal < amount:
        response = {'message': 'Not enough money!'}
        return jsonify(response), 402
    
    if amount <= 0:
        response = {'message': 'Amount must be positive!'}
        return jsonify(response), 401
    
    if nodeID == thisNode.id:
        response = {'message': 'You cannot transfer money to yourself'}
        return jsonify(response), 401
    
    if thisNode.mining:
        response = {'message': 'You cannot make a transactions now as a block is still being mined!'}
        return jsonify(response), 502
    
    thisNode.create_transaction(nodeID, amount);
    print("Back to REST")
    response = {'message': ('Sending ' + str(amount) + ' to node ' + str(nodeID))};
    print("Everything OK")
    return jsonify(response), 200;

@app.route('/getBalance', methods=['GET'])
def getBalance():
    #balance = thisNode.myWallet.balance();
    #response = {'balance': balance};
    response = {}
    for nodeI in thisNode.ring:
        nodeBal = 0 ;
        for utxo in thisNode.ring[nodeI]['utxos']:
            nodeBal += utxo['amount'];
        response[nodeI] = nodeBal;
    response['maBalance'] = thisNode.myWallet.balance()
    return jsonify(response), 200

@app.route('/registerNewNode', methods=['POST'])
def registerNewNode():
    requestData = json.loads(request.data)
    nodeIp = requestData['ip'];
    nodePort = requestData['port'];
    nodeAddress = requestData['address'];
    response = thisNode.register_node_to_ring(nodeIp, nodePort, nodeAddress);
    return jsonify(response), 200

@app.route('/receiveTransaction', methods=['POST'])
def receiveTransaction():
    requestData = json.loads(request.data)
    thisNode.add_transaction_to_block(requestData);
    
    return '{"message": "transaction recieved!"}', 200;

@app.route('/receiveBlock', methods=['POST'])
def receiveBlock():
    requestData = json.loads(request.data)

    blockInCheck = thisNode.reconstructBlock(requestData)
    if thisNode.valid_proof(blockInCheck):
        thisNode.otherNodeMined.set();
        thisNode.chain.add_block(blockInCheck);
        thisNode.currentBlock = thisNode.create_new_block();
        print(thisNode.chain.length)
        return '{"message": "block received!"}', 200;

    return '{"message": "block wasnt right!"}', 402;

@app.route("/receiveNewNodeInfo", methods=['POST'])
def receiveNewNodeInfo():
    requestData = json.loads(request.data);
    nodeID = requestData.pop('id');
    thisNode.ring[nodeID] = requestData;
    
    return '{"message": "Node added to ring!"}', 200;

@app.route("/printBlock", methods=['GET'])
def printBlock():
    return jsonify(thisNode.currentBlock.to_json()), 200;

@app.route("/printChain", methods=['GET'])
def printChain():
    return jsonify(thisNode.chain.to_json()), 200;

# run it once fore every node

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-a', '--address', default = '127.0.0.1', help='public accessible ip address');
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    parser.add_argument('-b', '--bootstrap', action='store_true', help='is this the bootstrap node?')
    parser.add_argument('-l', '--bootstrapaddress', default = '127.0.0.1', help='public ip address of bootstrap')
    parser.add_argument('-m', '--bootstrapport', default = 5000, type = int, help='port bootstrap listens on')
    args = parser.parse_args()
    port = args.port
    isIt = args.bootstrap;
    address = args.address;
    bootstrapAddress = args.bootstrapaddress;
    bootstrapPort = args.bootstrapport
    thisNode = node.node(address, port, isIt, bootstrapAddress, bootstrapPort, constants.NODES);
    app.run(host='127.0.0.1', port=port, threaded= True)