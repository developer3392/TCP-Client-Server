import socket
import os
import commands
import sys

from instructions import *
from sendreceive import *
from message import *

# Only accepts arguments no less than 3
if len(sys.argv) < 3:
	print "USAGE python " + sys.argv[0] + " <SERVER HOST> <PORT NUMBER>" 
	sys.exit()

 #Takes the arguments of the terminal for the host and port
serverHost = sys.argv[1]
serverPort = int(sys.argv[2])

# Creates a client socket and connects to the server
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverHost,serverPort))

# The server has connected and the session beings
print "Connection succesful!"

# If the client specifies an "lls" command, the
# method outputs the contents of the 'ls -l' command
def lls_command():

    for line in commands.getstatusoutput('ls -l'):
	    print line

    return

# Gets the print instructions method
print_instructions()

# Loops continuously until the client specifies "quit" as a command
while(1):

    # Prints ftp> 
    msg = "ftp"
    sys.stdout.write('%s> ' % msg)

    # Gets the input command from the user
    inputCommand = sys.stdin.readline().strip()

    # Sends the input command to the server
    sendMessage(clientSocket, inputCommand)

    # Data port number of the ephemeral port is received
    dataPortNum = int(recvMessage(clientSocket))    

    # A data socket is created
    dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # The data socket then connects to the port number of the server
    dataSocket.connect((serverHost, dataPortNum))

    # Terminates session if "quit" is input
    if (inputCommand == 'quit'):
        clientSocket.close()
        break

    # Acquires the ls from the server side and prints it out
    elif (inputCommand == 'ls'):
        output = recvMessage(dataSocket)
        print output

    # Runs ls and list files on client's directory
    elif (inputCommand == 'lls'):
        lls_command()

    # Otherwise, the command is either get/put or something else
    else:
        # Splits get/put command from the file name
        string = inputCommand.split(' ', 1)
        if(string[0] == "get" or string[0] == "put"):
            reqFile = string[1] 


            # If "put" is input, sends file data to server
            if (string[0] == 'put'):
                sendFile(reqFile, dataSocket)


            # If "get" is input, the client downloads file from server
            elif (string[0] == 'get'):
                recvFile(reqFile, dataSocket)
        else:
            print "Incorrect input! Please enter another command."

    dataSocket.close()

