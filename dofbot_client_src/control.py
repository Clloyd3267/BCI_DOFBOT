import time
import cv2
import os
from PIL import Image

from Arm_Lib import Arm_Device
Arm = Arm_Device()
angle_6 = Arm.Arm_serial_servo_read(6)
angle_1 = Arm.Arm_serial_servo_read(1)
angle_2 = Arm.Arm_serial_servo_read(2)
angle_3 = Arm.Arm_serial_servo_read(3)
angle_4 = Arm.Arm_serial_servo_read(4)
angle_5 = Arm.Arm_serial_servo_read(5)

def get_current_forward_position():
    global angle_3, angle_2
    if(abs(angle_3-90)<=5):
        return 0
    elif(abs(angle_3-55)<=5):
        return 1
    elif(abs(angle_3-25)<=5):
        if(abs(angle_2-90)<=5):
            return 2
        else:
            return 4
    else:
        return 3

def check_hand():
    global angle_6
    # print(angle_6)
    # print(Arm.Arm_serial_servo_read(6))
    return(abs(angle_6-Arm.Arm_serial_servo_read(6))<=5)

def close_hand():
    global angle_6
    angle_6  = Arm.Arm_serial_servo_read(6)
    while(check_hand()):
        if(angle_6<175):
            angle_6 += 15
        else:
            break
        Arm.Arm_serial_servo_write(6, angle_6, 50)
        time.sleep(0.25)
    return 0

def open_hand():
    global angle_6
    angle_6= 0
    Arm.Arm_serial_servo_write(6, 0, 500)
    return 0

def arm_turn_left():
    global angle_1
    increment = 10
    angle_1+= increment
    Arm.Arm_serial_servo_write(1, angle_1, 500)
    return 0

def arm_turn_right():
    global angle_1
    increment = 10
    angle_1-= increment
    Arm.Arm_serial_servo_write(1, angle_1, 500)
    return 0

def arm_next_forward_position():
    global angle_1, angle_2, angle_3, angle_4, angle_5, angle_6
    position = get_current_forward_position()
    if(position == 0):
        angle_2 = 90
        angle_3 = 55
        angle_4 = 70
        Arm.Arm_serial_servo_write6(angle_1, angle_2, angle_3, angle_4, angle_5, angle_6, 500)
    elif(position == 1):
        angle_2 = 90
        angle_3 = 25
        angle_4 = 65
        Arm.Arm_serial_servo_write6(angle_1, angle_2, angle_3, angle_4, angle_5, angle_6, 500)
    elif(position == 2):
        angle_2 = 90
        angle_3 = 15
        angle_4 = 30
        Arm.Arm_serial_servo_write6(angle_1, angle_2, angle_3, angle_4, angle_5, angle_6, 500)
    elif(position == 3):
        angle_2 = 45
        angle_3 = 25
        angle_4 = 65
        Arm.Arm_serial_servo_write6(angle_1, angle_2, angle_3, angle_4, angle_5, angle_6, 500)

    return 0

def arm_next_back_position():
    global angle_1, angle_2, angle_3, angle_4, angle_5, angle_6
    position = get_current_forward_position()
    if(position == 1):
        angle_2 = 90
        angle_3 = 90
        angle_4 = 90
        Arm.Arm_serial_servo_write6(angle_1, angle_2, angle_3, angle_4, angle_5, angle_6, 500)
    elif(position == 2):
        angle_2 = 90
        angle_3 = 55
        angle_4 = 70
        Arm.Arm_serial_servo_write6(angle_1, angle_2, angle_3, angle_4, angle_5, angle_6, 500)
    elif(position == 3):
        angle_2 = 90
        angle_3 = 25
        angle_4 = 65
        Arm.Arm_serial_servo_write6(angle_1, angle_2, angle_3, angle_4, angle_5, angle_6, 500)
    elif(position == 4):
        angle_2 = 90
        angle_3 = 15
        angle_4 = 30
        Arm.Arm_serial_servo_write6(angle_1, angle_2, angle_3, angle_4, angle_5, angle_6, 500)

    return 0

def take_picture():
    feed = cv2.VideoCapture(0)
    ret, frame = feed.read()
    picture = Image.fromarray(frame)
    save_picture(picture)
    feed.release()
    return 0

def save_picture(image):
    if(os.listdir("/media/dofbot")):
        filepath = "/media/dofbot/" + os.listdir("/media/dofbot")[0]
    else:
        filepath = "/home/dofbot/Pictures"
    filepath = filepath + "/" + time.strftime("%d-%b-%Y-%H-%M-%S") +".jpg"
    image.save(filepath)

def default():
    Arm.Arm_serial_servo_write6(90, 90, 90, 0, 90, 90, 500)
    # while(get_current_forward_position()!=0):
    #         arm_turn_left()
    #         arm_next_back_position()
    #         time.sleep(0.5)

def grab_and_get():
    while(get_current_forward_position()!=4):
        arm_turn_right()
        arm_next_forward_position()
        time.sleep(0.5)
    close_hand()
    time.sleep(0.5)
    while(get_current_forward_position()!=0):
        arm_turn_left()
        arm_next_back_position()
        time.sleep(0.5)
def put_back():
    while(get_current_forward_position()!=4):
        arm_turn_right()
        arm_next_forward_position()
        time.sleep(0.5)
    open_hand()
    time.sleep(0.5)
    while(get_current_forward_position()!=0):
        arm_turn_left()
        arm_next_back_position()
        time.sleep(0.5)
