import enum
import keyboard

from oledDriver import *


class modeType(enum.Enum):  # creating enumerations with class
    Initializing = 1
    Profile_Select = 2
    Training_Mode = 3
    Live_Mode = 4
    # AI_Assist_Mode = 5
    # Game_Mode = 6


# oledDriver = Draw()

# Draw.printToOled()


# oledDriver = Draw()


def main():
    previousMode = None
    currentMode = modeType.Initializing  # set default mode to Initialization
    oledDriver = Draw()
    while True:

        if currentMode == modeType.Initializing:
            #print(modeType.Initializing.name)      # print name of enumeration
            oledDriver.printToOled(modeType.Initializing.name)
            currentMode = modeType.Profile_Select
        elif currentMode == modeType.Profile_Select:
            #print(modeType.Profile_Select.name)
            oledDriver.printToOled(modeType.Profile_Select.name)
            print('Enter mode: ')
            t = input()
            #if t = liveMode:            # trained
                #currentMode = modeType.Live_Mode
            #if input('u'):            # untrained
                #currentMode = modeType.Training_Mode
        elif currentMode == modeType.Training_Mode:
            #print(modeType.Training_Mode.name)
            oledDriver.printToOled(modeType.Training_Mode.name)
            currentMode = modeType.Live_Mode
        # elif currentMode == modeType.Live_Mode:
        # print(modeType.Live_Mode.name)
        # oledDriver.printToOled(modeType.Live_Mode.name)
        if previousMode != currentMode:
            print(currentMode.name)
        previousMode = currentMode


if __name__ == '__main__':
    main()