import os

import bcolors
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.actionbar import ActionButton
from kivy.uix.button import Button
from kivy.uix.carousel import Carousel
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from requests import ConnectionError

from GUI_V3.Components import *
from libs.garden import MapView, MapMarker, MapMarkerPopup, MarkerMapLayer
from util import settings, get_controller_geo_ip

coord_enabled = False
maneuver_icon = os.path.abspath("icons/MissingTexture.png")

try:
    """Put anything that requires an internet connection for the map here
    """
    controller_coords = get_controller_geo_ip()
    start_lat = NumericProperty(controller_coords[0])
    start_lon = NumericProperty(controller_coords[1])
except ConnectionError:
    """Put any connection failed code here
    """
    print bcolors.FAIL + "Failed to connect!" + bcolors.ENDC

content = None
slider_d = Slider()
slider_hl = Slider(orientation="vertical")
slider_hh = Slider(orientation="vertical")
label_d = Label(text="Diameter:" + str(int(slider_d.value)) + "m")  # TODO: Substitute with user defined unit
label_hl = Label(text="Lowest altitude:" + str(int(slider_hl.value)) + "m")  # TODO: Substitute with user defined unit
label_hh = Label(text="Highest altitude:" + str(int(slider_hh.value)) + "m")  # TODO: Substitute with user defined unit
button = Button(text="Execute")
popup = None


def on_slide(instance, value):
    if instance is slider_d:
        label_d.text = "Diameter:" + str(int(value)) + "m"  # TODO: Substitute with user defined unit
    elif instance is slider_hl:
        label_hl.text = "Lowest Altitude:" + str(int(value)) + "m" # TODO: Substitute with user defined unit
    elif instance is slider_hh:
        label_hh.text = "Highest Altitude:" + str(int(value)) + "m"  # TODO: Substitute with user defined unit


class ManeuverMarker(MapMarkerPopup):
    source = maneuver_icon
    anchor_y = 0.5


class DroneMarker(MapMarker):
    source = StringProperty(os.path.abspath("icons/DroneIcon.png"))
    lat, lon = start_lat, start_lon  # TODO: Update with a get_drone_gps() function
    anchor_y = 0.5


class ControllerMarker(MapMarker):
    source = StringProperty(os.path.abspath("icons/ControllerIcon.png"))
    lat, lon = start_lat, start_lon  # TODO: Update with a get_controller_gps() function
    anchor_y = 0.5


class Map(MapView):
    lat = start_lat
    lon = start_lon
    pause_on_action = False

    def __int__(self):
        self.zoom = 15


class MapScreen(Screen):
    def __init__(self, **kwargs):
        super(MapScreen, self).__init__(**kwargs)
        self.map = Map()
        print self.map.scale  # Debug
        self.header = Header()
        self.footer = Footer()
        self.drone = DroneMarker()
        self.controller = ControllerMarker()
        self.maneuver = ManeuverMarker()

        self.add_widget(self.map)
        self.add_widget(self.header)
        self.add_widget(self.footer)

        self.drone.width = 40
        self.drone.height = 40
        self.map.add_marker(self.drone)

        self.controller.width = 40
        self.controller.height = 40
        self.map.add_marker(self.controller)

        self.maneuver.width = 40
        self.maneuver.height = 40
        self.map.add_marker(self.maneuver)

    def on_touch_down(self, touch):
        global coord_enabled

        if coord_enabled:
            self.maneuver.lat, self.maneuver.lon = self.map.get_latlon_at(touch.x, touch.y, self.map.zoom)
            self.maneuver.source = maneuver_icon
            self.map.trigger_update(False)
            popup.open()
            coord_enabled = False
        else:
            super(MapScreen, self).on_touch_down(touch)


class ManeuverButton(ActionButton):
    @staticmethod
    def update_marker_data(m):
        global maneuver_icon, coord_enabled, content, popup
        content = GridLayout(rows=3)

        if m == "Orbit":
            maneuver_icon = os.path.abspath("icons/MissingTexture.png")
            coord_enabled = True

            content.add_widget(label_d)
            content.add_widget(slider_d)
            content.add_widget(button)
        elif m == "Spiral":
            maneuver_icon = os.path.abspath("icons/MissingTexture.png")
            coord_enabled = True

            content.cols = 2
            content.add_widget(label_hl)
            content.add_widget(label_hh)
            content.add_widget(slider_hl)
            content.add_widget(slider_hh)
            content.add_widget(button)
        elif m == "Follow Me":
            # TODO: Implement follow_me()
            pass
        elif m == "Follow This":
            # TODO: Implement follow_this()
            pass

        popup = Popup(title="%s Maneuver" % m, title_align="center", content=content,
                      size_hint=(None, None), size=(200, 200), auto_dismiss=False)
        button.bind(on_press=popup.dismiss)
        popup.bind(on_dismiss=content.clear_widgets)
        slider_d.bind(value=on_slide)
        slider_hl.bind(value=on_slide)
        slider_hh.bind(value=on_slide)
