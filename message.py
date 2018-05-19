import socket
import os
import commands
import sys

from sendreceive import *

# Sends message with data to the destination
def sendMessage(socket, data):

    # A string of the length of data
    datalenstr = ""

    # Acquires the data's length into a string
    data_lenstr = str(len(data))

    # If the data_lenstr is under 10 bytes add 0's to the header
    while len(data_lenstr) < 10:
        data_lenstr = "0" + data_lenstr

    # Concatenates the string of 10 bytes with the data
    new_data = data_lenstr + data

    # Sends it to sendAll
    sendAll(socket, new_data)

# Receives data from the sender
def recvMessage(socket):

    # Receives 10 bytes of data from the sender
    lenstr = recvAll(socket, 10)

    # 10 bytes is turned into the data
    len = int(lenstr)

    # The necessary data is then received, specified
    # by len
    data = recvAll(socket, len)

    # Returns the data
    return data

#Sends the file data to destination
def sendFile(fileName, sock):
	
	# How much to read in a single read
	BYTES_TO_READ_MAX = 1024
	
	# How many bytes to actually read
	bytesToRead = BYTES_TO_READ_MAX
	
	# Get the size of the file
	fileSize = os.path.getsize(fileName)
	
	# Convert the file size to string
	fileSizeStr = str(fileSize)
	
	# Send the file size
	sendMessage(sock, fileSizeStr)
	
	# The number of the bytes sent so far
	numSent = 0
	
	# Open the file
	with open(fileName, "r") as myFile:
		
		# Keep sending until all is sent
		while fileSize > numSent:
			
			# Read the data from the file
			data = myFile.read(BYTES_TO_READ_MAX)
			
			# Are we at the end of the file?
			if data:
				# Count it!
				numSent += len(data)
				
				# Send it!
				sendAll(sock, data)


# Receives file data from the sender
def recvFile(fileName, sock):

	# Get the file size string
	fileSizeStr = recvMessage(sock)

	# Get the file size
	fileSize = int(fileSizeStr)

	# The maximum number of bytes to receive	
	MAX_TO_RECV = 1024

	# How many bytes to actually receive
	numToRecv = 0
	
	# Number of bytes received so far
	numRecvSoFar = 0

	# Open the file and save it
	with open(fileName, "w") as myFile:

		# Keep receiving it until all is received
		while fileSize > numRecvSoFar:

			# How many bytes to receive
			numToRecv = MAX_TO_RECV

			# How many bytes to receive
			if numToRecv < fileSize - numRecvSoFar:
				numToRecv = fileSize - numRecvSoFar
			
			# The received data
			data = recvAll(sock, numToRecv)

			# Save the data	
			myFile.write(data)
			
			# Count the number of bytes sent
			numRecvSoFar += len(data)
