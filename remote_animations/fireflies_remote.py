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

class FireFliesRemote(BaseRemoteStrip):
    def __init__(self, layout, start=0, end=-1, **args):
        super(FireFliesRemote, self).__init__(layout, start, end, **args)
        self.max_count = self.layout.numLEDs
        self.max_width = self.layout.numLEDs

    def pre_run(self):
        self._step = 0

    def step(self, amt=1):
        amt = 1
        if self._step > self.layout.numLEDs:
            self._step = 0

        self.layout.all_off()
        self.get_color()

        scaled_count = int(MidiTransform.remap_cc_value(self.count_control, 1, self.max_count))
        scaled_width = int(MidiTransform.remap_cc_value(self.width_control, 1, self.max_width))

        for i in range(scaled_count):
            pixel = random.randint(0, self.layout.numLEDs - 1)

            for i in range(scaled_width):
                if pixel + i < self.layout.numLEDs:
                    self.layout.set(pixel + i, self._color)

        self._step += amt

        delay_time = MidiTransform.remap_cc_value(self.delay_control, 0, 1)
        time.sleep(delay_time)
