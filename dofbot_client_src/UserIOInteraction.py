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

	def printMessage(self, message):
		"""
		Print message.

		Arguments:
			message (str) : The message to print.
		"""

		if self.consoleMode:
			print(message, "\n")
		else:
			pass # CDL=> Add OLED version later

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
			self.oled.clearDisplay(None)
			self.oled.printTo3Line(1, message)
			self.oled.printTo3Line(2, "< {} >".format(inputList[index]).center(OLEDDriver.MAX_LINE_WIDTH))

			while True:

				if   IODriver.isPressed(IODriver.BTN_A_PIN):  # Enter Pressed
					return inputList[index]

				elif IODriver.isPressed(IODriver.BTN_B_PIN):  # Left Pressed
					if index == 0:
						index = len(inputList) - 1
					else:
						index -= 1

					self.oled.printTo3Line(2, "< {} >".format(inputList[index]).center(OLEDDriver.MAX_LINE_WIDTH))

				elif IODriver.isPressed(IODriver.BTN_C_PIN):  # Right Pressed
					if index == len(inputList) - 1:
						index = 0
					else:
						index += 1

					self.oled.printTo3Line(2, "< {} >".format(inputList[index]).center(OLEDDriver.MAX_LINE_WIDTH))


