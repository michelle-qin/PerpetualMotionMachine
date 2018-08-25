# ////////////////////////////////////////////////////////////////
# //                     IMPORT STATEMENTS                      //
# ////////////////////////////////////////////////////////////////

import math
import sys

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.animation import Animation
from functools import partial
from kivy.config import Config
from kivy.core.window import Window
from time import sleep
import RPi.GPIO as GPIO 
sys.path.insert(0, "/home/pi/Libraries/Hardware")
import Stepper 
sys.path.insert(0, "/home/pi/Libraries/Hardware/RPiMIB")
import RPiMIB

# ////////////////////////////////////////////////////////////////
# //            DECLARE APP CLASS AND SCREENMANAGER             //
# //                     LOAD KIVY FILE                         //
# ////////////////////////////////////////////////////////////////
sm = ScreenManager()

class MyApp(App):
    def build(self):
        self.title = "Robotic Arm"
        return sm

Builder.load_file('main.kv')
Builder.load_file('/home/pi/Libraries/Kivy/DPEAButton.kv')
Builder.load_file('/home/pi/Libraries/Kivy/PauseScene.kv')
Window.clearcolor = (.1, .1,.1, 1) # (WHITE)

RPiMIB.openSPI()

# ////////////////////////////////////////////////////////////////
# //                    SLUSH/HARDWARE SETUP                    //
# ////////////////////////////////////////////////////////////////

arm = Stepper.Stepper(port = 0, speed = 100)

# ////////////////////////////////////////////////////////////////
# //                      GLOBAL VARIABLES                      //
# //                         CONSTANTS                          //
# ////////////////////////////////////////////////////////////////
START = True
STOP = False
UP = True
DOWN = False
ON = True
OFF = False
YELLOW = .180, 0.188, 0.980, 1
BLUE = 0.917, 0.796, 0.380, 1

lowerTowerPosition = 14.5
upperTowerPosition = 18.5

# ////////////////////////////////////////////////////////////////
# //                       MAIN FUNCTIONS                       //
# //             SHOULD INTERACT DIRECTLY WITH HARDWARE         //
# ////////////////////////////////////////////////////////////////
	
def quitAll():
    # free stepper motors, etc. before quit()
    quit() # quits program

def reset():
    arm.setMicroSteps(256)
    arm.setSpeed(10);
    arm.relativeMove(2)
    arm.home(0)

class MainScreen(Screen):
    armPosition = 0
    isOn = STOP
    isMagnetOn = OFF
    isArmUp = UP
    
    def toggleArm(self):
        self.ids.armControl.color = 0.701, 0.560, 0.078, 1
        self.isArmUp = not self.isArmUp
        self.armControl(self.isArmUp)

    def armControl(self, isArmUp):
        RPiMIB.reset();
        if (isArmUp == UP):
            self.ids.armControl.text = "Raise Arm"
            arm.setGPIOState(0, 7, 1)
            print('raise arm')
        else:
            self.ids.armControl.text = "Lower Arm"
            arm.setGPIOState(0, 7, 0)
            print('lower arm')
        self.isArmUp = isArmUp
        
    def toggleMagnet(self):
        self.ids.magnetControl.color = 0.701, 0.560, 0.078, 1
        self.isMagnetOn = not self.isMagnetOn
        self.magnetControl(self.isMagnetOn)
        
    def magnetControl(self, isMagnetOn):
        if (isMagnetOn == ON):
            self.ids.magnetControl.text = "Hold Ball"
            print('magnet on')
            RPiMIB.sendPWM(5, 5000)
        else:
            self.ids.magnetControl.text = "Release Ball"
            print('magnet off')
            RPiMIB.sendPWM(5, 0)
        self.isMagnetOn = isMagnetOn
    
    def auto(self):
        self.ids.auto.color = 0.180, 0.188, 0.980, 1
        self.ids.auto.text = "Stop"

        self.armControl(UP)
        self.magnetControl(ON)
        self.homeArm()
                
        if (self.isBallOnTallTower()):
            arm.setArmPosition(upperTowerPosition)
            self.pickUpBall()
            arm.setArmPosition(lowerTowerPosition)
            self.dropBall()

        if (self.isBallOnShortTower()):
            arm.setArmPosition(lowerTowerPosition)
            self.pickUpBall()
            arm.setArmPosition(upperTowerPosition)
            self.dropBall()

        self.homeArm()

    def pickUpBall():
        self.armControl(DOWN)
        sleep(0.25)
        self.magnetControl(ON)
        sleep(0.25)
        self.armControl(UP)

    def dropBall():
        self.armControl(DOWN)
        sleep(0.25)
        self.magnetControl(OFF)
        sleep(0.25)
        self.armControl(UP)
    
    def setArmPosition(self, position):
        self.armPosition = position
        self.ids.armControlLabel.text = "Arm Position " + str(math.trunc(self.armPosition))
        arm.goToPosition(self.armPosition)

    def homeArm(self):
        arm.home(0)
        
    def isBallOnTallTower(self):
        return arm.getGPIOState(1, 1)

    def isBallOnShortTower(self):
        return arm.getGPIOState(1, 2)
        
    def resetColors(self):
        self.ids.armControl.color = YELLOW
        self.ids.magnetControl.color = YELLOW
        self.ids.auto.color = BLUE

    def quit(self):
        quitAll()
    
def signal_handler(signal, frame):
    print ('Goodbye')
    quit()
    sys.exit(0)

sm.add_widget(MainScreen(name = 'main'))


# ////////////////////////////////////////////////////////////////
# //                          RUN APP                           //
# ////////////////////////////////////////////////////////////////

MyApp().run()
RPiMIB.closeSPI()
