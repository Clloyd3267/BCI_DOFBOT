# ------------------------------------------------------------------------------
# Name         : ServerInterfaceDriver.py
# Date Created : 11/4/2021
# Author(s)    : Chris Lloyd, Josiah Schmidt, Camilla Ketola, Dylan Shuhart
# Description  : High level driver for a SmartSocket server sending/receiving
#                headset data from an Emotiv X headset. Uses Google Protocol
#                Buffers Version 3 to describe a message schema.
# ------------------------------------------------------------------------------

# Imports
from bci_dofbot_interface_pb2 import *
from google.protobuf.any_pb2  import *
from google.protobuf.message import DecodeError
from SmartSockets.SmartSocket import *
from HeadsetAPIWrapper import *
import itertools

class ServerInterfaceDriver:
	"""
	High level driver for a SmartSocket server sending/receiving
	headset data from an Emotiv X headset. Uses Google Protocol
	Buffers Version 3 to describe a message schema.

	Attributes:
		socket_type (SocketType) : Whether this socket is a client or server.
		server_ip   (str)        : The IP address of the server.
		server_port (str)        : The Port of the server.
		debug       (bool)       : Whether debug prints should be enabled.
    """
	def __init__(self, server_ip, server_port):

		# Initialize server socket
		self.serverSmartSocket = SmartSocket(server_ip, server_port, SocketType.SERVER)

		# The current response id
		self.currentResponseID = itertools.count(start=1)

		# Wrapper class for headset functions
		self.headsetAPIWrapper = HeadsetAPIWrapper()

	def unpackRequestMessage(self, requestMessage, genericMessage):
		if not genericMessage.Unpack(requestMessage):
			print("Error Unpacking Msg: ", genericMessage)

	def populateBaseResponse(self, baseResponse, baseRequest, status, statusMessage):
		self.populateBaseMessage(baseResponse.baseMessage)
		baseResponse.id = self.getNextResponseID()
		baseResponse.requestID = baseRequest.id
		baseResponse.status = status
		baseResponse.statusMessage = statusMessage

	def populateBaseMessage(self, baseMessage):
		baseMessage.sourceAddress = self.serverSmartSocket.server_ip
		baseMessage.destinationAddress = self.serverSmartSocket.client_ip[0]
		baseMessage.port = self.serverSmartSocket.server_port

	def getNextResponseID(self):
		return next(self.currentResponseID)

	def sendMessage(self, protoMessage):
		genericMessage = Any()
		genericMessage.Pack(protoMessage)
		msgData = genericMessage.SerializeToString()
		self.serverSmartSocket.sendMessage(msgData)

	def waitForMessage(self):
		messageByteString = ""
		while not messageByteString:
			messageByteString = self.serverSmartSocket.receiveMessage()

		return messageByteString

	def handleMessage(self, messageByteString):
		# Create a new generic protobuf message
		genericMessage = Any()

		# Fill generic message with incoming packet
		try:
			genericMessage.ParseFromString(messageByteString)
		except DecodeError:
			print("Error: Could not parse message. Invalid data!")
			return None

		# Unpack the generic message as a specific message
		if genericMessage.Is(ListProfileRequest.DESCRIPTOR):           # ListProfileRequest
			# Unpack specific message
			message = ListProfileRequest()
			self.unpackRequestMessage(message, genericMessage)

			# Handle request command
			profileList = self.headsetAPIWrapper.listProfiles()

			# Package and send response message
			responseMessage = ListProfileResponse()
			self.populateBaseResponse(responseMessage.baseResponse, message.baseRequest, Status.SUCCESS, "")

			# Add profile list to response
			responseMessage.profiles.extend(profileList)

			self.sendMessage(responseMessage)

		elif genericMessage.Is(CreateProfileRequest.DESCRIPTOR):       # CreateProfileRequest
			# Unpack specific message
			message = CreateProfileRequest()
			self.unpackRequestMessage(message, genericMessage)

			# Handle request command
			status, statusMessage = self.headsetAPIWrapper.createProfile(message.profileName)

			# Package and send response message
			responseMessage = CreateProfileResponse()
			self.populateBaseResponse(responseMessage.baseResponse, message.baseRequest, status, statusMessage)

			self.sendMessage(responseMessage)

		elif genericMessage.Is(RenameProfileRequest.DESCRIPTOR):       # RenameProfileRequest
			# Unpack specific message
			message = RenameProfileRequest()
			self.unpackRequestMessage(message, genericMessage)

			# Handle request command
			status, statusMessage = self.headsetAPIWrapper.renameProfile(message.oldProfileName, message.newProfileName)

			# Package and send response message
			responseMessage = RenameProfileResponse()
			self.populateBaseResponse(responseMessage.baseResponse, message.baseRequest, status, statusMessage)

			self.sendMessage(responseMessage)

		elif genericMessage.Is(DeleteProfileRequest.DESCRIPTOR):       # DeleteProfileRequest
			# Unpack specific message
			message = DeleteProfileRequest()
			self.unpackRequestMessage(message, genericMessage)

			# Handle request command
			status, statusMessage = self.headsetAPIWrapper.deleteProfile(message.profileName)

			# Package and send response message
			responseMessage = DeleteProfileResponse()
			self.populateBaseResponse(responseMessage.baseResponse, message.baseRequest, status, statusMessage)

			self.sendMessage(responseMessage)

		elif genericMessage.Is(SelectProfileRequest.DESCRIPTOR):       # SelectProfileRequest
			# Unpack specific message
			message = SelectProfileRequest()
			self.unpackRequestMessage(message, genericMessage)

			# Handle request command
			status, statusMessage = self.headsetAPIWrapper.selectProfile(message.profileName)

			# Package and send response message
			responseMessage = SelectProfileResponse()
			self.populateBaseResponse(responseMessage.baseResponse, message.baseRequest, status, statusMessage)

			self.sendMessage(responseMessage)

		elif genericMessage.Is(DeselectProfileRequest.DESCRIPTOR):     # DeselectProfileRequest
			# Unpack specific message
			message = DeselectProfileRequest()
			self.unpackRequestMessage(message, genericMessage)

			# Handle request command
			status, statusMessage = self.headsetAPIWrapper.deselectProfile()

			# Package and send response message
			responseMessage = DeselectProfileResponse()
			self.populateBaseResponse(responseMessage.baseResponse, message.baseRequest, status, statusMessage)

			self.sendMessage(responseMessage)

		elif genericMessage.Is(GetSelectedProfileRequest.DESCRIPTOR):  # GetSelectedProfileRequest
			# Unpack specific message
			message = GetSelectedProfileRequest()
			self.unpackRequestMessage(message, genericMessage)

			# Handle request command
			status, statusMessage, selectedProfile = self.headsetAPIWrapper.getSelectedProfile()

			# Package and send response message
			responseMessage = GetSelectedProfileResponse()
			self.populateBaseResponse(responseMessage.baseResponse, message.baseRequest, status, statusMessage)

			# Add selected profile to response
			responseMessage.profileName = selectedProfile

			self.sendMessage(responseMessage)

		else:
			print("Unknown Message Type: {}!".format(genericMessage.TypeName()))


if __name__ == "__main__":
	# Connection information
	server_ip = "128.153.176.67"
	server_port = 42070

	# Create a server socket
	server = ServerInterfaceDriver(server_ip, server_port)

	# Main server loop
	try:
		while True:
			message = server.waitForMessage()
			server.handleMessage(message)
	except:
		print("Keyboard interrupt issued. Server is shutting down!")

