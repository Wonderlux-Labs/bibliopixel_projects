from bibliopixel.animation import BaseStripAnim
from bibliopixel import colors
import random
import time

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
        c = colors.conversions.HUE_RAINBOW[int(c_num)]
        return c

class FireFliesMidi(BaseStripAnim):
    def __init__(self, layout, **args):
        super(FireFliesMidi, self).__init__(layout, 0, -1)
        self._color_control = args.get('color_control') or 100
        self._width_control = args.get('width_control') or 0
        self._count_control = args.get('count_control') or 0
        self._level_control = args.get('level_control') or 100
        self._delay_control = args.get('delay_control') or 0
        self._max_width = args.get('max_width') or 10
        self._max_count = args.get('max_count') or 10
        self._use_rgb = args.get('use_rgb') or False
        self._red_control = args.get('red_control') or 50
        self._green_control = args.get('green_control') or 50
        self._blue_control = args.get('blue_control') or 50

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        amt = 1
        if self._step > self.layout.numLEDs:
            self._step = 0

        self.layout.all_off()

        scaled_count = int(MidiTransform.remap_cc_value(self._count_control, 1, self._max_count))
        scaled_width = int(MidiTransform.remap_cc_value(self._width_control, 1, self._max_width))

        for i in range(scaled_count):
            pixel = random.randint(0, self.layout.numLEDs - 1)

            if self._use_rgb:
                c = ColorMidiUtils.three_cc_to_color(self._red_control, self._green_control, self._blue_control)
            else:
                c = ColorMidiUtils.one_cc_to_color(self._color_control)

            c_lev = MidiTransform.remap_cc_value(self._level_control, 0, 256)
            c = colors.color_scale(c, c_lev)

            for i in range(scaled_width):
                if pixel + i < self.layout.numLEDs:
                    self.layout.set(pixel + i, c)

        self._step += amt

        delay_time = MidiTransform.remap_cc_value(self._delay_control, 0, 1)
        time.sleep(delay_time)
