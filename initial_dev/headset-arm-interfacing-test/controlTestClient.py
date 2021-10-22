import control
import threading
import inspect
import time
from PI_server import ServerSocket

def _async_raise(tid, exctype):
	"""raises the exception, performs cleanup if needed"""
	tid = ctypes.c_long(tid)
	if not inspect.isclass(exctype):
		exctype = type(exctype)
	res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
	if res == 0:
		raise ValueError("invalid thread id")
	elif res != 1:
		# """if it returns a number greater than one, you're in trouble,
		# and you should call it again with exc=NULL to revert the effect"""
		ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)

def stop_thread(thread):
	_async_raise(thread.ident, SystemExit)


def Arm_Handle(myServer):
	while True:
		message = myServer.receiveMessage()
		if not message:
			continue
		elif message == "open":
			control.open_hand()
			time.sleep(1)
		elif message == "close":
			control.close_hand()
			time.sleep(1)
		elif message == "done":
			myServer.closeSocket()
			break

		print(message)


if __name__ == "__main__":
	# Connection information
	# server_ip = "128.153.176.67" # CDL=> Pi IP
	server_port = 42070

	# Create a new socket
	myServer = ServerSocket(server_port)

	thread2 = threading.Thread(target=Arm_Handle, args=(myServer,))
	thread2.setDaemon(True)
	thread2.start()
	time.sleep(10000)
