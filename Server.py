'''
Script for server
@author: hao
'''

import config
import protocol
import os
from socket import *
class server:

    # Constructor: load the server information from config file
    def __init__(self):
        self.port, self.path=config.config().readServerConfig()

    # Get the file names from shared directory
    def getFileList(self):
        return os.listdir(self.path)
    
    # Function to send file list to client       
    def listFile(self, serverSocket):
        serverSocket.send(protocol.prepareFileList(protocol.HEAD_LIST, self.getFileList()))

    # Function to send a file to client       
    def sendFile(self,serverSocket,fileName):
        f = open(fileName,'rb')
        l = f.read(1024) # each time we only send 1024 bytes of data
        while (l):
            serverSocket.send(l)
            l = f.read(1024)

    # Function to receive a file from the client
    def receiveFile(self, serverSocket, fileName):
        fileName = os.path.basename(fileName)
        filePath = os.path.join(self.path, fileName)

        with open(filePath, "wb") as f:
            serverSocket.sendall(b"OK")

            while True:
                data = serverSocket.recv(1024)
                if not data:
                    break
                f.write(data)

        serverSocket.sendall(b"OK")
        print(fileName + " has been uploaded!")
    # Main function of server, start the file sharing service
    def start(self):
        serverPort=self.port
        serverSocket=socket(AF_INET,SOCK_STREAM)
        serverSocket.bind(('',serverPort))
        serverSocket.listen(20)
        print('The server is ready to receive')

        while True:
            connectionSocket, addr = serverSocket.accept()
            dataRec = connectionSocket.recv(1024)
            header,msg=protocol.decodeMsg(dataRec.decode())

            if(header==protocol.HEAD_REQUEST):
                self.listFile(connectionSocket)
            elif(header==protocol.HEAD_DOWNLOAD):
                self.sendFile(connectionSocket, self.path+"/"+msg)
            elif(header==protocol.HEAD_UPLOAD):
                self.receiveFile(connectionSocket, msg)
            else:
                connectionSocket.send(protocol.prepareMsg(protocol.HEAD_ERROR, "Invalid Message"))

            connectionSocket.close()
def main():
    s=server()
    s.start()

if __name__ == "__main__":
    main()
