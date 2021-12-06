# ------------------------------------------------------------------------------
# Name         : IODriver.py
# Date Created : 11/16/2021
# Author(s)    : Chris Lloyd, Josiah Schmidt, Camilla Ketola, Dylan Shuhart
# Description  : Control library for Raspberry Pi GPIO.
# ------------------------------------------------------------------------------

# Imports
import RPi.GPIO as GPIO

# GPIO Pin assignments for BCI Dofbot # CDL=> Check these values later
BTN_A_PIN = RST_BTN     = 11
BTN_B_PIN = PRF_SEL_BTN = 13
BTN_C_PIN = UP_BTN      = 15
BTN_D_PIN = DN_BTN      = 16
BTN_E_PIN = LF_BTN      = 18
BTN_F_PIN = RT_BTN      = 22

# Ignore warnings and user board pin numbering scheme
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

def initInterruptEdge(button, callBackFunction):
	"""
	Setup an edge triggered interrupt on a specific gpio pin.

	Arguments:
		button           (int)  : The input pin number to add an interrupt to.
		callBackFunction (Func) : The function to be invoked when an interrupt occurs.
	"""
	GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.add_event_detect(button, GPIO.RISING, bouncetime=200, callback=callBackFunction)

def initPollingEdge(button):
	"""
	Setup an edge triggered detector on a specific gpio pin.

	Arguments:
		button (int) : The input pin number to add a detector to.
	"""
	GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.add_event_detect(button, GPIO.RISING, bouncetime=200)

def isPressed(button):
	"""
	Check if a specific pin had an edge event.

	Arguments:
		button (int) : The input pin number to check for an edge event on.

	Returns:
		Boolean of whether an edge event occurred.
	"""
	return GPIO.event_detected(button)
