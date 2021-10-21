# Imports
import socket

# CDL=> Move to seperate file later
class ReadBuffer:
	def __init__(self,sock):
		self.sock = sock
		self.buffer = b''
	def get_line(self):
		while b'\n' not in self.buffer:
			data = self.sock.recv(1024)
			if not data: # Socket closed
				return None
			self.buffer += data
		line,sep,self.buffer = self.buffer.partition(b'\n')
		return line.decode()

class ServerSocket:
	def __init__(self, server_port):
		self.server_port = server_port

		# Create TCP/IP socket on server side
		self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Bind the socket to the IP/PORT of the server
		# '' implies any IP/hostname that the server can be accessed by
		self.server_sock.bind(('', self.server_port))

		# Restrict to only one connection
		self.server_sock.listen(1)
		print("Server waiting for connection...")

		# Wait for a client to connect
		self.client_sock, self.client_addr = self.server_sock.accept()
		print("Connection Established with client: ", str(self.client_addr), ":", self.server_port)

		self.rcv_buf = ReadBuffer(self.client_sock)

	def closeSocket(self):
		self.client_sock.close()
		print("Disconnected from client: ", str(self.client_addr), ":", self.server_port)

	def sendMessage(self, message):
		self.client_sock.send((str(message) + "\n").encode())

	def receiveMessage(self):
		while True:
			line = self.rcv_buf.get_line()
			if not line:
				return None # CDL=> None?
			else:
				return str(line)


if __name__ == "__main__":
	# Connection information
	# server_ip = "128.153.176.67" # CDL=> Pi IP
	server_port = 42070

	# Create a new socket
	myServer = ServerSocket(server_port)

	while True:
		message = myServer.receiveMessage()
		if not message:
			continue
		elif message == "done":
			break
		else:
			print(message)

	# Close the connection
	myServer.closeSocket()