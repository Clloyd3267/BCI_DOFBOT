import time
import control
from SmartSockets.SmartSocket import *

if __name__ == "__main__":
	# Connection information
	server_ip = "128.153.176.67" # CDL=> Pi IP
	server_port = 42070

	# Create a new server socket
	myServer = SmartSocket(server_ip, server_port, SocketType.SERVER)

	# Main program loop
	while True:
		message = myServer.receiveMessage()
		if not message:
			continue
		elif message == "drop":
			control.open_hand()
			time.sleep(1)
		elif message == "lift":
			control.close_hand()
			time.sleep(1)
		elif message == "push":
			control.arm_next_forward_position()
			time.sleep(1)
		elif message == "pull":
			control.arm_next_back_position()
			time.sleep(1)
		elif message == "left":
			control.arm_turn_left()
			time.sleep(1)
		elif message == "right":
			control.arm_turn_right()
			time.sleep(1)
		elif message == "disappear":
			control.take_picture()
			time.sleep(1)
		elif message == "done":
			myServer.closeSocket()
			break

		print(message)

