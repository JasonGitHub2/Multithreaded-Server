#import socket module
from socket import *
import threading
import sys # In order to terminate the program

#for threading, and connection is recieved
def threadConnection(threadSocket,threadAddress):
    #print('Threaded new connection.\n\n')
    try:
        message = threadSocket.recv(1024)
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        #Send one HTTP header line into socket
        #send the Http header which is formatted as 200 OK 
        threadSocket.send(bytes("HTTP/1.1 200 OK\r\n\r\n","UTF-8"))
        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            threadSocket.send(outputdata[i].encode())
        threadSocket.send("\r\n".encode())
        threadSocket.close()
        
    except IOError:
        #Send response message for file not found
        #send error message
        file='errorPage.html'
        openFile=open(file)
        data=openFile.read()
        threadSocket.send(bytes("HTTP/1.1 200 OK\r\n\r\n","UTF-8"))
        for i in range(0, len(data)):
            threadSocket.send(data[i].encode())
        threadSocket.send("\r\n".encode())
        
        threadSocket.close()
        


serverSocket = socket(AF_INET, SOCK_STREAM)

#Prepare a sever socket
#create a port and bind socket to port and listen
port=3100
serverSocket.bind(('',port))
serverSocket.listen(1)



while True:
    #Establish the connection
    print('Ready to serve...')
    #serverSocket.listen(1)
    #when we recieve connection with accept, call threading on it.
    connectionSocket, addr = serverSocket.accept()
    childThread=threading.Thread(target=threadConnection, args=(connectionSocket,addr));
    #print('Connection recieved, attempting to create new thread.')
    childThread.start()
    
serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data


