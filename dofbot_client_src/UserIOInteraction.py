# ------------------------------------------------------------------------------
# Name         : UserIOInteraction.py
# Date Created : 11/19/2021
# Author(s)    : Chris Lloyd, Josiah Schmidt, Camilla Ketola, Dylan Shuhart
# Description  : User interface logic for interacting with a user.
#                Can all be through console or partially through OLED/GPIO buttons.
# ------------------------------------------------------------------------------

# Imports
import OLEDDriver
import IODriver
import os

class UserIOInteraction:
	"""
	This class controls the user interface logic.

	Attributes:
		consoleMode (bool)       : Whether the program uses the console/keyboard
		                           or the buttonpad and oled.
		oled        (OLEDDriver) : The OLED library for display information to the oled screen.
	"""

	def __init__(self, consoleMode=True):
		"""
		The default constructor for class UserIOInteraction.

		Arguments:
			consoleMode (bool) : Whether the program uses the console/keyboard
			                     or the buttonpad and oled.
		"""
		self.consoleMode = consoleMode

		if not self.consoleMode:
			self.oled = OLEDDriver.OLEDDriver()
			IODriver.initPollingEdge(IODriver.UP_BTN)
			IODriver.initPollingEdge(IODriver.DN_BTN)
			IODriver.initPollingEdge(IODriver.LF_BTN)
			IODriver.initPollingEdge(IODriver.RT_BTN)
			IODriver.initPollingEdge(IODriver.RST_BTN)
			IODriver.initPollingEdge(IODriver.PRF_SEL_BTN)

		self.profile = ""
		self.mode    = ""

	def keyboardPluggedIn(self):
		"""
		Check if a keyboard is plugged in.

		Returns:
			Boolean of whether a keyboard is plugged in.
		"""

		# CDL=> Add exception/warning if OS is not Linux
		deviceList = os.popen("usb-devices | grep 'S:  Product='")
		devices = deviceList.read()
		return "Keyboard" in devices

	def updateMode(self, mode):
		self.mode = mode
		self.oled.printToLine(0, (self.mode[:7].ljust(7) + " | " + self.profile))

	def updateProfile(self, profile):
		self.profile = profile
		self.oled.printToLine(0, (self.mode[:7].ljust(7) + " | " + self.profile))

	def printMessage(self, message, waitKey=True):
		"""
		Print message.

		Arguments:
			message (str)  : The message to print.
			waitKey (bool) : Whether to force user to press a key to continue
		"""

		if self.consoleMode:
			print(message, "\n")
		else:
			self.oled.clearDisplay("12")
			self.oled.printToLine(1, message[:OLEDDriver.MAX_LINE_WIDTH])
			self.oled.printToLine(2, message[OLEDDriver.MAX_LINE_WIDTH:])
			if waitKey:
				while not (IODriver.isPressed(IODriver.UP_BTN) or
						   IODriver.isPressed(IODriver.DN_BTN) or
						   IODriver.isPressed(IODriver.LF_BTN) or
						   IODriver.isPressed(IODriver.RT_BTN)):
					if   IODriver.isPressed(IODriver.RST_BTN):     # Reset Pressed
						self.oled.clearDisplay("12")
						return IODriver.RST_BTN
					elif IODriver.isPressed(IODriver.PRF_SEL_BTN): # Profile Selection Pressed
						self.oled.clearDisplay("12")
						return IODriver.PRF_SEL_BTN
				return None

	def promptUserInput(self, message):
		"""
		Prompt user for input.

		Arguments:
			message (str) : The message to prompt.

		Returns:
			The string the user typed in.
		"""

		# Only allow user input if in console mode or a keyboard is plugged in
		if self.consoleMode or self.keyboardPluggedIn():
			value = input(message)
			print() # Add extra linebreak after section
			return value
		else:
			print("No Keyboard plugged in. No way to get user input!\n")
			return None

	def promptUserList(self, message, inputList):
		"""
		Prompt user to select value in a list.

		Arguments:
			message   (str)         : The message to prompt.
			inputList (list of str) : The list to select from.

		Returns:
			The string the user selected from the list.
		"""

		if not inputList:
			return None
		elif self.consoleMode:
			while True:
				print(message)
				print("-" * len(message))
				print("Index | Value")
				for index, value in enumerate(inputList):
					print ("{:<5} | {}".format(index, value))

				userInput = input("\nInput the index of the value to select: ")
				print() # Add extra linebreak after section

				if userInput.isnumeric() and 0 <= int(userInput) < len(inputList):
					return inputList[int(userInput)]
				else:
					print("Invalid Input. Please try again!\n")
		else:
			index = 0
			self.oled.clearDisplay("12")
			self.oled.printToLine(1, message.center(OLEDDriver.MAX_LINE_WIDTH, '-'))
			self.oled.printToLine(2, "< {} >".format(inputList[index]).center(OLEDDriver.MAX_LINE_WIDTH))

			while True:
				if   IODriver.isPressed(IODriver.RST_BTN):     # Reset Pressed
					self.oled.clearDisplay("12")
					return IODriver.RST_BTN
				elif IODriver.isPressed(IODriver.PRF_SEL_BTN): # Profile Selection Pressed
					self.oled.clearDisplay("12")
					return IODriver.PRF_SEL_BTN

				elif IODriver.isPressed(IODriver.UP_BTN):      # Enter Pressed
					self.oled.clearDisplay("12")
					return inputList[index]

				elif IODriver.isPressed(IODriver.LF_BTN):      # Left Pressed
					if index == 0:
						index = len(inputList) - 1
					else:
						index -= 1

					self.oled.printToLine(2, "< {} >".format(inputList[index]).center(OLEDDriver.MAX_LINE_WIDTH))

				elif IODriver.isPressed(IODriver.RT_BTN):      # Right Pressed
					if index == len(inputList) - 1:
						index = 0
					else:
						index += 1

					self.oled.printToLine(2, "< {} >".format(inputList[index]).center(OLEDDriver.MAX_LINE_WIDTH))


