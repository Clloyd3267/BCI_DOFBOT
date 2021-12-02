# ------------------------------------------------------------------------------
# Name         : main.py
# Date Created : 12/01/2021
# Author(s)    : Chris Lloyd, Josiah Schmidt, Camilla Ketola, Dylan Shuhart
# Description  : Client main code for BCI Dofbot (EEG Controlled Robotic Arm).
# ------------------------------------------------------------------------------

# Imports
from HeadsetAPIWrapperTest import * # CDL=>from ClientInterfaceDriver import *
from UserIOInteraction import *
import enum
import time

class ModeType(enum.Enum):
	"""Simple Enumeration class to store system modes."""
	INITIALIZATION_MODE = 1
	PROFILE_SELECTION_MODE = 2
	TRAINING_MODE = 3
	LIVE_MODE = 4

def keyboardPluggedIn(): # CDL=> Replace with final version later
	return True

# CDL=> Move to library file
rstButton = False
ProfileSltButton = False
def isPressed(button):
	if button:
		button = False
		return True
	else:
		return False

class DofbotSubsystem:
	"""
	This class describes the main code for the BCI_Dofbot system running on the
	Dofbot Robotic Arm Raspberry Pi.

	Attributes:
		headsetInterface (ClientInterfaceDriver) : Whether this socket is a client or server.
		currentMode      (ModeType enum)         : The IP address of the server.
		debug            (bool)                  : Whether debug prints should be enabled.
    """

	def __init__(self, server_ip, server_port, debug=False):
		"""
		The default constructor for class DofbotSubsystem.

		Arguments:
			server_ip   (str)        : The IP address of the server.
			server_port (str)        : The Port of the server.
			debug       (bool)       : Whether debug prints should be enabled.
		"""

		self.debug = debug

		# Headset API Interface
		# headsetInterface = ClientInterfaceDriver(server_ip, server_port) # CDL=> Replace with client later
		self.headsetInterface = HeadsetAPIWrapper()

		# System Mode
		self.currentMode = ModeType.INITIALIZATION_MODE

	def initializationMode(self):
		"""The user logic for the initialization mode."""
		# CDL=> Move arm to default position
		pass # CDL=> Do more here!

	def profileSelectionMode(self):
		"""The user logic for the profile selection mode."""

		# Get a list of all the profiles
		profileList = self.headsetInterface.listProfiles()

		print("--------Select or Create a Profile---------")
		userInput = input("Type select or create: ").lower()

		if userInput == "select":
			profileName = promptUserList("Current Profile List:", profileList)
			if profileName:
				message = ""
				if keyboardPluggedIn():
					message = "What would you like to do with the profile? Type Load, Delete, Rename, or Train: "
				else:
					message = "What would you like to do with the profile? Type Load, Delete, or Train: "

				userInput = input(message).lower()

				if userInput == "load":
					print("Going to Live mode")
					self.headsetInterface.selectProfile(profileName)
					self.currentMode = ModeType.LIVE_MODE
				elif userInput == "train":
					print("Going to Training Mode")
					self.headsetInterface.selectProfile(profileName)
					self.currentMode = ModeType.TRAINING_MODE
				elif keyboardPluggedIn() and userInput == "rename":
					userInput = input("Enter a new profile name: ")
					self.headsetInterface.renameProfile(profileName, userInput)
					print("Profile {} renamed to {}".format(profileName, userInput))
				elif userInput == "delete":
					userInput = input("Are you sure you want to delete?").lower()
					if userInput == "yes":
						self.headsetInterface.deleteProfile(profileName)
					else:
						print("Canceling delete operation for {}".format(profileName))
				else:
					print("\nInvalid Input. Please try again!\n")
			else:
				print("\nInvalid Input. Please try again!\n")

		elif userInput == "create":
			newProfileName = ""
			if keyboardPluggedIn():
				newProfileName = input("Enter a new profile name: ")
			else:
				i = 0
				while True:
					newProfileName = "New Profile {}".format(i)
					if newProfileName not in profileList:
						break
					else:
						i += 1
			self.headsetInterface.createProfile(newProfileName)
			print("Profile {} created".format(newProfileName))

	def trainingMode(self):
		"""The user logic for the training mode."""

		userInput = input("Type clear to clear an all training, trainact to train an action or exit to leave and go live mode: ").lower()
		if keyboardPluggedIn() and userInput == "clear":
			print("Deleting training data")
			self.headsetInterface.clearAll()
		if keyboardPluggedIn() and userInput == "trainact":
			while True:
				actionList = list(self.headsetInterface.getSigTrainedAct().keys())
				action = promptUserList("Action List: ", actionList)
				trainDelete = promptUserList("Do you want to train or delete training for the action?", ["train", "delete"])
				if trainDelete == "delete":
					self.headsetInterface.trainProfile(action, "mentalCommand", "erase")
				elif trainDelete == "train":
					printMessage("Please think about or move with selected action")
					printMessage("Press button when ready")
					#insert button push

					self.headsetInterface.trainProfile(action, "mentalCommand", "start")
					#training running
					acceptReset = promptUserList("Training Complete! Do you want to accept or reject the training? ", ["accept", "reject"])
					if acceptReset == "accept":
						self.headsetInterface.trainProfile(action, "mentalCommand", "accept")
						doneNotDone = promptUserList("Are you done or do you want to train again? Type done or continue. ", ["done", "continue"])		# Check if done or train again
						if doneNotDone == "done": 					#if done, break, else continue
							break

						elif acceptReset == "reject":
							self.headsetInterface.trainProfile(action, "mentalCommand", "reset")
							printMessage("Training rejected")
							break

		if keyboardPluggedIn() and userInput == "exit":
			print("Going to live mode")
			self.currentMode = ModeType.LIVE_MODE

	def liveMode(self):
		"""The user logic for the live mode."""

		# Start Live Mode
		self.headsetInterface.startInferencing()

		while True:
			status, message, action, __, __ = self.headsetInterface.receiveInference()
			if isPressed(rstButton):
				self.headsetInterface.stopInferencing()
				self.currentMode = ModeType.INITIALIZATION_MODE
				break
			elif isPressed(ProfileSltButton):
				self.headsetInterface.stopInferencing()
				self.currentMode = ModeType.PROFILE_SELECTION_MODE
				break
			elif not status:
				printMessage(message)
				continue
			elif action == "neutral":
				continue
			elif action == "lift":
				# control.grab_and_get()
				print(action)
			elif action == "drop":
				#control.put_back()
				print(action)
			elif action == "disappear":
				#control.take_picture()
				print(action)
			else:
				print("Invalid Inference: {}".format(action))
			time.sleep(1)

			# Stop Live Mode
			status, message = self.headsetInterface.stopInferencing()

	def main(self):
		"""The main user logic for mode selection control."""
		try:
			while True:
				if self.currentMode == ModeType.INITIALIZATION_MODE:
					self.initializationMode()

				elif self.currentMode == ModeType.PROFILE_SELECTION_MODE:
					self.profileSelectionMode()

				elif self.currentMode == ModeType.TRAINING_MODE:
					self.trainingMode()

				elif self.currentMode == ModeType.LIVE_MODE:
					self.liveMode()
		except:
			print("Error exception occurred. Exiting!!!")

if __name__ == "__main__":
	# Connection information
	server_ip = "128.153.178.74"
	server_port = 42070

	dofbotSubsystem = DofbotSubsystem(server_ip, server_port)
	dofbotSubsystem.main()


