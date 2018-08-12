#   Written by Francis Pan as part of the standard kivy libraries for the DPEA
#   28 February 2018

from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.graphics import *

#   An Image that has button capabilities.
#   When using, specify:
#       id, source, size, position, on_press, and on_release

class ImageButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        self.size_hint = None, None
        self.keep_ratio = False
        self.allow_stretch = True
        self.size = 150, 150
        self.background_color = 0, 0, 0, 0
        self.background_normal = ''
        self.source = 'DPEA Logo Transparent.png'
