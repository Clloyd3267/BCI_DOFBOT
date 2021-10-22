# ------------------------------------------------------------------------------
# Name         : Simple_Server.py
# Date Created : 10/21/2021
# Author(s)    : Chris Lloyd, Josiah Schmidt, Camilla Ketola, Dylan Shuhart
# Description  : A test server to ensure the SmartSocket module works
# ------------------------------------------------------------------------------

# Imports
from SmartSocket import *

if __name__ == "__main__":
	# Connection information
	server_ip = "128.153.176.67"
	server_port = 42070

	# Create a server socket
	myServer = SmartSocket(server_ip, server_port, SocketType.SERVER)
	print("Socket Type: ", myServer.socket_type.name)

	# Receive data in server
	while True:
		message = myServer.receiveMessage()
		if not message:
			continue
		elif message == "done":
			break
		else:
			print(message)

	# Send some data from the client
	myServer.sendMessage("msg1")
	myServer.sendMessage("msg2")
	myServer.sendMessage("msg3")
	myServer.sendMessage("done")

	# Close the socket connection
	myServer.closeSocket()