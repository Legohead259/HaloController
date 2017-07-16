from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.gesture import Gesture
# import json
from gestures import *
from kivy.graphics import Line
from kivy.uix.widget import Widget
# from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from libs.garden.mapview import *
from util import *
# from kivy.clock import Clock


# -----BEGIN INITIALIZATION-----


colors = Colors()

loc = "D:\Projects\HaloController\Settings.json"
with open(loc) as settings_file:
    settings = json.load(settings_file)

Window.size = (480, 320)
Window.clearcolor = colors.white
Builder.load_file("GUI.kv")

sm = ScreenManager()
cur_screen = 0

coord_enabled = False


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
        print "Switching to: " + sm.current  # Debug


def previous_screen():
    """
    Directs the screen manager to proceed to the previous screen
    """
    global cur_screen
    if cur_screen > 0:
        cur_screen -= 1
        sm.switch_to(screens[cur_screen], direction="right")
        print "Switching to: " + sm.current  # Debug


def update_json(l):

    with open(l, "w") as settings_file_w:
        json.dump(settings, settings_file_w, indent=4)


# -----END UTILITY METHODS-----

# -----BEGIN GUI OBJECTS-----


class Background(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__()
        self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self.keyboard.bind(on_key_down=self.on_keyboard_down)

    def keyboard_closed(self):
        self.keyboard.unbind(on_key_down=self.on_keyboard_down)
        self.keyboard = None

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == "left":
            previous_screen()
            # print "left"  # Debug
        elif keycode[1] == "right":
            next_screen()
            # print 'right'  # Debug
        elif keycode[1] == "c":
            global coord_enabled
            coord_enabled = not coord_enabled
            # print coord_enabled  # Debug
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
        return "D:\Projects\HaloController\GUI\Icons\GPS Icon.png"
        # TODO: Change to read from the file path dynamically

    @staticmethod
    def get_drone_gps_connection():
        """
        Gets the GPS signal strength of the drone
        :return: Number of GPS satellites currently being received by the drone
        """
        # TODO: Implement gps connection code
        return "D:\Projects\HaloController\GUI\Icons\GPS Icon.png"
        # TODO: Change to read from the file path dynamically

    @staticmethod
    def get_drone_connection():
        """
        Gets the connection between the controller and the drone
        :return: The connection between the controller and the drone
        """
        # TODO: Implement drone connection code
        return "D:\Projects\HaloController\GUI\Icons\Connection Icon Full.png"
        # TODO: Change to read from the file path dynamically

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


class Footer(BoxLayout):
    text_color = colors.black
    background_color = colors.thanics_blue
    disabled = False


class FlightStats(Screen):
    text_color = colors.black
    background_color = colors.white
    header_enabled = settings["pages"]["flight_stats"]["header"]
    # print(header_enabled)  # Debug
    footer_enabled = settings["pages"]["flight_stats"]["footer"]
    # print(footer_enabled)  # Debug

    def __init__(self, **kwargs):
        super(Screen, self).__init__()
        self.update()
        self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self.keyboard.bind(on_key_down=self.on_keyboard_down)

    def keyboard_closed(self):
        self.keyboard.unbind(on_key_down=self.on_keyboard_down)
        self.keyboard = None

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'w':
            print 'w'
        elif keycode[1] == 's':
            print 's'
        elif keycode[1] == 'up':
            print 'up'
        elif keycode[1] == 'down':
            print 'down'
        return True

    def update(self):
        pass

    def update_hf(self):
        if self.header_enabled:
            self.ids.FlightStats.header.opacity = 1
        else:
            Screen.ids.FlightStats.header.opacity = 0

        if self.header_disabled:
            self.ids.FlightStats.footer.opacity = 1
        else:
            self.ids.FlightStats.footer.opacity = 0


class MapScr(Screen):
    text_color = colors.black
    background_color = colors.white
    header_enabled = settings["pages"]["map"]["header"]
    # print(header_enabled)  # Debug
    footer_enabled = settings["pages"]["map"]["footer"]
    # print(footer_enabled)  # Debug
    zoom = 16
    con_lat = 39
    con_lon = -77
    drone_lat = 39
    drone_lon = -77

    def __init__(self, **kwargs):
        super(Screen, self).__init__()
        self.update()
        self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self.keyboard.bind(on_key_down=self.on_keyboard_down)

    def keyboard_closed(self):
        self.keyboard.unbind(on_key_down=self.on_keyboard_down)
        self.keyboard = None

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'w':
            print 'w'
        elif keycode[1] == 's':
            print 's'
        elif keycode[1] == 'up':
            print 'up'
        elif keycode[1] == 'down':
            print 'down'
        return True

    def get_cur_con_lat(self):
        # TODO: Implement getting current controller latitude
        return 39

    def get_cur_con_lon(self):
        # TODO: Implement getting current controller longitude
        return -77

    def get_cur_drone_lat(self):
        # TODO: Implement getting current drone latitude
        return 39

    def get_cur_drone_lon(self):
        # TODO: Implement getting current drone longitude
        return -77

    def update_hf(self):
        if self.header_enabled:
            self.ids.FlightStats.header.opacity = 1
        else:
            Screen.ids.FlightStats.header.opacity = 0

        if self.header_disabled:
            self.ids.FlightStats.footer.opacity = 1
        else:
            self.ids.FlightStats.footer.opacity = 0

    def update_zoom(self):
        # TODO: Implement changing zoom level
        return 16

    def update(self):
        self.zoom = self.update_zoom()
        self.con_lat = self.get_cur_con_lat()
        self.con_lon = self.get_cur_con_lon()
        self.drone_lat = self.get_cur_drone_lat()
        self.drone_lon = self.get_cur_drone_lon()


class Map(MapView):
    def on_touch_down(self, touch):
        if coord_enabled:
            print self.get_latlon_at(touch.x, touch.y, self.zoom)
        else:
            super(MapView, self).on_touch_down(touch)


class ToolBar(Footer):
    """
    Tool bar for the map.
    If enabled, this will displace the flight stats in the toolbar and have several flight maneuver icons.
    For further documentation on the flight maneuvers, see their respective classes.
    """
    pass


class ManeuverIcon(Icon):
    pass


class Video(Screen):
    text_color = colors.black
    background_color = colors.white
    header_enabled = settings["pages"]["video"]["header"]
    # print(header_enabled)  # Debug
    footer_enabled = settings["pages"]["video"]["footer"]
    # print(footer_enabled)  # Debug

    def update_hf(self):
        if self.header_enabled:
            self.ids.FlightStats.header.opacity = 1
        else:
            Screen.ids.FlightStats.header.opacity = 0

        if self.header_disabled:
            self.ids.FlightStats.footer.opacity = 1
        else:
            self.ids.FlightStats.footer.opacity = 0


class Diagnostics(Screen):
    text_color = colors.black
    background_color = colors.white


class SettingsButton(Button):
    text_color = colors.black
    background_color = colors.thanics_blue


class SettingsLabel(Label):
    text_color = colors.white
    background_color = colors.thanics_blue


class SettingsSwitch(Switch):
    pass


class Settings(Screen):
    text_color = colors.black
    background_color = colors.white
    true_color = colors.green
    false_color = colors.red
    settings = settings

    @staticmethod
    def update_settings():
        confirm_button = Button(text="Confirm Changes")
        popup = Popup(content=confirm_button, title="")
        confirm_button.bind(on_press=popup.dismiss)
        confirm_button.bind(on_press=update_json(loc))
        popup.open()


screens = [FlightStats(), MapScr(), Video(), Diagnostics(), Settings()]


class GUIApp(App):
    sm.switch_to(screens[0])

    def build(self):
        return sm

if __name__ == '__main__':
    GUIApp().run()


# -----END GUI OBJECTS-----
