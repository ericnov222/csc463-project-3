'''
Created on Oct 24, 2017

@author: wuh2
This program is a simple peer-to-peer instance massage software.
It plays as both server and client.
To use the software:
python TCPtalk.py client_IPAddr clientPort ownPort

Example 1:
If you want to run the program on only one machine
You start your first application by using the following command:
python TCPtalk.py localhost 12001 12002

Then you start your second application:
python TCPtalk.py localhost 12002 12001

Example 2:
If you want to run the program on two machines with different ip addresses:
Suppose the two machines have ip addresses of 192.168.56.101 and 192.168.56.102, respectively
Start the program on first machine:
python TCPtalk.py 192.168.56.102 12000 12000

Start the program on second machine:
python TCPtalk.py 192.168.56.101 12000 12000
'''
from socket import *
import threading
import sys

CURSOR_UP_ONE = '\x1b[1A' # move the cursor to previous line on the screen
ERASE_LINE = '\x1b[2K'    # erase the content of the line on the screen

class Talk:
    '''
        This is the constructor of the class Talk,
        gets the ip and port information from user.
    '''
    def __init__(self, clientIP, clientPort, ownPort):
        self.clientIP=clientIP
        self.clientPort=clientPort
        self.ownPort=ownPort
        self.terminate=False

    '''
    This function performs as a server, keep receiving the information
    and output to the screen
    '''
    def startServer(self):
        serverSocket=socket(AF_INET,SOCK_STREAM)
        serverSocket.bind(('',self.ownPort))
        serverSocket.listen(1)
        print("server ready!")
        while not self.terminate:
            try:
                connectionSocket,addr=serverSocket.accept()
                msg=connectionSocket.recv(1024).decode()
                if msg.upper()=='QUIT':
                    self.terminate=True;
                print(addr[0]+"> "+msg)
                connectionSocket.close()
            except:
                break
    '''
    This function performs as a client, gets user input and sends message
    '''
    def sendMsg(self):
        print("client ready")
        while not self.terminate:
            try:
                #msg=raw_input() #python 2.7 version input
                msg=input() #python 3.x version input
                # print out the user input on the screen and overwrites the previous line
                print(CURSOR_UP_ONE+ERASE_LINE+"me> "+msg) 
                sys.stdout.flush()
                clientSocket=socket(AF_INET,SOCK_STREAM)
                clientSocket.connect((self.clientIP,self.clientPort))
                clientSocket.send(msg.encode())
                clientSocket.close()
                if msg.upper()=='QUIT':
                    self.terminate=True
            except:
                break
    
    '''
    This function runs both server and client functions as threads, so your
    application can receive and send message at the same time.
    '''
    def run(self):
        t1 = threading.Thread(target=self.startServer)
        t2 = threading.Thread(target=self.sendMsg)
        t1.start()
        t2.start()

'''
The main function takes three arguments: clientIP, clientPort, and ownIP
'''
def main(argv):
    clientIP=argv[1]
    clientPort=int(argv[2])
    ownPort=int(argv[3])
    print("start")
    t1=Talk(clientIP, clientPort, ownPort)
    t1.run()
    
main(sys.argv)
