# ------------------------------------------------------------------------------
# Name         : SmartSocket.py
# Date Created : 10/21/2021
# Author(s)    : Chris Lloyd, Josiah Schmidt, Camilla Ketola, Dylan Shuhart
# Description  : An abstraction layer for TCP/IP sockets to allow for simple
#                usage of the network sockets interface.
# ------------------------------------------------------------------------------

# Imports
import enum
import socket
import struct

class SocketType(enum.Enum):
	"""Simple Enumeration class to store socket types."""
	SERVER = 1
	CLIENT = 2

class SmartSocket:
	"""
	A socket that can be either a client or server depending on (self.socket_type).
	Data is written and recieved as strings. All messages are preceded by a 32-bit
	int with the message payload size to allow for simple receive and send.

	Attributes:
		socket_type (SocketType) : Whether this socket is a client or server.
		server_ip   (str)        : The IP address of the server.
		server_port (str)        : The Port of the server.
		debug       (bool)       : Whether debug prints should be enabled.
    """
	def __init__(self, server_ip, server_port, socket_type=SocketType.SERVER, debug=True):
		"""
		The default constructor for class SmartSocket.

		Arguments:
			socket_type (SocketType) : Whether this socket is a client or server.
			server_ip   (str)        : The IP address of the server.
			server_port (str)        : The Port of the server.
			debug       (bool)       : Whether debug prints should be enabled.
		"""

		# Validate/Store inputs
		if socket_type not in SocketType:
			print("Invalid Socket Type")
		self.socket_type = socket_type
		self.server_ip = server_ip
		self.server_port = server_port
		self.debug = debug

		if socket_type == SocketType.SERVER:
			# Create TCP/IP socket on server side
			self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			# Bind the socket to the IP/PORT of the server
			# '' implies any IP/hostname that the server can be accessed by
			self.server_sock.bind(('', self.server_port))

			# Restrict to only one connection
			self.server_sock.listen(1)
			if self.debug: print("Server waiting for connection...")

			# Wait for a client to connect
			self.client_sock, self.client_ip = self.server_sock.accept()
			if self.debug: print("Connection established with client: ", str(self.client_ip), ":", self.server_port)
		else:
			# Create TCP/IP socket on client side
			self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			# Connect the client socket to the IP/PORT of the server
			self.client_sock.connect((self.server_ip, self.server_port))
			if self.debug: print("Connection established with server: ", self.server_ip, ":", self.server_port)

	def closeSocket(self): # CDL=> What happens if send/receive called on a closed socket?
		"""Function to close the socket."""

		# Close the socket
		self.client_sock.close()

		# Print exit message
		if self.socket_type == SocketType.SERVER:
			if self.debug: print("Disconnected from client: ", str(self.client_ip), ":", self.server_port)
		else:
			if self.debug: print("Disconnected from server: ", self.server_ip, ":", self.server_port)

	def sendMessage(self, message):
		"""
		Function to send a message via the network socket.

		Arguments:
			message (str): The message to send.
		"""

		len_bytes = struct.pack('>L', len(message))

		# Send message length + serialized message
		self.client_sock.send(len_bytes)
		self.client_sock.send(message.encode())
		if self.debug: print("Message sent successfully!")


	def receiveMessage(self):
		"""
		Function to receive a message via the network socket.

		Returns:
			(str): The received message.
		"""

		# Read 4 byte message length
		msg_len_bytes = self.client_sock.recv(4)

		if len(msg_len_bytes) == 0:
			return None
		else:
			msg_len = struct.unpack('>L', msg_len_bytes)[0]
			if self.debug: print("Message received successfully!")
			return str(self.client_sock.recv(msg_len).decode())
