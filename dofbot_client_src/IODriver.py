import RPi.GPIO as GPIO
import signal
import sys

GPIO.setmode(GPIO.BCM)

BTN_A_PIN=4
BTN_B_PIN=17
BTN_C_PIN=27
BTN_D_PIN=22
BTN_E_PIN=5
BTN_F_PIN=6 

GPIO.setup(BTN_A_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BTN_B_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BTN_C_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BTN_D_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BTN_E_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BTN_F_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def signal_handler(sig, frame): #close GPIOs on sigint
	GPIO.cleanup()
	sys.exit(0)

def Poll_A(): #holds thread until button A is pushed
	GPIO.wait_for_edge(BTN_A_PIN, GPIO.RISING)
	return True

def Poll_B(): #holds thread until button B is pushed
        GPIO.wait_for_edge(BTN_B_PIN, GPIO.RISING)
        return True

def Poll_C(): #holds thread until button C is pushed
        GPIO.wait_for_edge(BTN_C_PIN, GPIO.RISING)
        return True

def Poll_D(): #holds thread until button D is pushed
        GPIO.wait_for_edge(BTN_D_PIN, GPIO.RISING)
        return True

def Poll_E(): #holds thread until button E is pushed
        GPIO.wait_for_edge(BTN_E_PIN, GPIO.RISING)
        return True

def Poll_F(): #holds thread until button F is pushed
        GPIO.wait_for_edge(BTN_F_PIN, GPIO.RISING)
        return True

def interruption(pin):
	return True

def interrupt_A(): #will return true once A is pushed
	GPIO.add_event_detect(BTN_A_PIN, GPIO.FALLING, callback = interruption, bouncetime=100)

def interrupt_B(): #will return true once B is pushed
        GPIO.add_event_detect(BTN_B_PIN, GPIO.FALLING, callback = interruption, bouncetime=100)

def interrupt_C(): #will return true once C is pushed
        GPIO.add_event_detect(BTN_C_PIN, GPIO.FALLING, callback = interruption, bouncetime=100)

def interrupt_D(): #will return true once D is pushed
        GPIO.add_event_detect(BTN_D_PIN, GPIO.FALLING, callback = interruption, bouncetime=100)

def interrupt_E(): #will return true once E is pushed
        GPIO.add_event_detect(BTN_E_PIN, GPIO.FALLING, callback = interruption, bouncetime=100)

def interrupt_F(): #will return true once F is pushed
        GPIO.add_event_detect(BTN_F_PIN, GPIO.FALLING, callback = interruption, bouncetime=100)


signal.signal(signal.SIGINT, signal_handler) #close GPIOs on sigint
