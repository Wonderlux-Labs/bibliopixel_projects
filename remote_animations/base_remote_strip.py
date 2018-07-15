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
        hue_num = MidiTransform.remap_cc_value(one_cc, 0, 255)
        color = bp_colors.conversions.HUE_RAINBOW[int(hue_num)]
        return color

class BaseRemoteStrip(BaseStripAnim):
    def __init__(self, layout, start=0, end=-1, color_control=0, brightness_control=100,
                 width_control=0, count_control=0, randomness_control=0, delay_control=0,
                 utility_control_one=0, utility_control_two=0, red_control=127,
                 green_control=127, blue_control=127, use_rgb = False):
        super(BaseRemoteStrip, self).__init__(layout, start, end)
        self.color_control = color_control
        self.brightness_control = brightness_control
        self.randomness_control = randomness_control
        self.width_control = width_control
        self.count_control = count_control
        self.delay_control = delay_control
        self.utility_control_one = utility_control_one
        self.utility_control_two = utility_control_two
        self.use_rgb = use_rgb
        self.red_control = red_control
        self.green_control = green_control
        self.blue_control = blue_control
        self._color = (255, 255, 255)

    def get_color(self):
        if self.use_rgb:
            color = ColorMidiUtils.three_cc_to_color(self.red_control,
                                                     self.green_control,
                                                     self.blue_control)
        else:
            color = ColorMidiUtils.one_cc_to_color(self.color_control)
            # allow animation to be set at white at the top of a controller
            if self.color_control == 127:
                color = bp_colors.White


        brightness_level = MidiTransform.remap_cc_value(self.brightness_control, 0, 256)
        self._color = bp_colors.color_scale(color, brightness_level)
