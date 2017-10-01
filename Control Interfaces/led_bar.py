from smbus import SMBus
import time
import random

# LED Power Modes
led_on_full = 0x01
led_on_half = 0x02
led_on_quart = 0x07
led_off = 0x00

# LED Brightnesses
max = 255
two_thirds = 170
three_quart = 191
half = 127
third = 85
quarter = 64
off = 0

# Addresses
update_adr = 0x25
driver_adr = 0x3F
shutdown_adr = 0x00
reset_adr = 0x4F

# LED Registers
led_1_r = 0x03
led_1_g = 0x04
led_1_b = 0x05
led_2_r = 0x06
led_2_g = 0x07
led_2_b = 0x08
led_3_r = 0x09
led_3_g = 0x0A
led_3_b = 0x0B
led_4_r = 0x0C
led_4_g = 0x0D
led_4_b = 0x0E
led_5_r = 0x0F
led_5_g = 0x10
led_5_b = 0x11
led_6_r = 0x12
led_6_g = 0x13
led_6_b = 0x14
led_7_r = 0x15
led_7_g = 0x16
led_7_b = 0x17
led_8_r = 0x18
led_8_g = 0x19
led_8_b = 0x1A
led_1 = led_1_r
led_2 = led_2_r
led_3 = led_3_r
led_4 = led_4_r
led_5 = led_5_r
led_6 = led_6_r
led_7 = led_7_r
led_8 = led_8_r

# Brightness Spectrum
spectrum = []
for x in range(0, 256, 4):
    spectrum.append(x)
# print len(spectrum)  #Debug: prints the length of spectrum
# print spectrum  #Debug: prints the spectrum list

# Rainbow Spectrums
rainbow_temp = []
r = 255
g = 0
b = 0


def increase(color, rate, color_str):
    while color != 255:
        if color + rate < 255:
            color += rate
        else:
            color = 255
        update_rainbow(color, color_str)


def decrease(color, rate, color_str):
    while color != 0:
        if color - rate > 0:
            color -= rate
        else:
            color = 0
        update_rainbow(color, color_str)


def update_rainbow(color, color_str):
    global r
    global g
    global b

    if color_str == "r":
        r = color
    elif color_str == "g":
        g = color
    elif color_str == "b":
        b = color
    rainbow_temp.append([r, g, b])


# print rainbow_temp  #Debug

def make_rainbow(r):
    global rainbow
    rate = int(255 / r)

    increase(g, rate, "g")  # Changes color to YELLOW
    decrease(r, rate, "r")  # Changes color to GREEN
    increase(b, rate, "b")  # Changes color to CYAN
    decrease(g, rate, "g")  # Changes color to BLUE
    increase(r, rate, "r")  # Changes color to MAGENTA
    decrease(b, rate, "b")  # Changes color to RED

    rainbow = list(reversed(rainbow_temp))


# Bus Creation
bus = SMBus(1)  # Creates new bus on channel 1


def update_leds():
    bus.write_byte_data(driver_adr, update_adr, 0x00)  # Sends update command to driver


def write_block_data(start_led, data):
    bus.write_i2c_block_data(driver_adr, start_led, data)
    update_leds()


# print data  #Debug: prints the data to be sent

def breathe_led(led):
    for brightness in spectrum:  # Increase in brightness from off to max
        write_block_data(led, [brightness])
        time.sleep(0.1)
    # print(brightness)  #Debug: prints brightness values
    # print brightness, ":", spectrum[brightness]  #Debug: prints the index number of spectrum and the value
    for brightness in spectrum:  # Decrease in brightness from max to off
        write_block_data(led, [brightness])
        time.sleep(0.1)
    # print(brightness)  #Debug: prints brightness value
    # print brightness-1, ":", spectrum[brightness - 1]  #Debug: prints the index number of spectrum and the value


def led_rainbow(led, num_led=1):
    for color in rainbow:
        # print color  #Debug: prints the color
        # make_color(led, color, num_led)
        write_block_data(led, color * num_led)
        time.sleep(0.1)
    write_block_data(led, [off, off, off] * num_led)


def setup():
    bus.write_byte_data(driver_adr, shutdown_adr, 0x01)  # Turn on LEDs
    make_rainbow(8)
    led_block = []
    for cmd in range(0, 25):
        led_block.append(led_on_quart)
    bus.write_i2c_block_data(driver_adr, 0x28, led_block)  # Activate LEDS
    # print led_on_full_block  #Debug
    update_leds()


def loop():
    while True:
        # breathe_led(led_1_r)
        # breathe_led_set(led_1_r)
        # make_color(led_1_r, "r")
        # make_color(led_3, "b")
        led_rainbow(led_1, random.randint(1, 8))
        pass


try:
    setup()
    loop()

except KeyboardInterrupt:
    pass

finally:
    bus.write_byte_data(driver_adr, shutdown_adr, 0x00)
    bus.write_byte_data(driver_adr, reset_adr, 0x4F)
