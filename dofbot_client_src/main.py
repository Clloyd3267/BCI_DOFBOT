import enum
import time
from ClientInterfaceDriver import *
from SmartSockets.SmartSocket import *
import keyboard

#from oledDriver import *


class modeType(enum.Enum):  # creating enumerations with class
	Initializing = 1
	Profile_Select = 2
	Training_Mode = 3
	Live_Mode = 4

def keyboardPluggedIn():
	return True


# oledDriver = Draw()

# Draw.printToOled()


# oledDriver = Draw()


def main():
	previousMode = None
	currentMode = modeType.Initializing  # set default mode to Initialization
	#oledDriver = Draw()
	while True:
		
		if currentMode == modeType.Initializing:
			print(modeType.Initializing.name)      # print name of enumeration
			#oledDriver.printToOled(modeType.Initializing.name)
			currentMode = modeType.Profile_Select
		elif currentMode == modeType.Profile_Select:
			createProfile = server.createProfile()
			profileList = server.listProfiles()
			
			print("--------Select or Create a Profile---------")
			userInput = input("Type Select or Create")

			if userInput == 'select':
				print("Current Profile List:")
				print("Index | Profile Name")
				for index, value in enumerate(profileList):
					print ("{} | {}".format(index, value))
			elif userInput == 'create':
				
				print('Name Profile')


			# print(modeType.Profile_Select.name)
			#oledDriver.printToOled(modeType.Profile_Select.name)
			#if input('t'):            # trained
				#currentMode = modeType.Live_Mode
			#if input('u'):            # untrained
				#currentMode = modeType.Training_Mode
		elif currentMode == modeType.Training_Mode:
			#print(modeType.Training_Mode.name)
			#oledDriver.printToOled(modeType.Training_Mode.name)
			currentMode = modeType.Live_Mode
		# elif currentMode == modeType.Live_Mode:
		# print(modeType.Live_Mode.name)
		# oledDriver.printToOled(modeType.Live_Mode.name)
		if previousMode != currentMode:
			print(currentMode.name)
		previousMode = currentMode


if __name__ == '__main__':
	main()