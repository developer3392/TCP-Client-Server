import socket
import os
import commands
import sys

# Sends the data to the destination
def sendAll(socket, data):
    
    bytesSent = 0
    
    # Loops until the all the data is sent
    while len(data) > bytesSent:
		bytesSent += socket.send(data[bytesSent:])


# Receives all the data from the sender
def recvAll(sock, numBytes):

    # Buffers used for the function
    recvBuff = ""
    tmpBuff = ""

    # Loops until all the data is received
    while len(recvBuff) < numBytes:

        # Temp Buffer acquires the amount of data
        # specified by the number of byes
        tmpBuff = sock.recv(numBytes)

        # Breaks if the connection is lost
        if not tmpBuff:
            break

        # Temp buffer is added to the received buffer
        recvBuff += tmpBuff

    # Returns all the data
    return recvBuff