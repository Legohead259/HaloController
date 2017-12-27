from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
import os

from kivy.properties import StringProperty
from kivy.uix.actionbar import ActionPrevious, ActionBar
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen

from libs.garden import MapView
from util import Colors, settings

colors = Colors()

Window.size = (480, 320)
Window.clearcolor = colors.white
Builder.load_file("Gui.kv")


class Header(GridLayout):
    pass


class Footer(ActionBar):
    pass


sm = ScreenManager()


class GUIApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    GUIApp().run()