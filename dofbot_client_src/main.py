import enum
import time
#from ClientInterfaceDriver import *
from HeadsetAPIWrapperTest import *

#from oledDriver import *


class modeType(enum.Enum):  # creating enumerations with class
	Initializing = 1
	Profile_Select = 2
	Training_Mode = 3
	Live_Mode = 4

def keyboardPluggedIn():
	return True


# # Connection information
# server_ip = "128.153.178.74" # CDL=> My IP (headset system)
# server_port = 42070

# # Create a client socket
# server = ClientInterfaceDriver(server_ip, server_port)

# myClient = SmartSocket(server_ip, 42071, SocketType.CLIENT)


def main():
	previousMode = None
	currentMode = modeType.Initializing  # set default mode to Initialization
	headsetAPIWrapper = HeadsetAPIWrapper()
	#oledDriver = Draw()
	while True:
		if currentMode == modeType.Initializing:
			print(modeType.Initializing.name)      # print name of enumeration
			#oledDriver.printToOled(modeType.Initializing.name)
			currentMode = modeType.Profile_Select
		elif currentMode == modeType.Profile_Select:
			profileList = headsetAPIWrapper.listProfiles()
		
			print("--------Select or Create a Profile---------")
			userInput = input("Type select or create: ").lower()

			if userInput == 'select':
				print("Current Profile List:")
				print("Index | Profile Name")
				for index, value in enumerate(profileList):
					print ("{} | {}".format(index, value))

				userInput = input("Input the index of the profile to select: ").lower()

				if userInput.isnumeric() and 0 <= int(userInput) < len(profileList):
					profileName = profileList[int(userInput)]
					print("Profile {} selected".format(profileName))
					message = ""
					if keyboardPluggedIn():
						message = "What would you like to do with the profile? Type Load, Delete, Rename, or Train: "
					else:
						message = "What would you like to do with the profile? Type Load, Delete, or Train: "

					userInput = input(message).lower()

					if userInput == "load":
						print("Going to Live mode")
						headsetAPIWrapper.selectProfile(profileName)
						currentMode = modeType.Live_Mode
					elif userInput == "train":
						print("Going to Training Mode")
						headsetAPIWrapper.selectProfile(profileName)
						currentMode = modeType.Training_Mode
					elif keyboardPluggedIn() and userInput == "rename":
						userInput = input("Enter a new profile name: ")
						headsetAPIWrapper.renameProfile(profileName, userInput)
						print("Profile {} renamed to {}".format(profileName, userInput))	
					elif userInput == "delete":
						userInput = input("Are you sure you want to delete?").lower()
						if userInput == "yes":
							headsetAPIWrapper.deleteProfile(profileName)
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
				headsetAPIWrapper.createProfile(newProfileName)
				print("Profile {} created".format(newProfileName))

			#oledDriver.printToOled(modeType.Profile_Select.name)
		elif currentMode == modeType.Training_Mode:
			print(modeType.Training_Mode.name)

			userInput = input("Type clear to clear an all training, trainact to train an action or exit to leave and go live mode").lower()
			if keyboardPluggedIn() and userInput == 'clear':
				print("Deleting training data")
				headsetAPIWrapper.clearAll()
			if keyboardPluggedIn() and userInput == 'trainact':
				print("Training Profile")
				headsetAPIWrapper.trainProfile(profileName)
			if keyboardPluggedIn() and userInput == 'exit':
				print("Going to live mode")
				currentMode = modeType.Live_Mode
			#trainProfile = headsetAPIWrapper.trainProfile()

			#oledDriver.printToOled(modeType.Training_Mode.name)
			
		elif currentMode == modeType.Live_Mode:
			print("===================== Live Inferencing =====================")
			break

			# # Start Live Mode
			# status, message = headsetAPIWrapper.startInferencing()

			# print(message)
			# prevAction = ""
			# while True:
			# 	message = myClient.receiveMessage()
			# 	if not message:
			# 		continue
			# 	else:
			# 		action = message.decode()
			# 		if prevAction == action:
			# 			pass
			# 		elif action == "neutral":
			# 			pass
			# 		elif action == "lift":
			# 			control.grab_and_get()
			# 			time.sleep(1)
			# 		elif action == "drop":
			# 			control.put_back()
			# 			time.sleep(1)
			# 		elif action == "disappear":
			# 			control.take_picture()
			# 			time.sleep(1)
			# 		else:
			# 			print("Invalid Inference")
			# 		prevAction = action
			# except KeyboardInterrupt:
			# 	print("Caught Keyboard interrupt")

			# finally:
			# 	print("Exiting!")
			# 	# Stop Live Mode
			# 	status, message = headsetAPIWrapper.stopInferencing()

			# 	print(message)

			# 	headsetAPIWrapper.serverSmartSocket.closeSocket()
		

		# print(modeType.Live_Mode.name)
		# oledDriver.printToOled(modeType.Live_Mode.name)
		#if previousMode != currentMode:
			#print(currentMode.name)
		#previousMode = currentMode


if __name__ == '__main__':
	main()
