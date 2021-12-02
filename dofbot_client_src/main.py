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
	    headsetInterface (ClientInterfaceDriver) : The headset interface.
		userIO           (UserIOInteraction)     : The user interaction interface.
	    currentMode      (ModeType enum)         : The IP address of the server.
	    debug            (bool)                  : Whether debug prints should be enabled.
	    consoleMode      (bool)                  : Whether the program uses the console/keyboard
	                                               or the buttonpad and oled.
	"""

	def __init__(self, server_ip, server_port, debug=True, consoleMode=True):
		"""
		The default constructor for class DofbotSubsystem.

		Arguments:
		    server_ip   (str)        : The IP address of the server.
		    server_port (str)        : The Port of the server.
		    debug       (bool)       : Whether debug prints should be enabled.
		    consoleMode (bool)       : Whether the program uses the console/keyboard or the buttonpad and oled.
		"""

		self.debug = debug
		self.consoleMode = consoleMode # CDl=> Use this later

		# Headset API interface
		# headsetInterface = ClientInterfaceDriver(server_ip, server_port) # CDL=> Replace with client later
		self.headsetInterface = HeadsetAPIWrapper()

		# User interaction object
		self.userIO = UserIOInteraction(consoleMode)

		# Set default system mode
		self.setCurrentMode(ModeType.INITIALIZATION_MODE)

	def setCurrentMode(self, mode):
		"""
		Function to change the current mode of the system.

		Arguments:
		    mode (ModeType enum) : The mode to change to.
		"""

		self.currentMode = mode
		# CDL=> Update mode on oled
		if self.debug: print("Entering mode {}\n".format(self.currentMode.name))

	def initializationMode(self):
		"""The user logic for the initialization mode."""

		# CDL=> Move arm to default position
		self.setCurrentMode(ModeType.PROFILE_SELECTION_MODE)

	def profileSelectionMode(self):
		"""The user logic for the profile selection mode."""

		# Get a list of all the profiles
		profileList = self.headsetInterface.listProfiles()

		userInput = self.userIO.promptUserList("Do you want to select or create a profile?", ["select", "create"])

		if userInput == "select":
			profileName = self.userIO.promptUserList("Current Profile List:", profileList)
			if profileName:
				options = ""
				if self.userIO.keyboardPluggedIn():
					options = ["load", "delete", "rename", "train"]
				else:
					options = ["load", "delete", "train"]

				userInput = self.userIO.promptUserList("What would you like to do with the profile?", options)

				if userInput == "load":
					self.headsetInterface.selectProfile(profileName)
					self.setCurrentMode(ModeType.LIVE_MODE)

				elif userInput == "train":
					self.headsetInterface.selectProfile(profileName)
					self.setCurrentMode(ModeType.TRAINING_MODE)

				elif self.userIO.keyboardPluggedIn() and userInput == "rename":
					userInput = self.userIO.promptUserInput("Enter a new profile name: ")
					self.headsetInterface.renameProfile(profileName, userInput)
					self.userIO.printMessage("Profile {} renamed to {}".format(profileName, userInput))

				elif userInput == "delete":
					userInput = self.userIO.promptUserList("Are you sure you want to delete profile {}?".format(profileName), ["no", "yes"])
					if userInput == "yes":
						self.headsetInterface.deleteProfile(profileName)
						self.userIO.printMessage("Profile {} deleted".format(profileName))
					else:
						self.userIO.printMessage("Canceling delete operation for {}".format(profileName))

				else:
					self.userIO.printMessage("Invalid Input. Please try again!")
			else:
				self.userIO.printMessage("Invalid Input. Please try again!")

		elif userInput == "create":
			newProfileName = ""
			if self.userIO.keyboardPluggedIn():
				newProfileName = self.userIO.promptUserInput("Enter a new profile name: ")
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
			self.userIO.printMessage("Profile {} created".format(newProfileName))

	def trainingMode(self):
		"""The user logic for the training mode."""

		userInput = self.userIO.promptUserList("Do you want to exit to live mode, train this profile, or clear all training?", ["clear", "train", "exit"])

		if userInput == "clear":
			userInput = self.userIO.promptUserList("Are you sure you want to delete all training data for profile {}?".format(self.headsetInterface.getSelectedProfile()), ["no", "yes"])

			if userInput == "yes":
				self.headsetInterface.clearAll() # CDL=> WE NEED TO MAKE THIS!
				self.userIO.printMessage("Training data deleted for profile {}?".format(self.headsetInterface.getSelectedProfile()))
			else:
				self.userIO.printMessage("Canceling delete operation for profile {}?".format(self.headsetInterface.getSelectedProfile()))

		elif userInput == "train":
			while True:
				# Get list of trainable list of actions
				actionList = list(self.headsetInterface.getSigTrainedAct().keys()) # CDL=> Add number of times trained

				action = self.userIO.promptUserList("Select an action to train or reset: ", actionList)

				trainDelete = self.userIO.promptUserList("Do you want to train or delete training for the action {}?".format(action), ["train", "delete"])

				if trainDelete == "delete":
					userInput = self.userIO.promptUserList("Are you sure you want to delete all training data for action {}?".format(action), ["no", "yes"])

					if userInput == "yes":
						self.headsetInterface.trainProfile(action, "mentalCommand", "erase")
						self.userIO.printMessage("Training data deleted for action {}".format(action))
					else:
						self.userIO.printMessage("Canceling delete operation for action {}".format(action))

				elif trainDelete == "train":
					self.userIO.printMessage("Please think about or move with selected action: {}".format(action))

					# CDL=> Add button press later for user is ready

					# Start the training for specific action
					self.headsetInterface.trainProfile(action, "mentalCommand", "start")

					# Training running
					acceptReject = self.userIO.promptUserList("Training Complete! Do you want to accept or reject the training? ", ["accept", "reject"])

					if acceptReject == "accept":
						# Accept the training for specific action
						self.headsetInterface.trainProfile(action, "mentalCommand", "accept")
						self.userIO.printMessage("Training accepted")

					elif acceptReject == "reject":
						self.headsetInterface.trainProfile(action, "mentalCommand", "reset")
						self.userIO.printMessage("Training rejected")

					# Check if done or train again
					doneNotDone = self.userIO.promptUserList("Are you done or do you want to continue training this action again? ", ["done", "continue"])

					if doneNotDone == "done": break

		elif userInput == "exit":
			self.setCurrentMode(ModeType.LIVE_MODE)

	def liveMode(self):
		"""The user logic for the live mode."""

		# Start Live Mode
		self.headsetInterface.startInferencing()

		while True:
			status, message, action, __, __ = self.headsetInterface.receiveInference()
			if isPressed(rstButton):
				self.headsetInterface.stopInferencing()
				self.setCurrentMode(ModeType.INITIALIZATION_MODE)
				break
			elif isPressed(ProfileSltButton):
				self.headsetInterface.stopInferencing()
				self.setCurrentMode(ModeType.PROFILE_SELECTION_MODE)
				break
			elif not status:
				self.userIO.printMessage(message)
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
			# CDL=> Add more actions!
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
			print("Exception occurred. Exiting!!!")

if __name__ == "__main__":
	# Connection information
	server_ip = "128.153.178.74"
	server_port = 42070

	dofbotSubsystem = DofbotSubsystem(server_ip, server_port)
	dofbotSubsystem.main()


