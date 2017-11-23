from smbus import SMBus
from collections import deque
import time


# =====GLOBAL DEFINITIONS=====


# LED Power Modes
_led_on_full = 0x01
_led_on_half = 0x03
_led_on_quart = 0x07
_led_off = 0x00

# LED Brightnesses
_max = 255
_off = 0

# Addresses
_update_adr = 0x25
_driver_adr = 0x3F
_shutdown_adr = 0x00
_reset_adr = 0x4F

# LED Registers
_leds = {"1r": 0x03, "1g": 0x04, "1b": 0x05, "2r": 0x06, "2g": 0x07, "2b": 0x08,
         "3r": 0x09, "3g": 0x0A, "3b": 0x0B, "4r": 0x0C, "4g": 0x0D, "4b": 0x0E,
         "5r": 0x0F, "5g": 0x10, "5b": 0x11, "6r": 0x12, "6g": 0x13, "6b": 0x14,
         "7r": 0x15, "7g": 0x16, "7b": 0x17, "8r": 0x18, "8g": 0x19, "8b": 0x1A}

# Brightness Spectrum
b_spectrum = []
for x in range(0, 256, 4):  # To change rate of brightness change, edit third parameter
    b_spectrum.append(x)

# Color Spectrum variables
c_spectrum = []
c_spectrum_temp = deque()
color = [255, 0, 0]

# Bus Creation
bus = SMBus(1)  # Creates new bus on channel 1


# =====COLOR SPECTRUM FUNCTIONS=====


def increase(rate, color_idx):
    """
    Increases the specified color by the given rate
    :param rate: the rate of change
    :param color_idx: the index identifier of the color; 0 (r), 1 (g), or 2 (b)
    """
    while color[color_idx] != 255:
        if color[color_idx] + rate < 255:
            color[color_idx] += rate
        else:
            color[color_idx] = 255
        c_spectrum.append(list(color[:]))


def decrease(rate, color_idx):
    """
    Decreases the specified color by the given rate
    :param rate: the rate of change
    :param color_idx: the index identifier of the color; 0 (r), 1 (g), or 2 (b)
    """
    while color[color_idx] != 0:
        if color[color_idx] - rate > 0:
            color[color_idx] -= rate
        else:
            color[color_idx] = 0
        c_spectrum.append(list(color[:]))


def make_spectrum(rate=8):
    """
    Creates the color spectrum used by spectrum_scroll()
    RECOMMENDED: Call this first in a setup function before scrolling
    :param rate: the rate of spectra divisions
    """
    _rate = int(255 / rate)

    increase(_rate, 1)  # Changes color to YELLOW
    decrease(_rate, 0)  # Changes color to GREEN
    increase(_rate, 2)  # Changes color to CYAN
    decrease(_rate, 1)  # Changes color to BLUE
    increase(_rate, 0)  # Changes color to MAGENTA
    decrease(_rate, 2)  # Changes color to RED


def spectrum_scroll(_num_led=8):
    """
    Scrolls through entire color spectrum. Is defined by color shifting up by 1 LED
    :param _num_led: the number of LEDs through which the transition will flow. Default/max is 8, min is 1
    """
    temp = []
    for l in range(0, 8/_num_led):
        temp += list(c_spectrum_temp)[l]

    write(temp*_num_led, _leds["1r"])
    c_spectrum_temp.rotate()
    time.sleep(0.03125)  # Sets period length (length of rainbow colors * delay)


@DeprecationWarning
def long_spectrum_scroll():
    """
    Scrolls through entire color spectrum. Is defined by color shifting through ENTIRE bar
    """
    write(c_spectrum_temp[1]*8, _leds["1r"])
    c_spectrum_temp.rotate()
    time.sleep(0.03125)


# =====BRIGHTNESS FUNCTIONS=====


def breathe(_led=_leds["1r"], _num_led=1):
    """
    Function that breathes a set of LEDs based on their BRIGHTNESS
    :param _led: the starting LED
    :param _num_led: the number of LEDs after the start one that are to be changed as well
    """
    delay = 0.1

    for brightness in b_spectrum:  # Increase in brightness from off to max
        write([brightness]*_num_led, _led)
        time.sleep(delay)
    for brightness in reversed(b_spectrum):  # Decrease in brightness from max to off
        write([brightness]*_num_led, _led)
        time.sleep(delay)


# =====UTILITY FUNCTIONS=====


def write(_data, _start_led=_leds["1r"], _reg=-1):
    """
    Writes new data to LED driver and automatically updates it
    :param _data: the data to send to the LED driver
    :param _start_led: the first LED to interact with
    :param _reg: the register to send data to on the LED driver
    """
    if _reg == 0x28:
        bus.write_i2c_block_data(_driver_adr, _reg, _data)
    elif _reg != -1:
        bus.write_byte_data(_driver_adr, _reg, _data)
    else:
        bus.write_i2c_block_data(_driver_adr, _start_led, _data)

    bus.write_byte_data(_driver_adr, _update_adr, 0x00)  # Sends update command to driver


# =====IMPLEMENTATION FUNCTIONS=====


def setup():
    """
    Sets up LED driver with proper power settings and initializes any global variable necessary for operation
    """
    global c_spectrum_temp

    # Turn on LEDs
    write(0x01, _reg=_shutdown_adr)

    # Activate LEDs at set current
    led_block = []
    for i in range(0, 25):
        led_block.append(_led_on_quart)  # To change current through LEDs edit the appended code
    write(led_block, _reg=0x28)  # NOTE: 0x28 is the setup code for LED 1R

    # Create color spectrum
    make_spectrum()
    c_spectrum_temp = deque(c_spectrum)


def test():
    """
    Basic testing to ensure functionality of any operation
    NOTE: To test operation, place command in the while loop
    """
    try:
        setup()
        while True:
            spectrum_scroll(1)
            # long_spectrum_scroll()
    except KeyboardInterrupt:
        print "Exiting..."
    finally:
        print "Cleaning..."
        clean()


def clean():
    """
    Cleans up LED driver to ensure smooth transition between operations
    """
    bus.write_byte_data(_driver_adr, _shutdown_adr, 0x00)  # Shuts down LEDs
    bus.write_byte_data(_driver_adr, _reset_adr, 0x4F)  # Resets LED registers
