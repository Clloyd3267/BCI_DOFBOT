# ------------------------------------------------------------------------------
# Name         : HeadsetAPIWrapper.py
# Date Created : 11/4/2021
# Author(s)    : Chris Lloyd, Josiah Schmidt, Camilla Ketola, Dylan Shuhart
# Description  : CDL=> Here
# ------------------------------------------------------------------------------

# Imports
# from bci_dofbot_interface_pb2 import *
from SmartSockets.SmartSocket import *
from custom_cortex import Cortex

# Global Variables
user = {
   "license": "b277efe2-8fdd-4bef-a54e-b5b85058bf63",
   "client_id": "yVAmVcwkGHUzjEMEHso81MHrPtihWveETJzIN9VK",
   "client_secret": "eF3OB86C40spvM1WwyjYpItSNoUIDI6dnPXl1XShrCLzgLqZ0GQTBZ6jtzUEfLcQul4eCD0h8JdMnFaSSPXis5AISy5Me4MtUdTsXJ2skW1qUpnrNVRKXgbmtZHiEvIx",
   "debit": 100
}

class HeadsetAPIWrapper:
	def __init__(self):
		self.c = Cortex(user, True)
		self.c.do_prepare_steps()  # This starts Cortex
		self.selectedProfile = ""
		self.stream = ['com']  # Receives mental command data by default
		# self.c.bind(new_com_data=self.on_new_data)
		self.selectedAction = ''
		self.server_ip = "128.153.178.74"
		self.server_port = 42071
		self.status_list = ['start', 'accept', 'reject', 'reset', 'erase']
		# Create a server socket
		# self.server = SmartSocket(self.server_ip, self.server_port, SocketType.SERVER, debug=True)

# ---------------------- Debug Actions ----------------------



# ---------------------- Profile Actions ----------------------

	# Make a list of strings containing the profile name
	def listProfiles(self):
		return self.c.query_profile()

	# Creates a new profile unless name is already taken
	## character limits?? ##
	def createProfile(self, profileName):

		if profileName not in self.c.query_profile():
			status = 'create'
			self.c.setup_profile(profileName, status)

			return True, "Profile {} added to profile list!".format(profileName)
		else:
			return False, "Profile {} already in profile list!".format(profileName)

	# Change the name of an existing profile
	def renameProfile(self, oldProfileName, newProfileName):

		if oldProfileName not in self.c.query_profile():
			return False, "Old profile {} not in profile list!".format(oldProfileName)
		elif newProfileName in self.c.query_profile():
			return False, "New profile {} already in profile list!".format(newProfileName)
		else:
			status = 'rename'
			self.c.setup_profile(oldProfileName, status, newProfileName)
			return True, "Profile renamed from {} to {} in profile list!".format(oldProfileName, newProfileName)

	# Removes a profile with a given name from the system
	def deleteProfile(self, profileName):
		if profileName not in self.c.query_profile():
			return False, "Profile {} not in profile list!".format(profileName)
		else:
			status = 'delete'
			self.c.setup_profile(profileName, status)
			return True, "Profile {} removed from profile list!".format(profileName)

	# Loads the profile with the given name
	def selectProfile(self, profileName):
		if profileName not in self.c.query_profile():
			return False, "Profile {} not in profile list!".format(profileName)
		else:
			self.c.sub_request(['sys'])
			self.selectedProfile = profileName
			status = 'load'
			self.c.setup_profile(profileName, status)
			return True, "Profile {} selected!".format(profileName)

	# Unload the profile with the given name
	def deselectProfile(self):
		if not self.selectedProfile:
			return False, "No profile selected!"
		else:
			message = "Profile {} selected!".format(self.selectedProfile)
			status = 'unload'
			self.c.setup_profile(self.selectedProfile, status)
			self.selectedProfile = ""
			return True, message

	# Return name of selected profile
	def getSelectedProfile(self):
		if not self.selectedProfile:
			return False, "No profile selected!", ""
		else:
			return True, "Profile {} is currently selected!".format(self.selectedProfile), self.selectedProfile

# ---------------------- Training Actions ----------------------

	# Top priority
	# Trains a profile using the given status and action
	def trainProfile(self, action, detection, status):

		print("Train function entered")
		if detection != ('mentalCommand' or 'facialExpression'):
			return False, "Detection must be set to 'mentalCommand' or 'facialExpression'"

		if detection == 'mentalCommand':
			self.stream = 'com'
		else:
			self.stream = 'fac'

		print(self.stream)

		# Make sure valid status is used
		if status not in self.status_list:
			print("incorrect status")
			return False, "Status input must be 'start' or 'accept' or 'reject' or 'reset' or 'erase'"

		# self.c.sub_request(['sys'])

		print('{} training -----------------------------------'.format(status))

		print(detection, action, status)

		self.c.train_request(detection=detection, action=action, status=status)

		return True, "{} {} training request was successful".format(status, action)


	#

	# Get all available commands for detection type
	def getDetectionInfo(self, detection):
		actions = self.c.getDetetctionInfo(detection)
		return True, actions

	def getTrainedActions(self, detection):
		#TODO
		pass

# ---------------------- Inferencing Actions ----------------------

	# Top priority
	# Subscribe to action stream
	def startInferencing(self):
		self.c.sub_request(self.stream)
		return True, ""

	# Top priority
	# Unsubscribe to action stream
	def stopInferencing(self):
		self.c.unsub_request(self.stream)
		return False, ""

	# Top priority
	# Returns headset action, power, and time
	def receiveInference(self):
		action, power, time = self.c.getCurrentInference()
		if (action and power and time):
			return True, "Action, time, power: ", action, power, int(time)
		else:
			return False, "Inference failed", "", 0, 0


if __name__ == "__main__":

	h = HeadsetAPIWrapper()

	# h.createProfile("HeadsetAPITest1")
	# print(h.listProfiles())
	#
	# h.deleteProfile("HeadsetTest1")
	# print(h.listProfiles())
	#
	# h.renameProfile("HeadsetAPITest1", "HeadsetTest1")
	# print(h.listProfiles())
	#
	# h.selectProfile("HeadsetTest1")
	# print(h.getSelectedProfile())
	# h.deselectProfile()
	# print(h.getSelectedProfile())

	h.createProfile("ToTrain")
	print(h.listProfiles())

	h.selectProfile("ToTrain")
	print(h.getSelectedProfile())

	h.getDetectionInfo('mentalCommand')

	print("before start train is called")
	h.trainProfile('neutral', 'mentalCommand', 'start')
	print("after start train called")

	print("before accept train is called")
	h.trainProfile('neutral', 'mentalCommand', 'accept')
	print("after accept train called")

	# h.startInferencing()
	#
	# try:
	# 	while True:
	# 		print(h.receiveInference())
	# except KeyboardInterrupt:
	# 	h.stopInferencing()
	#
	# print("out of loop")


