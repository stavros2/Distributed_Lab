from argparse import ArgumentParser
import requests; 
import os;
import signal;

def printNewLine():
    print("--------------------------------------------");

def terminating(sig, frame):
    exit()

signal.signal(signal.SIGINT, terminating);

def printHelp():
    print("You can select one of the following commands");
    printNewLine();
    print("t <node id> <amount>: To create a new transaction of amount @amount from you to user with id @id");
    print("view: To view all transactions registered in the last valid block")
    print("balance: To view the amount of noobcash coins left in your account")
    print("help: To view this message again")
    print("clear: To clear the window")
    print("exit: To close the Noobcash CLIent")
    
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args();
    port = args.port;
    baseURL =  "http://127.0.0.1:" + str(port) + "/"
    
    print("Welcome to the Noobcash CLIent");
    printHelp()
    while(1):
        printNewLine();
        print("Give a command");
        printNewLine();
        wholeLine = input();
        printNewLine();
        splitLine = wholeLine.split(' ');
        command = splitLine[0];
        args = splitLine[1::];
        
        if command.lower() == 't':
            if len(args) != 2:
                print("Sorry, this command takes 2 arguments.")
                print("If you are not sure about usage of this command type help and read the CLI manual");
                continue;
            requestData = '{"id": "' + args[0] + '", "amount":' + args[1] + '}';
            url = baseURL + "newTransaction";
            response = requests.post(url, data = requestData);
            print(response.json())
        
        elif command.lower() == 'view':
            url = baseURL + "viewTransactions"
            response = requests.get(url);
            print(response.json())
        
        elif command.lower() == 'balance':
            url = baseURL + "getBalance";
            response = requests.get(url);
            print(response.json())
        
        elif command.lower() == 'help':
            printHelp();
            
        elif command.lower() == 'clear':
            if os.name == 'nt': 
                os.system('cls');
            else:
                os.system('clear');    
            
        elif command.lower() == 'exit':
            exit();
            
        else:
            print("Invalid command. Please give a valid command or type help to read the manual");    
        
        