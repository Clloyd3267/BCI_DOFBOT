# ------------------------------------------------------------------------------
# Name         : Simple_Client.py
# Date Created : 10/21/2021
# Author(s)    : Chris Lloyd, Josiah Schmidt, Camilla Ketola, Dylan Shuhart
# Description  : A test client to ensure the SmartSocket module works
# ------------------------------------------------------------------------------

# Imports
from SmartSocket import *

if __name__ == "__main__":
	# Connection information
	server_ip = "128.153.176.67"
	server_port = 42070

	# Create a client socket
	myClient = SmartSocket(server_ip, server_port, SocketType.CLIENT)
	print("Socket Type: ", myClient.socket_type.name)

	# Send some data from the client
	myClient.sendMessage("msg1")
	myClient.sendMessage("msg2")
	myClient.sendMessage("msg3")
	myClient.sendMessage("done")

	# Receive data in client
	while True:
		message = myClient.receiveMessage()
		if not message:
			continue
		elif message == "done":
			break
		else:
			print(message)

	# Close the socket connection
	myClient.closeSocket()