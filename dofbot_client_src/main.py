# ------------------------------------------------------------------------------
# Name         : main.py
# Date Created : 12/01/2021
# Author(s)    : Chris Lloyd, Josiah Schmidt, Camilla Ketola, Dylan Shuhart
# Description  : Client main code for BCI Dofbot (EEG Controlled Robotic Arm).
# ------------------------------------------------------------------------------

# Imports
# from ClientInterfaceDriver import *
from HeadsetAPIWrapperTest import *
from UserIOInteraction import *
import control
import enum
import time

class ModeType(enum.Enum):
	"""Simple Enumeration class to store system modes."""
	INITIALIZATION_MODE    = "INIT"
	PROFILE_SELECTION_MODE = "PRF SEL"
	TRAINING_MODE          = "TRAIN"
	LIVE_MODE              = "LIVE"

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

	def __init__(self, server_ip, server_port, debug=True, consoleMode=False):
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

		# Headset API interface
		# self.headsetInterface = ClientInterfaceDriver(server_ip, server_port) # CDL=> Replace with client later
		self.headsetInterface = HeadsetAPIWrapper()

		# User interaction object
		self.userIO = UserIOInteraction(consoleMode)

		# Set default system mode
		self.setCurrentMode(ModeType.INITIALIZATION_MODE)

	def handler(self, pin):
		"""
		Handler function for GPIO inputs.

		Arguments:
			pin (int) : The pin that caused the interrupt.
		"""

		if pin == IODriver.RST_BTN:
			self.setCurrentMode(ModeType.INITIALIZATION_MODE)
			return False
		elif pin == IODriver.PRF_SEL_BTN:
			self.setCurrentMode(ModeType.PROFILE_SELECTION_MODE)
			return False
		else:
			return True

	def setCurrentMode(self, mode):
		"""
		Function to change the current mode of the system.

		Arguments:
			mode (ModeType enum) : The mode to change to.
		"""

		self.currentMode = mode

		# Update mode on oled
		self.userIO.updateMode(self.currentMode.value)

		if self.debug: print("Entering mode {}\n".format(self.currentMode.name))

	def initializationMode(self):
		"""The user logic for the initialization mode."""

		# Move arm to default position
		control.default()
		time.sleep(0.5)
		control.close_hand()
		time.sleep(0.5)
		control.open_hand()
		if IODriver.isPressed(IODriver.RST_BTN): pass
		if IODriver.isPressed(IODriver.PRF_SEL_BTN): pass

		self.userIO.updateProfile("")
		self.setCurrentMode(ModeType.PROFILE_SELECTION_MODE)

	def profileSelectionMode(self):
		"""The user logic for the profile selection mode."""

		self.userIO.updateProfile("")

		# Get a list of all the profiles
		profileList = self.headsetInterface.listProfiles()

		# Add create new option to profile list
		profileList.append("<Create New>")

		profileName = self.userIO.promptUserList("Select Profile", profileList)

		if not self.handler(profileName): return  # Break out of function

		elif profileName == "<Create New>":
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
			pin = self.userIO.printMessage("Profile {} created".format(newProfileName))
			if not self.handler(pin): return  # Break out of function

		else:
			options = ""
			if self.userIO.keyboardPluggedIn():
				options = ["load", "delete", "rename", "train"]
			else:
				options = ["load", "delete", "train"]

			userInput = self.userIO.promptUserList("Choose Operation", options)

			if not self.handler(userInput): return  # Break out of function

			elif userInput == "load":
				self.headsetInterface.selectProfile(profileName)
				self.userIO.updateProfile(profileName)
				self.setCurrentMode(ModeType.LIVE_MODE)

			elif userInput == "train":
				self.headsetInterface.selectProfile(profileName)
				self.setCurrentMode(ModeType.TRAINING_MODE)

			elif self.userIO.keyboardPluggedIn() and userInput == "rename":
				userInput = self.userIO.promptUserInput("New profile name: ")
				self.headsetInterface.renameProfile(profileName, userInput)
				pin = self.userIO.printMessage("Profile {} renamed to {}".format(profileName, userInput))
				if not self.handler(pin): return  # Break out of function

			elif userInput == "delete":
				userInput = self.userIO.promptUserList("Delete Prf {}?".format(profileName), ["no", "yes"])

				if not self.handler(userInput): return  # Break out of function

				elif userInput == "yes":
					self.headsetInterface.deleteProfile(profileName)
					pin = self.userIO.printMessage("Profile {} deleted".format(profileName))
					if not self.handler(pin): return  # Break out of function

				else:
					pin = self.userIO.printMessage("Canceling delete operation for {}".format(profileName))
					if not self.handler(pin): return  # Break out of function

			else:
				pin = self.userIO.printMessage("Invalid Input. Please try again!")
				if not self.handler(pin): return  # Break out of function

	def trainingMode(self):
		"""The user logic for the training mode."""

		__, __, selectedProfile = self.headsetInterface.getSelectedProfile()

		userInput = self.userIO.promptUserList("Choose Operation", ["clear", "train", "exit"])

		if not self.handler(userInput): return  # Break out of function

		elif userInput == "clear":
			userInput = self.userIO.promptUserList("Clr Prf {}?".format(selectedProfile), ["no", "yes"])

			if not self.handler(userInput): return  # Break out of function

			elif userInput == "yes":
				self.headsetInterface.clearAllTrainingData(selectedProfile)
				pin = self.userIO.printMessage("Training data deleted for profile {}?".format(selectedProfile))
				if not self.handler(pin): return  # Break out of function

			else:
				pin = self.userIO.printMessage("Canceling delete operation for profile {}?".format(selectedProfile))
				if not self.handler(pin): return  # Break out of function

		elif userInput == "train":
			# Get list of trainable list of actions
			actionList = list(self.headsetInterface.getTrainedActions().keys()) # CDL=> Add number of times trained

			action = self.userIO.promptUserList("Choose Action", actionList)

			if not self.handler(action): return  # Break out of function

			trainDelete = self.userIO.promptUserList("Choose Operation".format(action), ["train", "delete"])

			if not self.handler(trainDelete): return  # Break out of function

			elif trainDelete == "delete":
				userInput = self.userIO.promptUserList("Del Training Data?".format(action), ["no", "yes"])

				if not self.handler(userInput): return  # Break out of function

				elif userInput == "yes":
					self.headsetInterface.trainProfile(action, "mentalCommand", "erase")
					pin = self.userIO.printMessage("Training data deleted for action {}".format(action))
					if not self.handler(pin): return  # Break out of function

				else:
					pin = self.userIO.printMessage("Canceling delete operation for action {}".format(action))
					if not self.handler(pin): return  # Break out of function

			elif trainDelete == "train":
				while True:
					pin = self.userIO.printMessage("Perform {} action".format(action))
					if not self.handler(pin): return  # Break out of function

					# Start the training for specific action
					self.headsetInterface.trainProfile(action, "mentalCommand", "start")

					# Training running
					acceptReject = self.userIO.promptUserList("Choose Operation", ["accept", "reject"])

					if not self.handler(acceptReject): return  # Break out of function

					elif acceptReject == "accept":
						# Accept the training for specific action
						self.headsetInterface.trainProfile(action, "mentalCommand", "accept")
						pin = self.userIO.printMessage("Training accepted")
						if not self.handler(pin): return  # Break out of function

					elif acceptReject == "reject":
						self.headsetInterface.trainProfile(action, "mentalCommand", "reset")
						pin = self.userIO.printMessage("Training rejected")
						if not self.handler(pin): return  # Break out of function

					# Check if done or train again
					userInput = self.userIO.promptUserList("Done Training Action", ["done", "continue"])

					if not self.handler(userInput) or userInput == "done": return  # Break out of function

		elif userInput == "exit":
			self.setCurrentMode(ModeType.LIVE_MODE)

	def liveMode(self):
		"""The user logic for the live mode."""

		# Get an inferencing action from headset
		status, message, action, __, __ = self.headsetInterface.receiveInference()

		if   IODriver.isPressed(IODriver.RST_BTN):     # Reset Pressed
			self.setCurrentMode(ModeType.INITIALIZATION_MODE)

		elif IODriver.isPressed(IODriver.PRF_SEL_BTN): # Profile Selection Pressed
			self.setCurrentMode(ModeType.PROFILE_SELECTION_MODE)

		elif not status:
			print(message)
		elif action == "neutral":
			self.userIO.printMessage("Live Action:".center(OLEDDriver.MAX_LINE_WIDTH) + action.center(OLEDDriver.MAX_LINE_WIDTH), waitKey=False)
		elif action == "lift":
			self.userIO.printMessage("Live Action:".center(OLEDDriver.MAX_LINE_WIDTH) + action.center(OLEDDriver.MAX_LINE_WIDTH), waitKey=False)
			control.grab_and_get()
			time.sleep(0.5)
			if IODriver.isPressed(IODriver.RST_BTN): pass
			if IODriver.isPressed(IODriver.PRF_SEL_BTN): pass
		elif action == "drop":
			self.userIO.printMessage("Live Action:".center(OLEDDriver.MAX_LINE_WIDTH) + action.center(OLEDDriver.MAX_LINE_WIDTH), waitKey=False)
			control.put_back()
			time.sleep(0.5)
			if IODriver.isPressed(IODriver.RST_BTN): pass
			if IODriver.isPressed(IODriver.PRF_SEL_BTN): pass
		elif action == "disappear":
			self.userIO.printMessage("Live Action:".center(OLEDDriver.MAX_LINE_WIDTH) + action.center(OLEDDriver.MAX_LINE_WIDTH), waitKey=False)
			control.take_picture()

		# CDL=> Add more actions!
		else:
			self.userIO.printMessage("Invalid Inference:".center(OLEDDriver.MAX_LINE_WIDTH) + action.center(OLEDDriver.MAX_LINE_WIDTH))

		time.sleep(1) # CDL=> Sleep for 250ms?

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
					# Start Live Mode
					self.headsetInterface.startInferencing()

					# Loop through Live Mode
					while self.currentMode == ModeType.LIVE_MODE:
						self.liveMode()

					# Stop Live Mode
					self.headsetInterface.stopInferencing()

		except KeyboardInterrupt:
			print("Keyboard Interrupt issued. Exiting!")

		except Exception as e:
			print("Exception {} occurred. Exiting!".format(e))

if __name__ == "__main__":
	# Connection information
	server_ip = "128.153.183.36"
	server_port = 42070

	dofbotSubsystem = DofbotSubsystem(server_ip, server_port)
	dofbotSubsystem.main()
