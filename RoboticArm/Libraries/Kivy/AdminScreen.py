from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *

password = '2018'
userPW = ''

Builder.load_file('DPEAButton.kv')
Builder.load_file('AdminScreen.kv')

class AdminScreen(Screen):

    def addNum(self, num):
        global userPW
        self.ids.pw.text += '* '
        userPW += str(num)

    def removeNum(self):
        global userPW
        self.ids.pw.text = self.ids.pw.text[:len(self.ids.pw.text) - 2]
        userPW = userPW[:len(userPW) - 1]

    def checkPass(self):
        global password
        global userPW
        if (password == userPW):
            print('correct')
            self.ids.pw.text = ' '
            userPW = ''
            self.parent.current = 'examples'

    def resetColors(self):
        self.ids.back.color = 0.019, 0.337, 1, 1
        self.ids.one.color = 0.019, 0.337, 1, 1
        self.ids.two.color = 0.019, 0.337, 1, 1
        self.ids.three.color = 0.019, 0.337, 1, 1
        self.ids.four.color = 0.019, 0.337, 1, 1
        self.ids.five.color = 0.019, 0.337, 1, 1
        self.ids.six.color = 0.019, 0.337, 1, 1
        self.ids.seven.color = 0.019, 0.337, 1, 1
        self.ids.eight.color = 0.019, 0.337, 1, 1
        self.ids.nine.color = 0.019, 0.337, 1, 1
        self.ids.zero.color = 0.019, 0.337, 1, 1
        self.ids.backspace.color = 0.019, 0.337, 1, 1
        self.ids.enter.color = 0.019, 0.337, 1, 1

    def backButtonDown(self):
        self.ids.back.color = 0.01, 0.168, .5, 1

    def oneButtonDown(self):
        self.ids.one.color = 0.01, 0.168, .5, 1

    def twoButtonDown(self):
        self.ids.two.color = 0.01, 0.168, .5, 1

    def threeButtonDown(self):
        self.ids.three.color = 0.01, 0.168, .5, 1

    def fourButtonDown(self):
        self.ids.four.color = 0.01, 0.168, .5, 1

    def fiveButtonDown(self):
        self.ids.five.color = 0.01, 0.168, .5, 1

    def sixButtonDown(self):
        self.ids.six.color = 0.01, 0.168, .5, 1

    def sevenButtonDown(self):
        self.ids.seven.color = 0.01, 0.168, .5, 1

    def eightButtonDown(self):
        self.ids.eight.color = 0.01, 0.168, .5, 1

    def nineButtonDown(self):
        self.ids.nine.color = 0.01, 0.168, .5, 1

    def zeroButtonDown(self):
        self.ids.zero.color = 0.01, 0.168, .5, 1

    def backspaceButtonDown(self):
        self.ids.backspace.color = 0.01, 0.168, .5, 1

    def enterButtonDown(self):
        self.ids.enter.color = 0.01, 0.168, .5, 1
