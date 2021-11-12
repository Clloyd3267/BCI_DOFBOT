from control import *
from ClientInterfaceDriver import *

if __name__ == "__main__":
	# Connection information
	server_ip = "128.153.190.62" # CDL=> My IP (headset system)
	server_port = 42070

	# Create a client socket
	server = ClientInterfaceDriver(server_ip, server_port)

	done = False

	while not done:
		# List profiles for a user to pick one
		profileList = server.listProfiles()

		while True:
			print("")
			print("===================== Select a Profile =====================")
			print("Current Profile List:")
			print("---------------------")
			print("Index | Profile Name")
			for index, value in enumerate(profileList):
				print ("{} | {}".format(index, value))

			userInput = input("Input the index of the profile to select or enter -1 to create and select a new profile: ")

			if userInput == "-1":                         # Create new profile
				print("")
				userInput = input("Input new profile name: ")
				if server.createProfile(userInput):
					server.selectProfile(userInput)
					print("User created and selected!")
					break
				else:
					print("Invalid Input. Please try again!")

			elif 0 <= int(userInput) < len(profileList):  # Select Profile
				if server.selectProfile(profileList[int(userInput)]):
					print("User selected!")
					break
				else:
					print("Invalid Input. Please try again!")
			else:                                         # Invalid Input
				print("Invalid Input. Please try again!")

		print("Selected User: ", server.getSelectedProfile())

	server.serverSmartSocket.closeSocket()