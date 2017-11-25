from led_bar import *
import Control_Interfaces.led_bar as led_bar
import time

led_bar.setup()

boot_start = time.time()
print boot_start  # Debug

while time.time() <= boot_start + 10:
    led_bar.spectrum_scroll()

link_start = time.time()
print link_start  # Debug

while time.time() <= link_start + 5:
    led_bar.alternate_flash(delay=0.125)

ack_start = time.time()
print ack_start  # Debug

while time.time() <= ack_start + 3:
    led_bar.flash(led_bar._green_leds)
