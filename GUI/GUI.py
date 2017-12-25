from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
import os

from kivy.properties import StringProperty
from kivy.uix.actionbar import ActionPrevious
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen

from libs.garden import MapMarker
from libs.garden.mapview import MapView
from util import Colors, settings

colors = Colors()

Window.size = (480, 320)
Window.clearcolor = colors.white
Builder.load_file("Gui.kv")

cur_screen = 0

coord_enabled = False
flight_stats = {"vx": 0, "vy": 0, "vz": 0, "ax": 0, "ay": 0, "az": 0, "pitch": 0, "roll": 0, "yaw": 0, "alt": 0,
                "dist": 0, "vu": settings["general"]["units"]["velocity"],
                "au": settings["general"]["units"]["acceleration"], "mu": settings["general"]["units"]["measurement"],
                "du": u'\N{Degree Sign}'}


class HomeButton(ActionPrevious):
    title = 'Halo Controller'
    app_icon = os.path.abspath("icons/DroneIcon.png")
    with_previous = False


class Header(GridLayout):
    top_left = os.path.abspath("icons/CockpitTL.png")
    drone_gps = StringProperty(os.path.abspath("icons/GPSIcon.png"))
    drone_battery = StringProperty(os.path.abspath("icons/Battery.png"))
    drone_connection = StringProperty(os.path.abspath("icons/DroneNo.png"))

    top_right = os.path.abspath("icons/CockpitTR.png")
    controller_gps = StringProperty(os.path.abspath("icons/GPSIcon.png"))
    wifi_connection = StringProperty(os.path.abspath("icons/ConnectionIconNone.png"))
    controller_battery = StringProperty(os.path.abspath("icons/Battery.png"))

    def update_gps(self):
        self.gps = os.path.abspath("icons/MissingTexture.png")


class MapScreen(Screen):
    pass


class Map(MapView):
    pass


class ManeuverIcon(MapMarker):
    pass


class DroneIcon(MapMarker):
    pass


class ControllerIcon(MapMarker):
    pass


ms = MapScreen()
m = Map()
sm = ScreenManager()
sm.switch_to(ms)


class GUIApp(App):
    icon = os.path.abspath("icons/DroneIcon.png")
    title = "Halo Controller"

    def build(self):
        # os.chdir("..")
        # os.chdir("GUI")
        print os.path.abspath("")
        return sm


if __name__ == '__main__':
    GUIApp().run()