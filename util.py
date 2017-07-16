import json

loc = "D:\Projects\HaloController\Settings.json"
with open(loc) as settings_file:
    settings = json.load(settings_file)


class Colors():
    thanics_blue = None
    white = None
    black = None
    green = None
    red = None

    def __init__(self):
        self.thanics_blue = self.convert_rgb_values(settings["general"]["colors"]["thanics_blue"])
        # print misc_color  # Debug
        self.white = self.convert_rgb_values(settings["general"]["colors"]["white"])
        # print bg_color  # Debug
        self.black = self.convert_rgb_values(settings["general"]["colors"]["black"])
        # print txt_color  # Debug
        self.green = self.convert_rgb_values(settings["general"]["colors"]["green"])
        # print true_color  # Debug
        self.red = self.convert_rgb_values(settings["general"]["colors"]["red"])
        # print false_color  # Debug

    def convert_rgb_values(self, val):
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


def next_screen(cs, s, sm):
    temp = cs
    temp += 1
    sm.switch_to(s[temp], direction="left")
    return temp
