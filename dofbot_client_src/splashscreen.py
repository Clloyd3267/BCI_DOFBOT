# ------------------------------------------------------------------------------
# Name         : splashscreen.py
# Date Created : 12/07/2021
# Author(s)    : Chris Lloyd, Josiah Schmidt, Camilla Ketola, Dylan Shuhart
# Description  : Startup script to move the arm to a default position and
#                initialize the oled to a splashscreen.
# ------------------------------------------------------------------------------

# Imports
from UserIOInteraction import *
import control
import time

def splashscreen():
	userIO = UserIOInteraction(consoleMode=False)
	message = "Welcome to the".center(OLEDDriver.MAX_LINE_WIDTH) + "BCI Arm System".center(OLEDDriver.MAX_LINE_WIDTH)
	userIO.oled.printToLine(0, "MI6: Big Brain Team".center(OLEDDriver.MAX_LINE_WIDTH))
	userIO.printMessage(message, waitKey=False)

	# Move arm to default postion and open/close claw
	control.default()
	time.sleep(0.5)
	control.close_hand()
	time.sleep(0.5)
	control.open_hand()

if __name__ == "__main__":
	splashscreen()