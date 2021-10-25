import time

from Arm_Lib import Arm_Device
Arm = Arm_Device()
angle_6 = Arm.Arm_serial_servo_read(6)

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
