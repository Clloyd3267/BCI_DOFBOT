import threading
import time
import random
import inspect
import ctypes

angle_1 = angle_2 = angle_3 = angle_4 = angle_5 = angle_6 = 90

from Arm_Lib import Arm_Device
Arm = Arm_Device()

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)

def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

def get_command():
    global angle_1, angle_2, angle_3, angle_4, angle_5, angle_6
    command = str(input("Give a command: "))
    if(command == "move_servo"):
        servo = int(input("which one: "))
        angle = int(input("what degree angle (0-180): "))
        if(servo == 1):
            angle_1= angle
        elif(servo == 2):
            angle_2= angle
        elif(servo == 3):
            angle_3= angle
        elif(servo == 4):
            angle_4= angle
        elif(servo == 5):
            angle_5= angle
        elif(servo == 6):
            angle_6= angle
        Arm.Arm_serial_servo_write(servo, angle, 500)
    elif(command == "rgb"):
        red = int(input("choose a red value: "))
        green = int(input("choose a green value: "))
        blue = int(input("choose a blue value: "))
        Arm.Arm_RGB_set(red, green, blue)
    elif(command == "open_hand"):
        angle_6= 0
        Arm.Arm_serial_servo_write(6, 0, 500)
    elif(command == "close_hand_forcefully"):
        angle_6 = 180
        Arm.Arm_serial_servo_write(6, 180, 500)
    elif(command == "default_position"):
        angle_1 = angle_2 = angle_3 = angle_4 = angle_5 = angle_6 = 90
        Arm.Arm_serial_servo_write6(90, 90, 90, 90, 90, 90, 1000)
    elif(command == "buzzer_start"):
        Arm.Arm_Buzzer_On()
    elif(command == "buzzer_stop"):
        Arm.Arm_Buzzer_Off()
    elif(command == "reach_forward_a_little"):
        angle_2=90
        angle_3= 55
        angle_4= 70
        Arm.Arm_serial_servo_write6(angle_1,angle_2, angle_3, angle_4, angle_5, angle_6, 1000)
    elif(command == "reach_forward_a_little_more"):
        angle_2= 90
        angle_3= 15
        angle_4= 30
        Arm.Arm_serial_servo_write6(angle_1,angle_2, angle_3, angle_4, angle_5, angle_6, 1000)
    elif(command == "reach_forward"):
        angle_2= 90
        angle_3= 25
        angle_4= 65
        Arm.Arm_serial_servo_write6(angle_1, angle_2, 25, 65, angle_5, angle_6, 1000)
    elif(command == "reach_down"):
        angle_2= 45
        angle_3= 25
        angle_4= 65
        Arm.Arm_serial_servo_write6(angle_1, 45, 25, 65, angle_5, angle_6, 1000)
    elif(command == "turn_right"):
        angle_1= int(input("what angle to turn to (0->90): "))
        Arm.Arm_serial_servo_write(1, angle_1, 500)
    elif(command == "turn_left"):
        angle= int(input("what angle to turn to (0->90): "))
        angle_1= 180-angle
        Arm.Arm_serial_servo_write(1, 180-angle, 500)
    elif(command == "pull_up"):
        angle_2= 90
        angle_3= 90
        angle_4= 90
        Arm.Arm_serial_servo_write6(angle_1, 90, 90, 90, angle_5, angle_6, 1000)
    elif(command == "chris_mode"):
        while(1):
            Arm.Arm_Buzzer_Off()
            red= random.randint(0, 256)
#            if(red>=127):
#                Arm.Arm_Buzzer_On()
#            else:
#                Arm.Arm_Buzzer_Off()
            blue= random.randint(0, 256)
            green= random.randint(0, 256)
            Arm.Arm_RGB_set(red, green, blue)
            angle_1= random.randint(0, 180)
            angle_2= random.randint(35, 100)
            angle_3= random.randint(35, 100)
            angle_4= random.randint(35, 100)
            angle_5= random.randint(0, 180)
            angle_6= random.randint(0, 180)
            Arm.Arm_serial_servo_write6(angle_1, angle_2, angle_3, angle_4, angle_5, angle_6, 500)
            time.sleep(0.5)
    elif(command=="close_hand"):
        angle_6 = Arm.Arm_serial_servo_read(6)
        while(check_hand()):
            if(angle_6<175):
                angle_6 += 15
            else:
                break
            Arm.Arm_serial_servo_write(6, angle_6, 100)
            time.sleep(0.25)
    elif(command == "stop"):
        Arm.Arm_Clear_Action()
    else:
        print("command not recognized")

def check_hand():
#    print(angle_6)
#    print(Arm.Arm_serial_servo_read(6))
    return(abs(angle_6-Arm.Arm_serial_servo_read(6))<=3)

def Arm_Handle():
    s_time = 500
    s_step = 1
    Arm.Arm_serial_servo_write6(90, 90, 90, 90, 90, 90, 1000)
    while 1:
        get_command()
        time.sleep(1)

thread2 = threading.Thread(target=Arm_Handle)
thread2.setDaemon(True)
thread2.start()
time.sleep(1000000)
