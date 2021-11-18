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
			deleteProfile = server.deleteProfile()
			deselectProfile = server.deselectProfile()
			selectProfile = server.selectProfile()
			renameProfile = server.renameProfile()
			


			print("--------Select or Create a Profile---------")
			userInput = input("Type Select or Create")

			if userInput == 'select':
				print("Current Profile List:")
				print("Index | Profile Name")
				for index, value in enumerate(profileList):
					print ("{} | {}".format(index, value))

					userInput2 = input("Input the index of the profile to select: ")

				if userInput2.isnumeric() and 0 <= int(userInput2) < len(profileList):
					profileName = profileList[int(userInput2)]
					if server.selectProfile(profileName):
						print("\nUser {} selected!\n".format(profileName))
					else:
						print("\nUser {} could not be selected. Please try again!\n".format(profileName))
				else:
					print("\nInvalid Input. Please try again!\n")

				print("What would you like to do with the profile? (Type Load, Delete, Rename, or Train")
				userInput3 = input()

				if userInput3 == 'Load':
					print("Going to Live mode")
					currentMode = modeType.Live_Mode
				elif userInput3 == 'Train':
					print("Going to Training Mode")
					currentMode = modeType.Training_Mode
				elif userInput3 == 'Rename':
					userInput4 = input(renameProfile)#PLEASE CHECK THIS
					
				elif userInput3 == 'Delete':
					server.deleteProfile()

			elif userInput == 'create':
				
				print('Name Profile')


			#oledDriver.printToOled(modeType.Profile_Select.name)
		elif currentMode == modeType.Training_Mode:
			print(modeType.Training_Mode.name)
			trainProfile = server.trainProfile()
			getSelectedProfile = server.getSelectedProfile()

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
