# Imports
import socket

class ClientSocket:
	def __init__(self, server_ip, server_port):
		self.server_ip = server_ip
		self.server_port = server_port

		# Create TCP/IP socket on client side
		self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Connect the client socket to the IP/PORT of the server
		self.client_sock.connect((self.server_ip, self.server_port))
		print("Connection Established with server: ", self.server_ip, ":", self.server_port)

	def closeSocket(self):
		self.client_sock.close()
		print("Disconnected from server: ", self.server_ip, ":", self.server_port)

	def sendMessage(self, message):
		self.client_sock.send((str(message) + '\n').encode())


if __name__ == "__main__":
	# Connection information
	server_ip = "128.153.176.67"
	server_port = 42070

	# Create a new socket
	myClient = ClientSocket(server_ip, server_port)

	# Send some data
	myClient.sendMessage("move_left")
	myClient.sendMessage("move_neutral")
	myClient.sendMessage("move_right")
	myClient.sendMessage("done")

	# Close the connection
	myClient.closeSocket()

