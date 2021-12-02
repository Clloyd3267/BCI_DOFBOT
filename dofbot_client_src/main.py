import enum
import time
#from ClientInterfaceDriver import *
from HeadsetAPIWrapperTest import *
from UserIOInteraction import *


class modeType(enum.Enum):  # creating enumerations with class
	Initializing = 1
	Profile_Select = 2
	Training_Mode = 3
	Live_Mode = 4

def keyboardPluggedIn():
	return True


def isPressed(button):
	if button:
		button = False
		return True
	else:
		return False

rstButton = False
ProfileSltButton = False
	

if __name__ == "__main__":
	previousMode = None
	currentMode = modeType.Initializing  # set default mode to Initialization
	headsetAPIWrapper = HeadsetAPIWrapper()
	while True:
		if currentMode == modeType.Initializing:
			print(modeType.Initializing.name)      # print name of enumeration
			currentMode = modeType.Profile_Select
		elif currentMode == modeType.Profile_Select:
			profileList = headsetAPIWrapper.listProfiles()
		
			print("--------Select or Create a Profile---------")
			userInput = input("Type select or create: ").lower()

			if userInput == "select":
				profileName = promptUserList("Current Profile List:", profileList)
				if profileName:	 
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

			elif userInput == "create":
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

		elif currentMode == modeType.Training_Mode:
			print(modeType.Training_Mode.name)

			userInput = input("Type clear to clear an all training, trainact to train an action or exit to leave and go live mode: ").lower()
			if keyboardPluggedIn() and userInput == "clear":
				print("Deleting training data")
				headsetAPIWrapper.clearAll()
			if keyboardPluggedIn() and userInput == "trainact":
				while True:
					actionList = list(headsetAPIWrapper.getSigTrainedAct().keys())
					action = promptUserList("Action List: ", actionList)
					trainDelete = promptUserList("Do you want to train or delete training for the action?", ["train", "delete"])
					if trainDelete == "delete":
						headsetAPIWrapper.trainProfile(action, "mentalCommand", "erase")
					elif trainDelete == "train":
						printMessage("Please think about or move with selected action")
						printMessage("Press button when ready")
						#insert button push

						headsetAPIWrapper.trainProfile(action, "mentalCommand", "start")
						#training running
						acceptReset = promptUserList("Training Complete! Do you want to accept or reject the training? ", ["accept", "reject"])
						if acceptReset == "accept":
							headsetAPIWrapper.trainProfile(action, "mentalCommand", "accept")
							doneNotDone = promptUserList("Are you done or do you want to train again? Type done or continue. ", ["done", "continue"])		# Check if done or train again
							if doneNotDone == "done": 					#if done, break, else contiue
								break
							
							elif acceptReset == "reject":
								headsetAPIWrapper.trainProfile(action, "mentalCommand", "reset")
								printMessage("Training rejected")
								break

			if keyboardPluggedIn() and userInput == "exit":
				print("Going to live mode")
				currentMode = modeType.Live_Mode
			#trainProfile = headsetAPIWrapper.trainProfile()
			
		elif currentMode == modeType.Live_Mode:
			printMessage("===================== Live Inferencing =====================")

			# Start Live Mode
			headsetAPIWrapper.startInferencing()

			while True:
				status, message, action, power, rtime = headsetAPIWrapper.receiveInference()
				if isPressed(rstButton):
					headsetAPIWrapper.stopInferencing()
					currentMode = modeType.Initializing
					break
				elif isPressed(ProfileSltButton):
					headsetAPIWrapper.stopInferencing()
					currentMode = modeType.Profile_Select
					break
				elif not status:
					printMessage(message)
					continue
				elif action == "neutral":
					continue
				elif action == "lift":
					# control.grab_and_get()
					print(action)
				elif action == "drop":
					#control.put_back()
					print(action)
				elif action == "disappear":
					#control.take_picture()
					print(action)
				else:
					print("Invalid Inference: {}".format(action))
				time.sleep(1)

				# Stop Live Mode
				status, message = headsetAPIWrapper.stopInferencing()
