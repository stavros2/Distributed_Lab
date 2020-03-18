import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS


import block
import node
import blockchain
import wallet
import transaction
import wallet
import constants;


### JUST A BASIC EXAMPLE OF A REST API WITH FLASK

thisNode = node.node();

app = Flask(__name__)
CORS(app)


#.......................................................................................



@app.route('/get_balance', methods=['GET'])
def get_balance():
    balance = thisNode.myWallet.balance();
    response = {'balance': balance};
    return jsonify(response), 200

# run it once fore every node

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-a', '--address', default = '127.0.0.1', help='public accessible ip address');
    parser.add_argument('-p', '--port', default=5001, type=int, help='port to listen on')
    parser.add_argument('-b', '--bootstrap', action='store_true', help='is this the bootstrap node?')
    args = parser.parse_args()
    port = args.port
    isIt = args.bootstrap;
    address = args.address;
    thisNode = node.node(address, port, isIt, '127.0.0.1', '5000', constants.NODES);
    print(type(address));
    print(address)
    app.run(host='127.0.0.1', port=port)