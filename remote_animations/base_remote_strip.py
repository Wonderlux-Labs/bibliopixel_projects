from bibliopixel.animation import BaseStripAnim
from bibliopixel import colors as bp_colors

class MidiTransform:
    def remap_cc_value(x, out_min, out_max):
        return NumberUtils.remap(x, 0, 127, out_min, out_max)

class NumberUtils:
    def remap(x, in_min, in_max, out_min, out_max):
        value = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        return value

class ColorMidiUtils:
    def three_cc_to_color(red_cc, green_cc, blue_cc):
        red = MidiTransform.remap_cc_value(red_cc, 0, 255)
        green = MidiTransform.remap_cc_value(green_cc, 0, 255)
        blue = MidiTransform.remap_cc_value(blue_cc, 0, 255)
        return(red, green, blue)

    def one_cc_to_color(one_cc):
        c_num = MidiTransform.remap_cc_value(one_cc, 0, 255)
        c = bp_colors.conversions.HUE_RAINBOW[int(c_num)]
        return c

class BaseRemoteStrip(BaseStripAnim):
    def __init__(self, layout, start=0, end=-1, **args):
        super(BaseRemoteStrip, self).__init__(layout, start, end, **args)
        self.color_control = args.get('color_control') or 0
        self.brightness_control = args.get('brightness_control') or 100
        self.randomness_control = args.get('randomness_control') or 0
        self.width_control = args.get('width_control') or 0
        self.count_control = args.get('count_control') or 0
        self.delay_control = args.get('delay_control') or 0
        self.utility_control_one = args.get('utility_control_one') or 0
        self.utility_control_two = args.get('utility_control_two') or 0
        self.use_rgb = args.get('use_rgb') or False
        self.red_control = args.get('red_control') or 50
        self.green_control = args.get('green_control') or  50
        self.blue_control = args.get('blue_control') or 50
        self._color = (255, 255, 255)

    def get_color(self):
        if self.use_rgb:
            c = ColorMidiUtils.three_cc_to_color(self.red_control, self.green_control, self.blue_control)
        else:
            c = ColorMidiUtils.one_cc_to_color(self.color_control)

        c_lev = MidiTransform.remap_cc_value(self.brightness_control, 0, 256)
        self._color = bp_colors.color_scale(c, c_lev)
