# ------------------------------------------------------------------------------
# Name         : HeadsetAPIWrapperTest.py
# Date Created : 11/4/2021
# Author(s)    : Chris Lloyd, Josiah Schmidt, Camilla Ketola, Dylan Shuhart
# Description  : CDL=> Here
# ------------------------------------------------------------------------------

# Imports

class HeadsetAPIWrapper:
	def __init__(self):
		self.profileList = ["Chris Lloyd", "Dylan Shuhart"]
		self.selectedProfile = ""

	def listProfiles(self):
		return self.profileList

	def createProfile(self, profileName):
		if profileName not in self.profileList:
			self.profileList.append(profileName)
			return True, "Profile {} added to profile list!".format(profileName)
		else:
			return False, "Profile {} already in profile list!".format(profileName)

	def renameProfile(self, oldProfileName, newProfileName):
		if oldProfileName not in self.profileList:
			return False, "Old profile {} not in profile list!".format(oldProfileName)
		elif newProfileName in self.profileList:
			return False, "New profile {} already in profile list!".format(newProfileName)
		else:
			self.profileList = [profile.replace(oldProfileName, newProfileName) for profile in self.profileList]
			return True, "Profile renamed from {} to {} in profile list!".format(oldProfileName, newProfileName)

	def deleteProfile(self, profileName):
		if profileName not in self.profileList:
			return False, "Profile {} not in profile list!".format(profileName)
		else:
			self.profileList.remove(profileName)
			return True, "Profile {} removed from profile list!".format(profileName)

	def selectProfile(self, profileName):
		if profileName not in self.profileList:
			return False, "Profile {} not in profile list!".format(profileName)
		else:
			self.selectedProfile = profileName
			return True, "Profile {} selected!".format(profileName)

	def deselectProfile(self):
		if not self.selectedProfile:
			return False, "No profile selected!"
		else:
			message = "Profile {} selected!".format(self.selectedProfile)
			self.selectedProfile = ""
			return True, message

	def getSelectedProfile(self):
		if not self.selectedProfile:
			return False, "No profile selected!", ""
		else:
			return True, "Profile {} is currently selected!".format(self.selectedProfile), self.selectedProfile

	def trainProfile(self, action, detection, status):
		return True, "Action: {}, Detection: {}, Status: {}".format(action, detection, status), action

	def startInferencing(self):
		return True, "Inferencing started!"

	def stopInferencing(self):
		return True, "Inferencing stopped!"

	def receiveInference(self):
		status = True
		message = ""
		action = ""
		power = 0.9
		time = 69420
		return status, message, action, power, time