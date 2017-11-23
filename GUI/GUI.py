import json
import os

from kivy.core.window import Window
from kivy.lang import Builder

from util import Colors

colors = Colors()

os.chdir("..")
settings_loc = os.path.abspath("Settings.json")
# print settings_loc  # Debug
os.chdir("GUI - Deprecated")
# print os.path.abspath("")  # Debug

with open(settings_loc) as settings_file:
    settings = json.load(settings_file)

Window.size = (480, 320)
Window.clearcolor = colors.white
Builder.load_file("Gui.kv")

cur_screen = 0

coord_enabled = False
flight_stats = {"vx": 0, "vy": 0, "vz": 0, "ax": 0, "ay": 0, "az": 0, "pitch": 0, "roll": 0, "yaw": 0, "alt": 0,
                "dist": 0, "vu": settings["general"]["units"]["velocity"],
                "au": settings["general"]["units"]["acceleration"], "mu": settings["general"]["units"]["measurement"],
                "du": u'\N{Degree Sign}'}

