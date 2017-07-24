from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.gesture import Gesture
# import json
from gestures import *
from kivy.graphics import Line
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from libs.garden.mapview import *
from util import *
from kivy.clock import Clock
import os
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import NumericProperty, StringProperty


# -----BEGIN INITIALIZATION-----


colors = Colors()

os.chdir("..")
settings_loc = os.path.abspath("Settings.json")
# print settings_loc  # Debug
os.chdir("GUI")
# print os.path.abspath("")  # Debug

with open(settings_loc) as settings_file:
    settings = json.load(settings_file)

Window.size = (480, 320)
Window.clearcolor = colors.white
Builder.load_file("GUI.kv")

cur_screen = 0

coord_enabled = False
flight_stats = {"vx": 0, "vy": 0, "vz": 0, "ax": 0, "ay": 0, "az": 0, "pitch": 0, "roll": 0, "yaw": 0, "alt": 0,
                "dist": 0, "vu": settings["general"]["units"]["velocity"],
                "au": settings["general"]["units"]["acceleration"], "mu": settings["general"]["units"]["measurement"]}


# -----END INITIALIZATION-----

# -----BEGIN UTILITY METHODS-----


def next_screen():
    """
    Directs the screen manager to proceed to the next screen
    """
    global cur_screen
    if cur_screen < len(screens) - 1:
        cur_screen += 1
        sm.switch_to(screens[cur_screen], direction="left")
        # print "Switching to: " + sm.current  # Debug


def previous_screen():
    """
    Directs the screen manager to proceed to the previous screen
    """
    global cur_screen
    if cur_screen > 0:
        cur_screen -= 1
        sm.switch_to(screens[cur_screen], direction="right")
        # print "Switching to: " + sm.current  # Debug


def update_settings():
    """
    Updates the settings json
    """
    with open(settings_loc, "w") as settings_file_w:
        json.dump(settings, settings_file_w, indent=4)


# -----END UTILITY METHODS-----

# -----BEGIN GUI OBJECTS-----


class Background(Screen):
    """
    This class will run in the background of all screens on the GUI.
    During development, keyboard inputs will be substituted for the actual controller inputs.
    When properly implemented, this class will check for inputs from all of the inputs and adjust the screen accordingly
    """

    # TODO: Update to handle keyboard (during dev) and controller board (during deployment) inputs
    # TODO: Update to automatically switch between keyboard and controller board inputs

    def __init__(self, **kwargs):
        super(Screen, self).__init__()
        self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self.keyboard.bind(on_key_down=self.on_keyboard_down)

    def keyboard_closed(self):
        """
        Method for closing keyboard connection to GUI
        """
        self.keyboard.unbind(on_key_down=self.on_keyboard_down)
        self.keyboard = None

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        """
        Method for when the key on the keyboard is pressed.
        """
        if keycode[1] == "left":
            previous_screen()
            # print "left"  # Debug
        elif keycode[1] == "right":
            next_screen()
            # print 'right'  # Debug
        # elif keycode[1] == "c":
        #     global coord_enabled
        #     coord_enabled = not coord_enabled
        #     # print coord_enabled  # Debug
        elif keycode[1] == "=":
            global flight_stats
            flight_stats["vx"] += 1
            # print flight_stats["vx"]

        return True


class GestureBox(Widget):
    """
    This class creates a box that encompasses the entire window.
    In this box, gestures can be made by clicking and dragging the cursor in a direction.
    Behaviors can be defined in the 'on_touch_up' method.
    To create a new gesture, follow the documentation in the 'gestures.py' file.
    """
    @staticmethod
    def make_gesture(point_list):
        """
        Creates a gesture for recognition in the 'on_touch_up' method
        :param point_list: the list of points created by the gesture
        :return: the gesture in a string format
        """
        g = Gesture()
        g.add_stroke(point_list)
        g.normalize()
        return g

    def __init__(self, *args, **kwargs):
        super(GestureBox, self).__init__()
        self.gdb = GestureDatabase()
        self.gdb.add_gesture(swipe_l_r)
        self.gdb.add_gesture(swipe_r_l)

    def on_touch_down(self, touch):
        """
        Method that starts the gesture recognition when the click is first clicked down
        :param touch: the touch created by the user
        :return: True when touch is down and the widget is not disabled
        """
        if not self.disabled:
            user_data = touch.ud
            user_data['line'] = Line(points=(touch.x, touch.y))
            # print touch.x, touch.y  # Debug
            return True
        else:
            pass

    def on_touch_move(self, touch):
        """
        Method that records the movement of the touch
        :param touch: the touch created by the user
        :return: True when touch is moving and the widget is not disabled
        """
        if not self.disabled:
            try:
                touch.ud['line'].points += [touch.x, touch.y]
            except KeyError:
                pass
            return True
        else:
            pass

    def on_touch_up(self, touch):
        """
        Method that checks the performed gesture and performs the assigned actions
        :param touch: the touch created by the user
        :return: True when touch is gone
        """
        if not self.disabled:
            global cur_screen
            try:
                gesture = self.make_gesture(list(zip(touch.ud['line'].points[::2], touch.ud['line'].points[1::2])))

                # print("Left to Right:", gesture.get_score(swipe_l_r))  # Debug
                # print("Right to Left:", gesture.get_score(swipe_r_l))  # Debug

                gesture2 = self.gdb.find(gesture, minscore=settings["general"]["touch_min_score"])

                # print(gesture2)  # Debug

                if gesture2 is None:
                    return

                if gesture2[1] == swipe_l_r:
                    if cur_screen > 0:
                        previous_screen()
                    # print "L-R"  # Debug
                elif gesture2[1] == swipe_r_l:
                    next_screen()
                    # print "R-L"  # Debug
            except KeyError or TypeError:
                pass
        else:
            pass


