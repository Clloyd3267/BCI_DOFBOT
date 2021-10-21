import enum

class modeType (enum.Enum):     #creating enumerations with class
    Initialization = 1
    Profile_Select = 2
    Training_Mode = 3
    Live_Mode = 4
    AI_Assist_Mode = 5
    Game_Mode = 6
#Tests
print("The enum name is: ", end="")
print(modeType.Initialization.name)      #print out name of enum

print("The enum name is: ", end="")
print(modeType.Profile_Select.name)
print("hello chrsi")
#end tests

for currentMode in (modeType):
    if currentMode == modeType.Initialization:
        print(modeType.Initialization.name)
    elif currentMode == modeType.Profile_Select:
        print(modeType.Profile_Select.name)
    elif currentMode == modeType.Training_Mode:
        print(modeType.Training_Mode.name)
    elif currentMode == modeType.Live_Mode:
        print(modeType.Live_Mode.name)
    elif currentMode == modeType.AI_Assist_Mode:
        print(modeType.AI_Assist_Mode.name)
    else:
        print(modeType.Game_Mode.name)

