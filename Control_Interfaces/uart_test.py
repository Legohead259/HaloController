import time
import serial

port = serial.Serial(port="/dev/ttyS0", baudrate=9600)
ack = 0

while True:
    port.write(str(ack))
    print "Sent:", ack
    time.sleep(1)
    bit_rec = port.read()
    print "Received:", bit_rec
    ack += 1
    print "This is a test to show that GitHub V1 updating is working"
