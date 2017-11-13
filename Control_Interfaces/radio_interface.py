import serial

port = serial.Serial(port="/dev/ttyS0", baudrate=9600, timeout=1)

coefficients = {"Link Request": 0x01, "Link Acknowledge": 0x02, "Throttle": 0x03, "Roll": 0x04, "Pitch": 0x05,
                "Yaw": 0x06, "X_Velocity": 0x07, "Y_Velocity": 0x08, "Z_Velocity": 0x09, "X_Acceleration": 0x0A,
                "Y_Acceleration": 0x0B, "Z_Acceleration": 0x0C, "Drone_GPS_Latitude": 0x0D, "Drone_GPS_Longitude": 0x0E,
                "Controller_GPS_Latitude": 0x0F, "Controller_GPS_Longitude": 0x10, "Altitude": 0x11, "Fail": 0x12}

input_buffer = []
output_buffer = []


def receive():
    """
    Function that reads data from the serial buffer sent from the drone to input_buffer
    """
    global input_buffer

    input_buffer = port.readline()
    print "Received:", input_buffer  # Debug


def send(val):
    """
    Function that sends data in the output_buffer to the drone
    """
    port.write(val)
    print "Sent:", val
