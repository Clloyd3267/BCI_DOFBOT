import enum

class modeType (enum.Enum):
    Initialization = 1
    Profile_Select = 2
    #Training_Mode = 3
    #Live_Mode = 4
    #AI_Assist_Mode = 5
    #game_Mode = 6
print("The enum name is: ", end="")
print(modeType.Initialization.name)

print("The enum name is: ", end="")
print(modeType.Profile_Select.name)
print("hello chrsi")

#psuedocode for functions (for reference not actual code)
#if startup:
    #print(modeType.Initialization.name)

#if profSel:
    #print(modeType.Profile_Select.name)

#if training
    #print(modeType.Training_Mode.name)
