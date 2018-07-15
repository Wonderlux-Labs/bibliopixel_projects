import random
import time
import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from base_remote_strip import BaseRemoteStrip
from base_remote_strip import MidiTransform
from base_remote_strip import NumberUtils
from base_remote_strip import ColorMidiUtils
from bibliopixel import colors as bp_colors

# Base class to be used by any display type

class TwinkleRemote(BaseRemoteStrip):
    def __init__(self, layout,
                 density=50, speed=10, max_bright=255, start=0, end=-1):
        super(TwinkleRemote, self).__init__(layout, start, end)
        self.colors = [(255,240,255), (245, 230, 233), (250,230,230)]
        self.density = density
        self.speed = speed
        self.max_bright = max_bright

        # Make sure speed, density & max_bright are in sane ranges
        self.speed = min(self.speed, 100)
        self.speed = max(self.speed, 2)
        self.density = min(self.density, 100)
        self.density = max(self.density, 2)
        self.max_bright = min(self.max_bright, 255)
        self.max_bright = max(self.max_bright, 5)
        self.internal_delay = 0

    def pre_run(self):
        self._step = 0
        # direction, color, level
        self.pixels = [(0, bp_colors.Off, 0)] * self.layout.numLEDs

    def change_color(self, color):
        x = (color[0] + random.randint(0,100)) % 255
        y = (color[1] + random.randint(0,100))% 255
        z = (color[2] + random.randint(0,100)) % 255
        return (x,y,z)

    def pick_led(self, speed):
        idx = random.randrange(0, self.layout.numLEDs)
        p_dir, p_color, p_level = self.pixels[idx]
        self.colors = list(map(lambda color: self.change_color(color), self.colors))
        print(self.colors)
        if random.randrange(0, 100) < self.density:
            if p_dir == 0:  # 0 is off
                p_level += speed
                p_dir = 1  # 1 is growing
                p_color = random.choice(self.colors)
                self.layout._set_base(idx, bp_colors.color_scale(p_color, p_level))

                self.pixels[idx] = p_dir, p_color, p_level

    def step(self, amt=1):
        self.layout.all_off()
        self.pick_led(self.speed)

        for i, val in enumerate(self.pixels):
            p_dir, p_color, p_level = val
            if p_dir == 1:
                p_level += self.speed
                if p_level > 255:
                    p_level = 255
                    p_dir = 2  # start dimming
                self.layout._set_base(i, bp_colors.color_scale(p_color, p_level))
            elif p_dir == 2:
                p_level -= self.speed
                if p_level < 0:
                    p_level = 0
                    p_dir = 0  # turn off
                self.layout._set_base(i, bp_colors.color_scale(p_color, p_level))

            self.pixels[i] = (p_dir, p_color, p_level)

        self._step += amt
