import os
from kivy.uix.screenmanager import Screen

from libs.garden import MapView, MapMarker
from util import settings

coord_enabled = False


class MapScreen(Screen):
    pass


class Map(MapView):
    """
    The map that is rendered on the map screen
    """
    con_lat = settings["pages"]["map"]["defaults"]["lat"]
    con_lon = settings["pages"]["map"]["defaults"]["lon"]
    drone_lat = settings["pages"]["map"]["defaults"]["lat"]
    drone_lon = settings["pages"]["map"]["defaults"]["lon"]
    drone_icon = os.path.abspath("icons/DroneIcon.png")
    con_icon = os.path.abspath("icons/ControllerIcon.png")
    marker_lat = None
    marker_lon = None
    marker_height = 25
    con_gps_enabled = True

    def __init__(self, **kwargs):
        super(Map, self).__init__(**kwargs)
        self.update()

    def on_touch_down(self, touch):
        if 50 < touch.y < 270:  # Checks to see if the touch is between the header and footer
            if coord_enabled:
                self.marker_lat, self.marker_lon = self.get_latlon_at(touch.x, touch.y, self.zoom)
                print(self.marker_lat, self.marker_lon)  # Debug
                self.set_marker_pos()
            else:
                super(MapView, self).on_touch_down(touch)

    def set_marker_pos(self, marker):
        x, y = self.get_window_xy_from(marker.lat, marker.lon, self.zoom)
        marker.x = int(x - marker.width * marker.anchor_x)
        marker.y = int(y - marker.height * marker.anchor_y)
        if isinstance(marker, MapMarker):
            marker.placeholder.x = marker.x - marker.width / 2
            marker.placeholder.y = marker.y + marker.height

    def get_con_gps(self):
        """
        Returns if the controller has GPS available
        :return: Controller GPS enabled
        """
        # TODO: Implement controller GPS check
        self.con_gps_enabled = False
        return self.con_gps_enabled

    def get_cur_con_lat(self):
        """
        Gets the current latitude of the controller
        """
        # TODO: Implement getting current controller latitude
        if self.con_gps_enabled:
            self.con_lat = 39
            return self.con_lat
        else:
            return

    def get_cur_con_lon(self):
        """
        Gets the current longitude of the controller
        """
        # TODO: Implement getting current controller longitude
        if self.con_gps_enabled:
            self.con_lon = -77
            return self.con_lon
        else:
            return

    def get_cur_drone_lat(self):
        """
        Gets the current latitude of the drone
        """
        # TODO: Implement getting current drone latitude
        self.drone_lat = 39.0005
        return self.drone_lat

    def get_cur_drone_lon(self):
        """
        Gets the current longitude of the drone
        """
        # TODO: Implement getting current drone longitude
        self.drone_lon = -77.0001
        return self.drone_lon

    def update(self, *args):
        """
        Simplifies updating updating coordinate information for controller and drone
        """
        # print "Updating Map..."  # Debug
        # cx, cy = self.get_window_xy_from(self.con_lat, self.con_lon, self.zoom)
        # dx, dy = self.get_window_xy_from(self.drone_lat, self.drone_lon, self.zoom)

        # with self.canvas:
        # l = Line(points=[cx, cy, dx, dy])
        # self.canvas.add(l)
        # self.canvas.remove(l)

        if self.con_gps_enabled:
            self.con_lat = self.get_cur_con_lat()
            # print self.con_lat  # Debug
            self.con_lon = self.get_cur_con_lon()
            # print self.con_lon  # Debug

        self.drone_lat = self.get_cur_drone_lat()
        # print self.drone_lat  # Debug
        self.drone_lon = self.get_cur_drone_lon()
        # print self.drone_lon  # Debug
        self.con_gps_enabled = self.get_con_gps()
        # print self.con_gps_enabled  # Debug

