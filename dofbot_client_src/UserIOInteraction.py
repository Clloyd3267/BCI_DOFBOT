# ------------------------------------------------------------------------------
# Name         : UserIOInteraction.py
# Date Created : 11/19/2021
# Author(s)    : Chris Lloyd, Josiah Schmidt, Camilla Ketola, Dylan Shuhart
# Description  : User interface logic for interacting with a user.
#                Can all be through console or partially through OLED/GPIO buttons.
# ------------------------------------------------------------------------------

#Imports

class UserIOInteraction:
	"""
	This class controls the user interface logic.

	Attributes:
	    consoleMode (bool) : Whether the program uses the console/keyboard
	                         or the buttonpad and oled.
	"""

	def __init__(self, consoleMode=True):
		"""
		The default constructor for class UserIOInteraction.

		Arguments:
		    consoleMode (bool) : Whether the program uses the console/keyboard
		                         or the buttonpad and oled.
		"""
		self.consoleMode = consoleMode

	def keyboardPluggedIn(self):
		"""
		Check if a keyboard is plugged in.

		Returns:
		    Boolean of whether a keyboard is plugged in.
		"""
		# CDL=> Add exception/warning if OS is not Linux
		return True # CDL=> Replace with final version later!

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

		if self.consoleMode:
			value = input(message)
			print() # Add extra linebreak after section
			return value
		elif self.keyboardPluggedIn(): # CDl=> Add this function in
			return None # CDL=> Add OLED version later
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
			return None # CDL=> Add OLED version later

