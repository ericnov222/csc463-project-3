'''
Created on Oct 23, 2017

@author: wuh2
'''
from socket import *

serverName='127.0.0.1'
serverPort=12000
clientSocket=socket(AF_INET,SOCK_DGRAM)
message=raw_input('Input lowercase sentences:')
clientSocket.sendto(message.encode(),(serverName,serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()
