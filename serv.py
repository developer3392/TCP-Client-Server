import socket
import commands
import sys
import os

from sendreceive import *
from message import *

# Only accepts arguments no less than 2
if len(sys.argv) < 2:
	print "USAGE python " + sys.argv[0] + " <PORT NUMBER>" 
	sys.exit()


# The port number of the server
port = int(sys.argv[1])

# Creates the server socket and binds it to the port number
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(("", port))

# Listens for clients
print "Listening for clients..."

serverSocket.listen(1)

# Loops continuously for new potential clients
while (1):

    # Creates a connection socket
    connectionSocket, addr = serverSocket.accept()

    # A new socket has been found
    print "New client connected!"

    # Loops until the server receives "quit" to terminate client connection
    while(1):

        # Receives the client's command
        reqCommand = recvMessage(connectionSocket)
        print "Client> %s" %(reqCommand)

        # Server creates a ephemeral socket
        ephemeralSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Binds the ephemeral socket to port number 0
        ephemeralSocket.bind(('',0))

        # Listens for a connection
        ephemeralSocket.listen(1)

        # Converts the ephemeral port to a string
        ephemeralPort = str(ephemeralSocket.getsockname()[1])

        # Sends the ephemeral port to the client
        sendMessage(connectionSocket, ephemeralPort)

        # Accepts the connection and get's the client's data socket
        dataSocket, dataAddr = ephemeralSocket.accept()
        
        # If the command is "quit" it terminates the session with client
        if (reqCommand == "quit"):
            connectionSocket.close()
            print "Connection has been closed with client"
            print "Waiting on new connection..."
            break

        # If "ls" then the the output of the ls is acquired and sent to client
        elif (reqCommand == "ls"):
            output = str(commands.getoutput('ls -l'))
            sendMessage(dataSocket, output)

        # Otherwise the command is either a get or put, along with specified file name
        else:

            # Splits get/put command from filename
            string = reqCommand.split(" ", 1)
            if(string[0] == "get" or string[0] == "put"):

                reqFile = string[1] 

                # If the command is "put" then the server receives the data file
                if (string[0] == "put"):
                    recvFile(reqFile, dataSocket)
                    print "Received Successful"

                # If the command is "get" then the server opens the file and sends
                # the data file to the client  
                elif (string[0] == "get"):
                    sendFile(reqFile, dataSocket)
                    print "Send Successful"
                
        dataSocket.close()