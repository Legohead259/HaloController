import os

from kivy.properties import NumericProperty, StringProperty
from kivy.uix.actionbar import ActionButton
from kivy.uix.screenmanager import Screen
from requests import ConnectionError

from libs.garden import MapView, MapMarker
from util import settings, get_controller_geo_ip

coord_enabled = False

maneuver_icon = StringProperty("")

try:
    """Put anything that requires an internet connection for the map here
    """
    controller_coords = get_controller_geo_ip()
    start_lat = controller_coords[0]
    start_lon = controller_coords[1]
except ConnectionError:
    """Put any connection failed code here
    """
    print "Failed to connect!"


class ManeuverIcon(MapMarker):
    pass


class DroneIcon(MapMarker):
    pass


class ControllerIcon(MapMarker):
    pass


class MapScreen(Screen):
    pass


class Map(MapView):
    pass


class ManeuverButton(ActionButton):
    pass