class Icon(Widget):
    """
    Superclass for any icons used in the GUI
    """
    pass


class Header(GridLayout):
    """
    Top portion of the GUI that contains the connectivity stats and battery level.
    The connectivity stats are for GPS and WiFi.
    """
    text_color = colors.black
    background_color = colors.thanics_blue
    disabled = False
    battery_conversion_factor = None
    battery_level_color = None
    left_image = os.path.abspath("icons/CockpitTL.png")
    # print left_image  # Debug
    right_image = os.path.abspath("icons/CockpitTR.png")
    # print right_image  # Debug
    battery_image = os.path.abspath("icons/Battery.png")
    # print battery_image  # Debug

    def __init__(self, **kwargs):
        super(Header, self).__init__(**kwargs)
        self.update()

    @staticmethod
    def get_con_gps_connection():
        """
        Gets the GPS signal strength of the controller
        :return: Number of GPS satellites currently being received by the controller
        """
        # TODO: Implement gps connection code
        return os.path.abspath("icons/GPSIcon.png")

    @staticmethod
    def get_drone_gps_connection():
        """
        Gets the GPS signal strength of the drone
        :return: Number of GPS satellites currently being received by the drone
        """
        # TODO: Implement gps connection code
        return os.path.abspath("icons/GPSIcon.png")

    @staticmethod
    def get_drone_connection():
        """
        Gets the connection between the controller and the drone
        :return: The connection between the controller and the drone
        """
        # TODO: Implement drone connection code
        return os.path.abspath("icons/ConnectionIconFull.png")

    @staticmethod
    def update_battery_bar():
        """
        Updates the battery bar indicating the current battery charge
        """
        FULL_WIDTH = 40
        REF_VOLT = 1.2

        cur_volt = 4.2 - 3  # TODO: Implement battery level retriever

        if cur_volt >= 0:
            cur_percent = cur_volt / REF_VOLT
            # print cur_percent  # Debug
            conversion_factor = int((FULL_WIDTH * (1-cur_percent)))
            # print conversion_factor  # Debug

            if cur_percent <= .25:
                color = colors.red
            else:
                color = colors.green
            return [conversion_factor, color]  # width, height, color
        else:
            return [FULL_WIDTH, colors.red]

    def update(self):
        """
        Called periodically to update the stats in the header bar
        """
        batt_bar = self.update_battery_bar()
        self.battery_conversion_factor = batt_bar[0]
        self.battery_level_color = batt_bar[1]


class HeaderIcon(Icon):
    """
    Icon for the header of the GUI
    """
    pass


