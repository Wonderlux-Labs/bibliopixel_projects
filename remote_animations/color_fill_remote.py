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

class ColorFillRemote(BaseRemoteStrip):
    """Fill the dots progressively along the strip."""

    def __init__(self, layout, **args):
        print(args)
        super(ColorFillRemote, self).__init__(layout, **args)

    def step(self, amt=1):

        self.get_color()
        self.layout.fill(self._color)
        delay_time = MidiTransform.remap_cc_value(self.delay_control, 0, 1)
        time.sleep(delay_time)
