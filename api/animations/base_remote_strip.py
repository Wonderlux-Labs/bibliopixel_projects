from bibliopixel.animation import BaseStripAnim

class BaseRemoteStrip(BaseStripAnim):
    def __init__(self, layout, start=0, end=-1, **args):
        super(BaseRemoteStrip, self).__init__(layout, start, end)
        self._color_control = 0
        self._brightness_control = 100
