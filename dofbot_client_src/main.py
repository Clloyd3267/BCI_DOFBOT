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
		consoleMode      (bool)                  : Whether the program uses the console/keyboard
		                                           or the buttonpad and oled.
    """

	def __init__(self, server_ip, server_port, debug=False, consoleMode=True):
		"""
		The default constructor for class DofbotSubsystem.

		Arguments:
			server_ip   (str)        : The IP address of the server.
			server_port (str)        : The Port of the server.
			debug       (bool)       : Whether debug prints should be enabled.
			consoleMode (bool)       : Whether the program uses the console/keyboard or the buttonpad and oled.
		"""

		self.debug = debug
		self.consoleMode = consoleMode

		# Headset API Interface
		# headsetInterface = ClientInterfaceDriver(server_ip, server_port) # CDL=> Replace with client later
		self.headsetInterface = HeadsetAPIWrapper()

		# System Mode
		self.currentMode = ModeType.INITIALIZATION_MODE

	def initializationMode(self):
		"""The user logic for the initialization mode."""
		# CDL=> Move arm to default position
		# CDL=> Update mode on oled
		printMessage("Entering Profile Selection Mode")
		self.currentMode = ModeType.PROFILE_SELECTION_MODE

	def profileSelectionMode(self):
		"""The user logic for the profile selection mode."""

		# Get a list of all the profiles
		profileList = self.headsetInterface.listProfiles()

		printMessage("--------Select or Create a Profile---------")

		userInput = promptUserInput("Type select or create: ").lower()

		if userInput == "select":
			profileName = promptUserList("Current Profile List:", profileList)
			if profileName:
				message = ""
				if keyboardPluggedIn():
					message = "What would you like to do with the profile? Type Load, Delete, Rename, or Train: "
				else:
					message = "What would you like to do with the profile? Type Load, Delete, or Train: "

				userInput = promptUserInput(message).lower()

				if userInput == "load":
					self.headsetInterface.selectProfile(profileName)
					printMessage("Entering Live Mode")
					self.currentMode = ModeType.LIVE_MODE

				elif userInput == "train":
					self.headsetInterface.selectProfile(profileName)
					printMessage("Entering Training Mode")
					self.currentMode = ModeType.TRAINING_MODE

				elif keyboardPluggedIn() and userInput == "rename":
					userInput = promptUserInput("Enter a new profile name: ")
					self.headsetInterface.renameProfile(profileName, userInput)
					printMessage("Profile {} renamed to {}".format(profileName, userInput))

				elif userInput == "delete":
					userInput = promptUserInput("Are you sure you want to delete? (yes or no): ").lower()
					if userInput == "yes":
						self.headsetInterface.deleteProfile(profileName)
					else:
						printMessage("Canceling delete operation for {}".format(profileName))

				else:
					printMessage("\nInvalid Input. Please try again!\n")
			else:
				printMessage("\nInvalid Input. Please try again!\n")

		elif userInput == "create":
			newProfileName = ""
			if keyboardPluggedIn():
				newProfileName = promptUserInput("Enter a new profile name: ")
			else:
				i = 0
				# Generate new profile name with next lowest number
				while True:
					newProfileName = "New Profile {}".format(i)
					if newProfileName not in profileList:
						break
					else:
						i += 1

			self.headsetInterface.createProfile(newProfileName)
			printMessage("Profile {} created".format(newProfileName))

	def trainingMode(self):
		"""The user logic for the training mode."""

		userInput = promptUserList("Do you want to exit to live mode, train this profile, or clear all training?", ["clear", "train", "exit"])

		if userInput == "clear":
			printMessage("Deleting training data for {} profile".format(self.headsetInterface.getSelectedProfile()))
			self.headsetInterface.clearAll() # CDL=> WE NEED TO MAKE THIS!

		if userInput == "train":
			while True:
				# Get list of trainable list of actions
				actionList = list(self.headsetInterface.getSigTrainedAct().keys()) # CDL=> Add number of times trained

				action = promptUserList("Select an action to train or reset: ", actionList)

				trainDelete = promptUserList("Do you want to train or delete training for the action?", ["train", "delete"])

				if trainDelete == "delete":
					# CDL=> Add "are you sure you want to yadayada"
					self.headsetInterface.trainProfile(action, "mentalCommand", "erase")
					printMessage("Training Data deleted for {} action".format(action))

				elif trainDelete == "train":
					printMessage("Please think about or move with selected action: {}".format(action))

					# CDL=> Add button press later for user is ready

					# Start the training for specific action
					self.headsetInterface.trainProfile(action, "mentalCommand", "start")

					# Training running
					acceptReject = promptUserList("Training Complete! Do you want to accept or reject the training? ", ["accept", "reject"])

					if acceptReject == "accept":
						# Accept the training for specific action
						self.headsetInterface.trainProfile(action, "mentalCommand", "accept")
						printMessage("Training accepted")

					elif acceptReject == "reject":
						self.headsetInterface.trainProfile(action, "mentalCommand", "reset")
						printMessage("Training rejected")

					# Check if done or train again
					doneNotDone = promptUserList("Are you done or do you want to continue training this action again? ", ["done", "continue"])

					if doneNotDone == "done":
						break

		if userInput == "exit":
			printMessage("Entering Live Mode")
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