class Footer(GridLayout):
    """
    Footer of the GUI.
    The speed (x/y/z), acceleration, distance from home, and altitude will be displayed here
    """
    # TODO: Implement getting and displaying stats
    text_color = colors.black
    text_size = 10
    background_color = colors.thanics_blue
    disabled = False

    vel_x = NumericProperty(flight_stats["vx"])
    vel_y = NumericProperty(flight_stats["vy"])
    vel_z = NumericProperty(flight_stats["vz"])
    acc_x = NumericProperty(flight_stats["ax"])
    acc_y = NumericProperty(flight_stats["ay"])
    acc_z = NumericProperty(flight_stats["az"])
    altitude = NumericProperty(flight_stats["alt"])
    dist_from_home = NumericProperty(flight_stats["dist"])
    vel_unit = StringProperty(flight_stats["vu"])
    acc_unit = StringProperty(flight_stats["au"])
    meas_unit = StringProperty(flight_stats["mu"])

    def __init__(self, **kwargs):
        super(GridLayout, self).__init__()

        labels = {"vx": FSLabel(text="[b]vel_x: [/b]" + str(self.vel_x) + self.vel_unit, id='vx_label')}

        for l in labels:
            self.add_widget(labels.get(l))
            print labels.get(l)
            print self.children
            print self.ids

    def update(self, *args):
        # print "Updating Footer..."  # Debug
        # print flight_stats  # Debug
        # self.vel_x = flight_stats["vx"]
        # # self.ids.vel_x_label.text = "[b]vel_x: [/b]" + str(self.vel_x) + self.vel_unit
        # print self.vel_x  # Debug
        # print flight_stats["vx"]
        # # print self.ids.vel_x_label.text
        # print self.ids
        # app = App.get_running_app()
        # print app
        # self.vel_y = flight_stats["vy"]
        # self.vel_z = flight_stats["vz"]
        # self.acc_x = flight_stats["ax"]
        # self.acc_y = flight_stats["ay"]
        # self.acc_z = flight_stats["az"]
        # self.altitude = flight_stats["alt"]
        # self.dist_from_home = flight_stats["dist"]
        # self.vel_unit = flight_stats["vu"]
        # self.acc_unit = flight_stats["au"]
        # self.meas_unit = flight_stats["mu"]
        pass


class FlightStats(Screen):
    """
    Screen that will have a 3D render of the drone properly orientated relative to the controller (yaw) and zeroes.
    The drone will be rendered with an arrow pointed forward and its motion will all be rendered in real-time.
    """
    text_color = colors.black
    background_color = colors.white
    header_enabled = settings["pages"]["flight_stats"]["header"]
    # print(header_enabled)  # Debug
    footer_enabled = settings["pages"]["flight_stats"]["footer"]
    # print(footer_enabled)  # Debug

    def __int__(self, **kwargs):
        super(Screen, self).__init__()
        self.update()
        self.update_hf()

    def get_velocity(self):
        """
        Updates velocity values for the drone
        :return: The x and y velocity of the drone respectively
        """
        global vel_x, vel_y, vel_z
        vel_x = 0  # TODO: Implement getting value
        # print vel_x  # Debug
        vel_y = 0  # TODO: Implement getting value
        # print vel_y  # Debug
        vel_z = 0  # TODO: Implement getting value
        # print vel_z  # Debug

        return vel_x, vel_y, vel_z

    def get_acceleration(self):
        """
        Updates acceleration values for the drone
        :return: The x and y acceleration of the drone respectively
        """
        global acc_x, acc_y, acc_z
        acc_x = 0  # TODO: Implement getting value
        # print acc_x  # Debug
        acc_y = 0  # TODO: Implement getting value
        # print acc_y  # Debug
        acc_z = 0  # TODO: Implement getting value
        # print acc_z  # Debug

        return acc_x, acc_y, acc_z

    def get_axes(self):
        """
        Updates axes values for the drone
        :return: The pitch, roll, and yaw of the drone respectively
        """
        global pitch, roll, yaw
        pitch = 0  # TODO: Implement getting value
        # print pitch  # Debug
        roll = 0  # TODO: Implement getting value
        # print roll  # Debug
        yaw = 0  # TODO: Implement getting value
        # print yaw  # Debug

        return pitch, roll, yaw

    def get_dist_from_home(self):
        """
        Updates the distance the drone is away from home (where it first activated
        The drone will send 
        :return: The distance from home in
        """
        global dist_from_home
        dist_from_home = 0  # TODO: Implement getting value
        return dist_from_home

    def update(self):
        """
        Lumps all of the flight stats updates into one.
        For specific documentation, refer to the respective method
        """
        # print "Updating Flight Stats..."  # Debug

        self.get_velocity()
        self.get_acceleration()
        self.get_axes()

    def update_hf(self):
        """
        Enables or disables the header and footer based on user preference
        """
        # TODO: Better Implement
        if self.header_enabled:
            self.ids.FlightStats.header.opacity = 1
        else:
            Screen.ids.FlightStats.header.opacity = 0

        if self.header_disabled:
            self.ids.FlightStats.footer.opacity = 1
        else:
            self.ids.FlightStats.footer.opacity = 0


class FSLabel(Label):
    font_size = 15
    text_color = colors.white
    markup = True


