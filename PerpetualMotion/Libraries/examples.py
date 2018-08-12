"""
Written by Francis Pan as part of the standard kivy libraries for the DPEA
28 February 2018
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *

import ImageButton

sm = ScreenManager()

class MyApp(App):
    def build(self):
        return sm

Builder.load_file('examples.kv')
Builder.load_file('DPEAButton.kv')
Window.clearcolor = (0.95, 0.95, 0.95, 1)

def quitAll():
    quit()

class MainScreen(Screen):
    def exitProgram(self):
        quitAll()

sm.add_widget(MainScreen(name = 'examples'))

MyApp().run()
