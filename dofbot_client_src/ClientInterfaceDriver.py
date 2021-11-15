# ------------------------------------------------------------------------------
# Name         : ClientInterfaceDriver.py
# Date Created : 11/8/2021
# Author(s)    : Chris Lloyd, Josiah Schmidt, Camilla Ketola, Dylan Shuhart
# Description  : CDL=>
# ------------------------------------------------------------------------------
# Imports
from bci_dofbot_interface_pb2 import *
from google.protobuf.any_pb2  import *
from SmartSockets.SmartSocket import *
import itertools

class ClientInterfaceDriver:
	def __init__(self, server_ip, server_port):

		# Initialize server socket
		self.serverSmartSocket = SmartSocket(server_ip, server_port, SocketType.CLIENT)

		self.currentResponseID = itertools.count(start=1)

	def unpackResponseMessage(self, responseMessage, genericMessage):
		if not genericMessage.Unpack(responseMessage):
			print("Error Unpacking Msg: ", genericMessage)

	def populateBaseRequest(self, baseRequest):
		self.populateBaseMessage(baseRequest.baseMessage)
		baseRequest.id = self.getNextResponseID()

	def populateBaseMessage(self, baseMessage):
		# baseMessage.sourceAddress = self.serverSmartSocket.client_ip[0]
		# baseMessage.destinationAddress = self.serverSmartSocket.server_ip
		# baseMessage.port = self.serverSmartSocket.server_port
		pass

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

	def waitForGenericMessage(self):
		# Wait for response message
		messageByteString = self.waitForMessage()

		# Create a new generic protobuf message
		genericMessage = Any()

		# Fill generic message with incoming packet
		genericMessage.ParseFromString(messageByteString)
		return genericMessage

	def listProfiles(self):
		# Package and send request message
		requestMessage = ListProfileRequest()
		self.populateBaseRequest(requestMessage.baseRequest)

		# Send request message
		self.sendMessage(requestMessage)

		genericMessage = self.waitForGenericMessage()

		if genericMessage.Is(ListProfileResponse.DESCRIPTOR):
			# Parse message
			responseMessage = ListProfileResponse()
			self.unpackResponseMessage(responseMessage, genericMessage)

			return responseMessage.profiles
		else:
			print("Error parsing message! Unexpected response type {}".format(genericMessage.TypeName))
			return []

	def createProfile(self, profileName):
		# Package and send request message
		requestMessage = CreateProfileRequest()
		self.populateBaseRequest(requestMessage.baseRequest)

		# Add profile name to request
		requestMessage.profileName = profileName

		# Send request message
		self.sendMessage(requestMessage)

		genericMessage = self.waitForGenericMessage()

		if genericMessage.Is(CreateProfileResponse.DESCRIPTOR):
			# Parse message
			responseMessage = CreateProfileResponse()
			self.unpackResponseMessage(responseMessage, genericMessage)

			return responseMessage.baseResponse.status == Status.SUCCESS
		else:
			print("Error parsing message! Unexpected response type {}".format(genericMessage.TypeName))
			return False, "Error parsing message!"

	def renameProfile(self, oldProfileName, newProfileName):
		# Package and send request message
		requestMessage = RenameProfileRequest()
		self.populateBaseRequest(requestMessage.baseRequest)

		# Add profile names to request
		requestMessage.oldProfileName = oldProfileName
		requestMessage.newProfileName = newProfileName

		# Send request message
		self.sendMessage(requestMessage)

		genericMessage = self.waitForGenericMessage()

		if genericMessage.Is(RenameProfileResponse.DESCRIPTOR):
			# Parse message
			responseMessage = RenameProfileResponse()
			self.unpackResponseMessage(responseMessage, genericMessage)

			return responseMessage.baseResponse.status == Status.SUCCESS
		else:
			print("Error parsing message! Unexpected response type {}".format(genericMessage.TypeName))
			return False, "Error parsing message!"

	def deleteProfile(self, profileName):
		# Package and send request message
		requestMessage = DeleteProfileRequest()
		self.populateBaseRequest(requestMessage.baseRequest)

		# Add profile name to request
		requestMessage.profileName = profileName

		# Send request message
		self.sendMessage(requestMessage)

		genericMessage = self.waitForGenericMessage()

		if genericMessage.Is(DeleteProfileResponse.DESCRIPTOR):
			# Parse message
			responseMessage = DeleteProfileResponse()
			self.unpackResponseMessage(responseMessage, genericMessage)

			return responseMessage.baseResponse.status == Status.SUCCESS
		else:
			print("Error parsing message! Unexpected response type {}".format(genericMessage.TypeName))
			return False, "Error parsing message!"

	def selectProfile(self, profileName):
		# Package and send request message
		requestMessage = SelectProfileRequest()
		self.populateBaseRequest(requestMessage.baseRequest)

		# Add profile name to request
		requestMessage.profileName = profileName

		# Send request message
		self.sendMessage(requestMessage)

		genericMessage = self.waitForGenericMessage()

		if genericMessage.Is(SelectProfileResponse.DESCRIPTOR):
			# Parse message
			responseMessage = SelectProfileResponse()
			self.unpackResponseMessage(responseMessage, genericMessage)

			return responseMessage.baseResponse.status == Status.SUCCESS
		else:
			print("Error parsing message! Unexpected response type {}".format(genericMessage.TypeName))
			return False, "Error parsing message!"

	def deselectProfile(self):
		# Package and send request message
		requestMessage = DeselectProfileRequest()
		self.populateBaseRequest(requestMessage.baseRequest)

		# Send request message
		self.sendMessage(requestMessage)

		genericMessage = self.waitForGenericMessage()

		if genericMessage.Is(DeselectProfileResponse.DESCRIPTOR):
			# Parse message
			responseMessage = DeselectProfileResponse()
			self.unpackResponseMessage(responseMessage, genericMessage)

			return responseMessage.baseResponse.status == Status.SUCCESS
		else:
			print("Error parsing message! Unexpected response type {}".format(genericMessage.TypeName))
			return False, "Error parsing message!"

	def getSelectedProfile(self):
		# Package and send request message
		requestMessage = GetSelectedProfileRequest()
		self.populateBaseRequest(requestMessage.baseRequest)

		# Send request message
		self.sendMessage(requestMessage)

		genericMessage = self.waitForGenericMessage()

		if genericMessage.Is(GetSelectedProfileResponse.DESCRIPTOR):
			# Parse message
			responseMessage = GetSelectedProfileResponse()
			self.unpackResponseMessage(responseMessage, genericMessage)

			return responseMessage.profileName
		else:
			print("Error parsing message! Unexpected response type {}".format(genericMessage.TypeName))
			return False, "Error parsing message!"

	def trainProfile(self, action, detection, status):
		# Package and send request message
		requestMessage = TrainingRequest()
		self.populateBaseRequest(requestMessage.baseRequest)

		# Populate request message
		requestMessage.action = action
		requestMessage.detectionType = detection
		requestMessage.trainingStatus = status

		# Send request message
		self.sendMessage(requestMessage)

		genericMessage = self.waitForGenericMessage()

		if genericMessage.Is(TrainingResponse.DESCRIPTOR):
			# Parse message
			responseMessage = TrainingResponse()
			self.unpackResponseMessage(responseMessage, genericMessage)

			return responseMessage.baseResponse.status == Status.SUCCESS, responseMessage.baseResponse.statusMessage
		else:
			print("Error parsing message! Unexpected response type {}".format(genericMessage.TypeName))
			return False, "Error parsing message!"

	def startInferencing(self):
		# Package and send request message
		requestMessage = StartInferencingRequest()
		self.populateBaseRequest(requestMessage.baseRequest)

		# Send request message
		self.sendMessage(requestMessage)

		genericMessage = self.waitForGenericMessage() # CDL=> COme bak here ;)

		if genericMessage.Is(StartInferencingResponse.DESCRIPTOR):
			# Parse message
			responseMessage = StartInferencingResponse()
			self.unpackResponseMessage(responseMessage, genericMessage)

			return responseMessage.baseResponse.status == Status.SUCCESS, responseMessage.baseResponse.statusMessage
		else:
			print("Error parsing message! Unexpected response type {}".format(genericMessage.TypeName))
			return False, "Error parsing message!"

	def stopInferencing(self):
		# Package and send request message
		requestMessage = StopInferencingRequest()
		self.populateBaseRequest(requestMessage.baseRequest)

		# Send request message
		self.sendMessage(requestMessage)

		genericMessage = self.waitForGenericMessage()

		if genericMessage.Is(StopInferencingResponse.DESCRIPTOR):
			# Parse message
			responseMessage = StopInferencingResponse()
			self.unpackResponseMessage(responseMessage, genericMessage)

			return responseMessage.baseResponse.status == Status.SUCCESS, responseMessage.baseResponse.statusMessage
		else:
			print("Error parsing message! Unexpected response type {}".format(genericMessage.TypeName))
			return False, "Error parsing message!"

	def receiveInference(self):
		# Package and send request message
		requestMessage = ReceiveInferenceRequest()
		self.populateBaseRequest(requestMessage.baseRequest)

		# Send request message
		self.sendMessage(requestMessage)

		genericMessage = self.waitForGenericMessage()

		if genericMessage.Is(ReceiveInferenceResponse.DESCRIPTOR):
			# Parse message
			responseMessage = ReceiveInferenceResponse()
			self.unpackResponseMessage(responseMessage, genericMessage)

			action = responseMessage.action
			power = responseMessage.power
			time = responseMessage.time

			return responseMessage.baseResponse.status == Status.SUCCESS, responseMessage.baseResponse.statusMessage, action, power, time
		else:
			print("Error parsing message! Unexpected response type {}".format(genericMessage.TypeName))
			return False, "Error parsing message!"

if __name__ == "__main__":
	# Connection information
	# server_ip = "128.153.176.67"
	server_ip = "128.153.178.74" # 128.153.190.62
	server_port = 42070

	# Create a server socket
	server = ClientInterfaceDriver(server_ip, server_port)

	print(server.listProfiles())
	# server.createProfile("Bob")
	# print(server.listProfiles())
	# server.renameProfile("Bob", "Not Bob ;)")
	# print(server.listProfiles())

	# print("Selected profile: ", server.getSelectedProfile())
	# server.selectProfile("Cat 1 Crit rider Josiah (only on CU campus crit)")
	# print("Selected profile: ", server.getSelectedProfile())
	# server.deselectProfile()
	# print("Selected profile: ", server.getSelectedProfile())

	# server.deleteProfile("Cat 1 Crit rider Josiah (only on CU campus crit)")
	# print(server.listProfiles())
	# print(server.receiveInference())

	server.serverSmartSocket.closeSocket()
