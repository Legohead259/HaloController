import sys
from kivy.base import runTouchApp
from kivy.lang import Builder

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from libs.garden.mapview import *


class Map(MapView):
    pass

root = Builder.load_string("""
#:import sys sys
Map:
    lat: 50.6394
    lon: 3.057
    zoom: 13
    map_source: MapSource(sys.argv[1], attribution="") if len(sys.argv) > 1 else "osm"

    MapMarker:
        lat: 50.6394
        lon: 3.057
        

""")

runTouchApp(root)
