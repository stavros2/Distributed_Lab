import threading;
import time;
import random;
import requests;
import json;


NODES = 10;

reqList = [];

def dummy(filename, port):
    f = open(filename, "r");
    f1 = f.readlines();
    for line in f1:
        args = line.split();
        requestData = '{"id": "' + args[0] + '", "amount":' + args[1] + '}';
        url =  "http://127.0.0.1:" + str(port) + "/newTransaction";
        reqList.append((url, requestData));
        
    return;

if __name__ == '__main__':
    startTimestamp = time.time();
    threads = []
    transactions =0;
    for i in range(NODES):
        myF = 'transactions' + str(i) + '.txt';
        myP = 5000;
        myP += i;
        threads.append(threading.Thread(target = dummy, args = (myF,myP,)));
        
    for i in range(NODES):
        threads[i].start();
        
    for i in range(NODES):
        threads[i].join();
    
    random.shuffle(reqList);
    for request in reqList:
        response = requests.post(request[0], data = request[1]);
        if response.status_code == 200:
            transactions += 1;
        time.sleep(0.2);
    
    endTimestamp = time.time();
    xronos = endTimestamp - startTimestamp;
    throughput = transactions / xronos;
    print("All transactions done in %d seconds" %xronos )
    print("Throughput %f" %throughput)
    response = requests.get("http://127.0.0.1:5000/printChain");
    responseDict = json.loads(response.json());
    noBlocks = int(responseDict['length']) - 1;
    avgBlockTime = xronos / noBlocks;
    print("The average duration of block mining was %f seconds" %avgBlockTime);
    