import serial
import time

port = serial.Serial(port="/dev/tty0", baudrate=9600)  # TODO: Configure port for appropriate device

link_request = 0x01
link_acknowledge = 0x02

coefficients = {"throttle": 0x03, "roll": 0x04}
pitch_co = 0x05
yaw_co = 0x06
x_vel_co = 0x07
y_vel_co = 0x08
z_vel_co = 0x09
x_acc_co = 0x0A
y_acc_co =
