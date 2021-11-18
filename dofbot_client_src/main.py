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


# Connection information
server_ip = "128.153.178.74" # CDL=> My IP (headset system)
server_port = 42070

# Create a client socket
server = ClientInterfaceDriver(server_ip, server_port)

myClient = SmartSocket(server_ip, 42071, SocketType.CLIENT)


def main():
	previousMode = None
	currentMode = modeType.Initializing  # set default mode to Initialization
	#oledDriver = Draw()
	while True:
		getSelectedProfile = server.getSelectedProfile()

		if currentMode == modeType.Initializing:
			print(modeType.Initializing.name)      # print name of enumeration
			#oledDriver.printToOled(modeType.Initializing.name)
			currentMode = modeType.Profile_Select
		elif currentMode == modeType.Profile_Select:
			createProfile = server.createProfile()
			profileList = server.listProfiles()
			deleteProfile = server.deleteProfile()
			deselectProfile = server.deselectProfile()
			selectProfile = server.selectProfile()
			renameProfile = server.renameProfile()
			


			print("--------Select or Create a Profile---------")
			userInput = input("Type select or create").lower()

			if userInput == 'select':
				print("Current Profile List:")
				print("Index | Profile Name")
				for index, value in enumerate(profileList):
					print ("{} | {}".format(index, value))

					userInput = input("Input the index of the profile to select: ").lower()

				if userInput.isnumeric() and 0 <= int(userInput) < len(profileList):
					profileName = profileList[int(userInput)]
					print("Profile {} selected".format(profileName))
					if keyboardPluggedIn():
						userInput = input("What would you like to do with the profile? Type Load, Delete, Rename, or Train: ").lower()
					else:
						userInput = input("What would you like to do with the profile? Type Load, Delete, or Train: ").lower()
					if userInput == 'Load':
						print("Going to Live mode")
						server.selectProfile(profileName)
						currentMode = modeType.Live_Mode
					elif userInput == 'Train':
						print("Going to Training Mode")
						server.selectProfile(profileName)
						currentMode = modeType.Training_Mode
					elif keyboardPluggedIn() and userInput == 'Rename':
						userInput = input("Enter a new profile name: ")
						server.renameProfile(profileName, userInput)
						print("Profile {} renamed to {}".format(profileName, userInput))	
					elif userInput == 'Delete':
						userInput = input("Are you sure you want to delete?").lower()
						if userInput == 'yes':
							server.deleteProfile(profileName)
						else:
							print("Canceling delete operation for {}".format(profileName))
					else:
						print("\nInvalid Input. Please try again!\n")
				else:
					print("\nInvalid Input. Please try again!\n")

			elif userInput == 'create':
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
				server.createProfile(newProfileName)
				print("Profile {} created".format(newProfileName))

			#oledDriver.printToOled(modeType.Profile_Select.name)
		elif currentMode == modeType.Training_Mode:
			print(modeType.Training_Mode.name)
			trainProfile = server.trainProfile()
			

			#oledDriver.printToOled(modeType.Training_Mode.name)
			currentMode = modeType.Live_Mode
		elif currentMode == modeType.Live_Mode:
			print("===================== Live Inferencing =====================")

			# Start Live Mode
			status, message = server.startInferencing()

			print(message)
			prevAction = ""
			while True:
				message = myClient.receiveMessage()
				if not message:
					continue
				else:
					action = message.decode()
					if prevAction == action:
						pass
					elif action == "neutral":
						pass
					elif action == "lift":
						control.grab_and_get()
						time.sleep(1)
					elif action == "drop":
						control.put_back()
						time.sleep(1)
					elif action == "disappear":
						control.take_picture()
						time.sleep(1)
					else:
						print("Invalid Inference")
					prevAction = action
			# except KeyboardInterrupt:
			# 	print("Caught Keyboard interrupt")

			# finally:
			# 	print("Exiting!")
			# 	# Stop Live Mode
			# 	status, message = server.stopInferencing()

			# 	print(message)

			# 	server.serverSmartSocket.closeSocket()
		

		# print(modeType.Live_Mode.name)
		# oledDriver.printToOled(modeType.Live_Mode.name)
		#if previousMode != currentMode:
			#print(currentMode.name)
		#previousMode = currentMode


if __name__ == '__main__':
	main()
