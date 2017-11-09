import serial
import time

port = serial.Serial(port="/dev/tty0", baudrate=9600)  # TODO: Configure port for appropriate device

link_request = 0x01
link_acknowledge = 0x02


