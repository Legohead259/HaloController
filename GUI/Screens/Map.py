import os

from kivy.properties import NumericProperty, StringProperty
from kivy.uix.actionbar import ActionButton
from kivy.uix.screenmanager import Screen
from requests import ConnectionError

from libs.garden import MapView, MapMarker
from util import settings, get_controller_geo_ip

coord_enabled = False

maneuver_icon = StringProperty("")


class MapScreen(Screen):
    def __init__(self, **kw):
        super(MapScreen, self).__init__(**kw)


class Map(MapView):
    try:
        """Put anything that requires an internet connection for the map here
        """
        controller_coords = get_controller_geo_ip()
        lat = NumericProperty(controller_coords[0])
        lon = NumericProperty(controller_coords[1])
    except ConnectionError:
        """Put any connection failed code here
        """
        print "Failed to connect!"

    def set_marker_position(self, marker):
        x, y = self.get_window_xy_from(marker.lat, marker.lon, self.zoom)
        marker.x = int(x - marker.width * marker.anchor_x)
        marker.y = int(y - marker.height * marker.anchor_y)
        if isinstance(marker, MapMarker):
            marker.placeholder.x = marker.x - marker.width / 2
            marker.placeholder.y = marker.y + marker.height

    def on_touch_down(self, touch):
        if coord_enabled:
            self.set_marker_position()
            maneuver = ManeuverIcon(source=maneuver_icon)
            self.add_marker(maneuver)
            print "Placing marker at:"
        else:
            super(MapView, self).on_touch_down(touch)


class ManeuverIcon(MapMarker):
    pass


class DroneIcon(MapMarker):
    pass


class ControllerIcon(MapMarker):
    pass


class ManeuverButton(ActionButton):
    def update_marker_data(self, m):
        global maneuver_icon, coord_enabled

        if m == "Orbit":
            maneuver_icon = os.path.abspath("icons/MissingTexture.png")
            coord_enabled = True
            print "Setting ORBIT maneuver"  # Debug
            print "Coordinates Enabled:", coord_enabled
        # TODO: Implement rest of logic for other marker types
