import enum
import keyboard

class modeType (enum.Enum):     #creating enumerations with class
    Initializing = 1
    Profile_Select = 2
    Training_Mode = 3
    Live_Mode = 4
    #AI_Assist_Mode = 5
    #Game_Mode = 6


class BciCtr ():
    currentMode = modeType.Initializing                                 #set default mode to Initialization
    def main(self):
        while(True):
            if self.currentMode == modeType.Initializing:
                print(modeType.Initialization.name)  #print name of enumeration
                self.currentMode = modeType.Profile_Select
            elif self.currentMode == modeType.Profile_Select:
                print(modeType.Profile_Select.name)
                if keyboard.is_pressed('t'):            # trained
                    self.currentMode = modeType.Live_Mode
                if keyboard.is_pressed('u'):            #untrained
                    self.currentMode = modeType.Training_Mode
            elif self.currentMode == modeType.Training_Mode:
                print(modeType.Training_Mode.name)
                self.currentMode = modeType.Live_Mode
            elif self.currentMode == modeType.Live_Mode:
                print(modeType.Live_Mode.name)


