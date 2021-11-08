# ------------------------------------------------------------------------------
# Name         : HeadsetAPIWrapper.py
# Date Created : 11/4/2021
# Author(s)    : Chris Lloyd, Josiah Schmidt, Camilla Ketola, Dylan Shuhart
# Description  : CDL=> Here
# ------------------------------------------------------------------------------

# Imports
from bci_dofbot_interface_pb2 import *

class HeadsetAPIWrapper:
	def __init__(self):
		self.profileList = []
		self.selectedProfile = ""

	def listProfiles(self):
		return self.profileList

	def createProfile(self, profileName):
		if profileName not in self.profileList:
			self.profileList.append(profileName)
			return Status.SUCCESS, "Profile {} added to profile list!".format(profileName)
		else:
			return Status.FAILURE, "Profile {} already in profile list!".format(profileName)

	def renameProfile(self, oldProfileName, newProfileName):
		if oldProfileName not in self.profileList:
			return Status.FAILURE, "Old profile {} not in profile list!".format(oldProfileName)
		elif newProfileName in self.profileList:
			return Status.FAILURE, "New profile {} already in profile list!".format(newProfileName)
		else:
			self.profileList = [profile.replace(oldProfileName, newProfileName) for profile in self.profileList]
			return Status.SUCCESS, "Profile renamed from {} to {} in profile list!".format(oldProfileName, newProfileName)

	def deleteProfile(self, profileName):
		if profileName not in self.profileList:
			return Status.FAILURE, "Profile {} not in profile list!".format(profileName)
		else:
			self.profileList.remove(profileName)
			return Status.SUCCESS, "Profile {} removed from profile list!".format(profileName)

	def selectProfile(self, profileName):
		if profileName not in self.profileList:
			return Status.FAILURE, "Profile {} not in profile list!".format(profileName)
		else:
			self.selectedProfile = profileName
			return Status.SUCCESS, "Profile {} selected!".format(profileName)

	def deselectProfile(self):
		if not self.selectedProfile:
			return Status.FAILURE, "No profile selected!"
		else:
			message = "Profile {} selected!".format(self.selectedProfile)
			self.selectedProfile = ""
			return Status.SUCCESS, message

	def getSelectedProfile(self):
		if not self.selectedProfile:
			return Status.FAILURE, "No profile selected!"
		else:
			return Status.SUCCESS, "Profile {} is currently selected!".format(self.selectedProfile)