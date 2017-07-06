from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.gesture import GestureDatabase, Gesture
import json
from gestures import swipe_l_r, swipe_r_l
from kivy.graphics import Line
from kivy.uix.widget import Widget
# from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from libs.garden.mapview import *


loc = "D:\Projects\HaloController\Settings.json"
with open(loc) as settings_file:
    settings = json.load(settings_file)


def convert_rgb_values(val):
    con_val = []
    count = 0
    while count != 3:
        x = val[count]
        x /= 255
        con_val.append(x)
        # print con_val # Debug
        count += 1
    con_val.append(val[3])
    return con_val

thanics_blue = convert_rgb_values(settings["general"]["colors"]["thanics_blue"])
# print misc_color  # Debug
white = convert_rgb_values(settings["general"]["colors"]["white"])
# print bg_color  # Debug
black = convert_rgb_values(settings["general"]["colors"]["black"])
# print txt_color  # Debug
green = convert_rgb_values(settings["general"]["colors"]["green"])
# print true_color  # Debug
red = convert_rgb_values(settings["general"]["colors"]["red"])
# print false_color  # Debug

Window.size = (480, 320)
Window.clearcolor = white
Builder.load_file("GUI.kv")

sm = ScreenManager()
cur_screen = 0


class Header(GridLayout):
    text_color = black
    background_color = thanics_blue
    disabled = False
    battery_conversion_factor = None
    battery_level_color = None

    def __init__(self, **kwargs):
        super(Header, self).__init__(**kwargs)
        self.update()

    def get_gps_connection(self):
        # TODO Implement gps connection code
        return "D:\Projects\Halo Controller\GUI Icons\GPS Icon.png"

    def get_drone_connection(self):
        # TODO Implement drone connection code
        return "D:\Projects\Halo Controller\GUI Icons\Connection Icon Full.png"

    @staticmethod
    def update_battery_bar():
        FULL_WIDTH = 40
        REF_VOLT = 1.2

        cur_volt = 4.2 - 3  # TODO: Implement battery level retriever

        if cur_volt >= 0:
            cur_percent = cur_volt / REF_VOLT
            # print cur_percent  # Debug
            conversion_factor = int((FULL_WIDTH * (1-cur_percent)))
            # print conversion_factor  # Debug

            if cur_percent <= .25:
                color = red
            else:
                color = green
            return [conversion_factor, color]  # width, height, color
        else:
            return [40, red]

    def update(self):
        batt_bar = self.update_battery_bar()
        self.battery_conversion_factor = batt_bar[0]
        self.battery_level_color = batt_bar[1]


class Footer(BoxLayout):
    text_color = black
    background_color = thanics_blue
    disabled = False

    def next_screen():
        if cur_screen < len(screens) - 1:
            cur_screen += 1
            sm.switch_to(screens[cur_screen], direction="left")
            print "Switching to: " + sm.current  # Debug

    def previous_screen(self):
        if self.cur_screen > 0:
            self.cur_screen -= 1
            sm.switch_to(screens[self.cur_screen], direction="right")
            print "Switching to: " + sm.current  # Debug


class GestureBox(Widget):
    @staticmethod
    def make_gesture(name, point_list):
        g = Gesture()
        g.add_stroke(point_list)
        g.normalize()
        g.name = name
        return g

    def __init__(self, *args, **kwargs):
        super(GestureBox, self).__init__()
        self.gdb = GestureDatabase()
        self.gdb.add_gesture(swipe_l_r)
        self.gdb.add_gesture(swipe_r_l)

    def on_touch_down(self, touch):
        user_data = touch.ud
        user_data['line'] = Line(points=(touch.x, touch.y))
        # print touch.x, touch.y  # Debug
        return True

    def on_touch_move(self, touch):
        try:
            touch.ud['line'].points += [touch.x, touch.y]
        except KeyError:
            pass
        return True

    def on_touch_up(self, touch):
        global cur_screen
        try:
            gesture = self.make_gesture('', list(zip(touch.ud['line'].points[::2], touch.ud['line'].points[1::2])))

            # Debug
            # print("Left to Right:", g.get_score(swipe_l_r))
            # print("Right to Left:", g.get_score(swipe_r_l))

            gesture2 = self.gdb.find(gesture, minscore=settings["general"]["touch_min_score"])

            # print(gesture2) # Debug

            if gesture2:
                if gesture2[1] == swipe_l_r:
                    if cur_screen > 0:
                        cur_screen -= 1
                        sm.switch_to(screens[cur_screen], direction="right")
                        print "Switching to: " + sm.current  # Debug
                    # print "L-R"  # Debug
                elif gesture2[1] == swipe_r_l:
                    if cur_screen < len(screens) - 1:
                        cur_screen += 1
                        sm.switch_to(screens[cur_screen], direction="left")
                        print "Switching to: " + sm.current  # Debug
                    # print "R-L"  # Debug
        except KeyError:
            pass


class HeaderIcon(Widget):
    pass


class FlightStats(Screen):
    text_color = black
    background_color = white
    header_enabled = settings["pages"]["flight_stats"]["header"]
    # print(header_enabled)  # Debug
    footer_enabled = settings["pages"]["flight_stats"]["footer"]
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


class ToolBar(Footer):
    pass


class MapView(MapView):
    pass


class Map(Screen):
    text_color = black
    background_color = white
    header_enabled = settings["pages"]["map"]["header"]
    # print(header_enabled)  # Debug
    footer_enabled = settings["pages"]["map"]["footer"]
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


class Video(Screen):
    text_color = black
    background_color = white
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
    text_color = black
    background_color = white


class SettingsButton(Button):
    text_color = black
    background_color = thanics_blue


class SettingsLabel(Label):
    text_color = white
    background_color = thanics_blue


class SettingsSwitch(Switch):
    pass


class Settings(Screen):
    text_color = black
    background_color = white
    true_color = green
    false_color = red
    settings = settings

    def update_settings(self):
        confirm_button = Button(text="Confirm Changes")
        popup = Popup(content=confirm_button, title="")
        confirm_button.bind(on_press=popup.dismiss)
        confirm_button.bind(on_press=self.update_json)
        popup.open()

    @staticmethod
    def update_json(self):
        with open(loc, "w") as settings_file:
            json.dump(settings, settings_file, indent=4)


screens = [Settings(), FlightStats(), Map(), Video(), Diagnostics()]


class GUIApp(App):
    sm.switch_to(screens[0])

    def build(self):
        return sm

if __name__ == '__main__':
    GUIApp().run()
