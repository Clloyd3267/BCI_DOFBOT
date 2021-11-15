import control
from ClientInterfaceDriver import *
import time
from SmartSockets.SmartSocket import *

class ModeType(enum.Enum):
    INITIALIZATION = 1
    PROFILE_SELECT = 2
    TRAINING_MODE = 3
    LIVE_MODE = 4

def keyboardPluggedIn():
	return True

if __name__ == "__main__":
	# Connection information
	server_ip = "128.153.178.74" # CDL=> My IP (headset system)
	server_port = 42070

	# Create a client socket
	server = ClientInterfaceDriver(server_ip, server_port)

	myClient = SmartSocket(server_ip, 42071, SocketType.CLIENT)


	# currentMode = ModeType.INITIALIZATION
	# previousMode = ModeType.INITIALIZATION

	try:
		done = False
		while not done:
			profileList = server.listProfiles()

			print("===================== Select a Profile =====================")
			print("Current Profile List:")
			print("---------------------")
			print("Index | Profile Name")
			for index, value in enumerate(profileList):
				print ("{} | {}".format(index, value))

			userInput = input("Input the index of the profile to select: ")

			if userInput.isnumeric() and 0 <= int(userInput) < len(profileList):
				profileName = profileList[int(userInput)]
				if server.selectProfile(profileName):
					print("\nUser {} selected!\n".format(profileName))
				else:
					print("\nUser {} could not be selected. Please try again!\n".format(profileName))
			else:
				print("\nInvalid Input. Please try again!\n")

			print("")
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
				# # Get inference
				# # status, message, action, pow, t = server.receiveInference()

				# if not status:
				# 	print(message)
				# elif action == "neutral":
				# 	pass
				# elif action == "lift":
				# 	control.grab_and_get()
				# 	time.sleep(1)
				# elif action == "drop":
				# 	control.put_back()
				# 	time.sleep(1)
				# elif action == "disappear":
				# 	control.take_picture()
				# 	time.sleep(1)
				# else:
				# 	print("Invalid Inference")

	# 		if previousMode != currentMode:
	# 			print("Entering {} mode".format(currentMode.name))

	# 		previousMode = currentMode

	# 		if currentMode == ModeType.INITIALIZATION:
	# 			# Reset the arm to a default position
	# 			# Print the current mode when entering to the display
	# 			currentMode = ModeType.PROFILE_SELECT

	# 		elif currentMode == ModeType.PROFILE_SELECT:

	# 			profileList = server.listProfiles()

	# 			# Output profile list with create new profile option
	# 			print("")
	# 			print("===================== Select a Profile =====================")
	# 			print("Current Profile List:")
	# 			print("---------------------")
	# 			print("Index | Profile Name")
	# 			for index, value in enumerate(profileList):
	# 				print ("{} | {}".format(index, value))

	# 			# Get user input for selection
	# 			userInput = input("Input the index of the profile to select or enter -1 to create and select a new profile: ")

	# 			if userInput == "-1":  # Create new profile
	# 				if keyboardPluggedIn:
	# 					userInput = input("Input new profile name: ")
	# 					if server.createProfile(userInput):
	# 						server.selectProfile(userInput)
	# 						currentMode = ModeType.TRAINING_MODE

	# 						print("User created and selected!")
	# 						continue
	# 					else:
	# 						print("Invalid Input. Please try again!")
	# 				else:
	# 					i = 0
	# 					while "New Profile {}".format(i) not in profileList:
	# 						i += 1

	# 					profileName = "New Profile {}".format(i)

	# 					if server.createProfile(profileName):
	# 						server.selectProfile(profileName)
	# 						currentMode = ModeType.TRAINING_MODE

	# 						print("User created and selected!")
	# 						continue
	# 					else:
	# 						print("Invalid Input. Please try again!")

	# 			elif userInput.isnumeric() and 0 <= int(userInput) < len(profileList):  # Select Profile

	# 				chosenProfileName = profileList[int(userInput)]

	# 				# Get user input for selection
	# 				userInput = input("Input what action you would like to do: 'select', 'train,' 'rename', or 'delete': ")

	# 				# Prompt the user if they would like to select, train, rename, or delete the profile
	# 				if userInput == "train":
	# 					server.selectProfile(chosenProfileName)
	# 					currentMode = ModeType.TRAINING_MODE

	# 					print("User selected for training!")
	# 					continue
	# 				elif userInput == "select":
	# 					server.selectProfile(chosenProfileName)
	# 					currentMode = ModeType.LIVE_MODE

	# 					print("User selected for live mode!")
	# 					continue
	# 				elif userInput == "rename":
	# 					if keyboardPluggedIn:
	# 						userInput = input("Input new profile name: ")
	# 						if server.renameProfile(chosenProfileName, userInput):

	# 							print("User renamed!")
	# 							continue
	# 						else:
	# 							print("Invalid Input. Please try again!")
	# 					else:
	# 						print("Cannot rename profile when no keyboard is plugged in!")
	# 						continue
	# 				elif userInput == "delete":
	# 					if server.deleteProfile(chosenProfileName):
	# 						print("User deleted!")
	# 						continue
	# 					else:
	# 						print("Invalid Input. Please try again!")
	# 				else:
	# 					print("Invalid Input. Please try again!")
	# 			else:
	# 				print("CDL=>1")


	# 		# 	# List profiles for a user to pick one


	# 		# while True:


	# 		# 	print("")
	# 		# 	print("===================== Select a Profile =====================")
	# 		# 	print("Current Profile List:")
	# 		# 	print("---------------------")
	# 		# 	print("Index | Profile Name")
	# 		# 	for index, value in enumerate(profileList):
	# 		# 		print ("{} | {}".format(index, value))

	# 		# 	userInput = input("Input the index of the profile to select or enter -1 to create and select a new profile: ")

	# 		# 	if userInput == "-1":                         # Create new profile
	# 		# 		print("")
	# 		# 		userInput = input("Input new profile name: ")
	# 		# 		if server.createProfile(userInput):
	# 		# 			server.selectProfile(userInput)
	# 		# 			print("User created and selected!")
	# 		# 			break
	# 		# 		else:
	# 		# 			print("Invalid Input. Please try again!")

	# 		# 	elif 0 <= int(userInput) < len(profileList):  # Select Profile
	# 		# 		if server.selectProfile(profileList[int(userInput)]):
	# 		# 			print("User selected!")
	# 		# 			break
	# 		# 		else:
	# 		# 			print("Invalid Input. Please try again!")
	# 		# 	else:                                         # Invalid Input
	# 		# 		print("Invalid Input. Please try again!")

	# 		elif currentMode == ModeType.TRAINING_MODE:
	# 			print("Selected User: ", server.getSelectedProfile())
	# 			pass
	# 		elif currentMode == ModeType.LIVE_MODE:
	# 			pass

	except KeyboardInterrupt:
		print("Caught Keyboard interrupt")

	finally:
		print("Exiting!")
		# Stop Live Mode
		status, message = server.stopInferencing()

		print(message)

		server.serverSmartSocket.closeSocket()