class MapScr(Screen):
    """
    The map screen of the controller.
    A local map is rendered and displayed that the user can zoom, pan, and select different coordinates on.
    Upon first run of the controller, the user can enable or disable auto updates.
    With auto-updates, the controller will get its own coordinates and generate a map that renders a user-defined
        radius around the controller's current location.
    Without auto-updates, the user will have to pre-load coordinates for the controller to render.
    Relative tracking will allow users to track their drone relative to the controller (themselves).
    However, a phone must be plugged in for this feature to be enabled (this can be overridden in settings).
    If the controller or the drone are marked in the default location (Tesla's Headquarters in Palo Alto, CA), please
        check that the GPS unit on your phone/drone are functioning properly.
    """
    text_color = colors.black
    background_color = colors.white
    header_enabled = settings["pages"]["map"]["header"]
    # print(header_enabled)  # Debug
    footer_enabled = settings["pages"]["map"]["footer"]
    # print(footer_enabled)  # Debug

    def update_hf(self):
        """
        Enables or disables the header and footer based on user preference
        """
        if self.header_enabled:
            self.ids.FlightStats.header.opacity = 1
        else:
            Screen.ids.FlightStats.header.opacity = 0

        if self.header_disabled:
            self.ids.FlightStats.footer.opacity = 1
        else:
            self.ids.FlightStats.footer.opacity = 0

    def update(self):
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
                print self.marker_lat, self.marker_lon  # Debug

            else:
                super(MapView, self).on_touch_down(touch)

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


class ToolBar(Footer):
    """
    Tool bar for the map.
    If enabled, this will displace the flight stats in the toolbar and have several flight maneuver icons.
    For further documentation on the flight maneuvers, see their respective classes.
    """
    pass


class ManeuverIcon(Image, ButtonBehavior, Widget):
    """
    Class for the different maneuvers that can be dragged onto the map for execution
    """
    move_to_icon = os.path.abspath("icons/DroneIcon.png")

    @staticmethod
    def update_map_mode():
        global coord_enabled
        coord_enabled = not coord_enabled
        print coord_enabled  # Debug


class ManeuverMarker(MapMarker):
    pass


class Video(Screen):
    """
    Screen that will display a live feed from the Mobius camera on the drone.
    The user will be able to rotate the 360 degree image by swiping or choosing a 360-degree static render.
    """
    text_color = colors.black
    background_color = colors.white
    header_enabled = settings["pages"]["video"]["header"]
    # print(header_enabled)  # Debug
    footer_enabled = settings["pages"]["video"]["footer"]
    # print(footer_enabled)  # Debug

    def update_hf(self):
        """
        Turns on/off the header/footer based on user preference.
        """
        if self.header_enabled:
            self.ids.FlightStats.header.opacity = 1
        else:
            Screen.ids.FlightStats.header.opacity = 0

        if self.header_disabled:
            self.ids.FlightStats.footer.opacity = 1
        else:
            self.ids.FlightStats.footer.opacity = 0


class Diagnostics(Screen):
    """
    Screen that will display live diagnostics of the drone including battery life expectancy, cpu status, 
        motor efficiency and others
    """
    text_color = colors.black
    background_color = colors.white
    # TODO: Implement


class SettingsButton(Button):
    """
    Button that will toggle specified setting
    """
    text_color = colors.black
    background_color = colors.thanics_blue


class SettingsLabel(Label):
    """
    Label for settings
    """
    text_color = colors.white
    background_color = colors.thanics_blue


class SettingsSwitch(Switch):
    """
    Switch that will enable/disable specified setting
    """
    pass


class Settings(Screen):
    """
    Screen where user can choose preferences to personalize the controller experience to their liking.
    Every aspect of the drone and controller is configurable on this screen.
    Default profiles will be loaded for each flight mode and can be individually configured by the user.
    """
    text_color = colors.black
    background_color = colors.white
    true_color = colors.green
    false_color = colors.red
    settings = settings

    @staticmethod
    def settings_popup():
        """
        Creates a popup window in the settings screen that asked user to confirm the changed settings.
        Is only activated if changes have been made
        """
        confirm_button = Button(text="Confirm Changes")
        popup = Popup(content=confirm_button, title="Confirm Changes")
        confirm_button.bind(on_press=popup.dismiss)
        confirm_button.bind(on_press=update_settings())
        popup.open()

fs = FlightStats()
m = MapScr()
v = Video()
d = Diagnostics()
s = Settings()
f = Footer()

screens = [fs, m, v, d, s]


class GUIManager(ScreenManager):
    pass

sm = GUIManager()


class GUIApp(App):
    sm.switch_to(screens[0])
    icon = os.path.abspath("icons/DroneIcon.png")
    title = "Controller GUI"

    def build(self):
        Clock.schedule_interval(self.update, 0.25)
        # Clock.schedule_interval(f.update, 1)
        return sm

    def update(self, *args):
        """
        Updates all of the data streams
        """
        f.update()

        if sm.current == m.name:
            m.ids.map.update()
        elif sm.current == fs.name:
            fs.update()

if __name__ == '__main__':
    GUIApp().run()


# -----END GUI OBJECTS-----
