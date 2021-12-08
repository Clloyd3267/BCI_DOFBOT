# ------------------------------------------------------------------------------
# Name         : HeadsetAPIWrapper.py
# Date Created : 11/4/2021
# Author(s)    : Chris Lloyd, Josiah Schmidt, Camilla Ketola, Dylan Shuhart
# Description  : CDL=> Here
# ------------------------------------------------------------------------------

# Imports
from custom_cortex import Cortex
import time

# Global Variables
user = {
    "license": "b277efe2-8fdd-4bef-a54e-b5b85058bf63",
    "client_id": "yVAmVcwkGHUzjEMEHso81MHrPtihWveETJzIN9VK",
    "client_secret": "eF3OB86C40spvM1WwyjYpItSNoUIDI6dnPXl1XShrCLzgLqZ0GQTBZ6jtzUEfLcQul4eCD0h8JdMnFaSSPXis5AISy5Me4MtUdTsXJ2skW1qUpnrNVRKXgbmtZHiEvIx",
    "debit": 100
}

# Headset Wrapper

class HeadsetAPIWrapper:
	def __init__(self):
		self.c = Cortex(user)
		self.c.do_prepare_steps()  # This starts Cortex
		self.stream = ['com']  # Receives mental command data by default
		self.status_list = ['start', 'accept', 'reject', 'reset', 'erase']

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

	# Trains a profile using the given status and action
	def trainProfile(self, action, detection, status):

		print("Train function entered")
		if detection != ('mentalCommand' or 'facialExpression'):
			return False, "Detection must be set to 'mentalCommand' or 'facialExpression'"

		if detection == 'mentalCommand':
			self.stream = 'com'
		else:
			self.stream = 'fac'

		# Make sure valid status is used
		if status not in self.status_list:
			return False, "Status input must be 'start' or 'accept' or 'reject' or 'reset' or 'erase'"

		print('{} training -----------------------------------'.format(status))

		print(detection, action, status)

		self.c.train_request(detection=detection, action=action, status=status)

		return True, "{} {} training request was successful".format(status, action)

	# Get all available commands for detection type
	def getDetectionInfo(self, detection):
		actions = self.c.getDetetctionInfo(detection)
		return True, actions

	# Get the trained actions along with how many times they were trained
	def getTrainedActions(self, detection):
		return self.c.get_trained_signature_action(detection, self.selectedProfile)

# ---------------------- Inferencing Actions ----------------------

	# Subscribe to action stream
	def startInferencing(self):
		self.c.sub_request(self.stream)
		time.sleep(1)
		return True, "Inference Started"

	# Unsubscribe to action stream
	def stopInferencing(self):
		self.c.unsub_request(self.stream)
		return False, "Inference Stopped"

	# Returns headset action, power, and time
	def receiveInference(self):
		action, power, time = self.c.getCurrentInference()
		if (action and time):
			return True, "Action, time, power: ", action, power, int(time)
		else:
			print(action, power, time)
			return False, "Inference failed", "", 0, 0
