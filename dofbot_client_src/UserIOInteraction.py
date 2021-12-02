# ------------------------------------------------------------------------------
# Name         : UserIOInteraction.py
# Date Created : 11/4/2021
# Author(s)    : Chris Lloyd, Josiah Schmidt, Camilla Ketola, Dylan Shuhart
# Description  : CDL=> Here
# ------------------------------------------------------------------------------

#Imports


def printMessage(message):
    print(message)
def promptUserInput(message):
    return input(message)
def promptUserList(message, inputList):
	print(message)
	print("Index | Value")
	for index, value in enumerate(inputList):
		print ("{} | {}".format(index, value))

	userInput = input("Input the index of the value to select: ").lower()

	if userInput.isnumeric() and 0 <= int(userInput) < len(inputList): #cdl
		return inputList[int(userInput)]
	else:
		return None

