# ////////////////////////////////////////////////////////////////
# //                     IMPORT STATEMENTS                      //
# ////////////////////////////////////////////////////////////////

import math
import sys
#import spidev

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
sys.path.insert(0, "Libraries/Hardware")
import Stepper 
sys.path.insert(0, "Libraries/Hardware/RPiMIB")
import RPiMIB

#ramp.initGPIOState()
#def initialize():
#    toggleArm(UP)
#    toggleMagnet(OFF)
#    toggleRamp(TO_HOME)

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
Builder.load_file('Libraries/Kivy/DPEAButton.kv')
Builder.load_file('Libraries/Kivy/PauseScene.kv')
Window.clearcolor = (.1, .1,.1, 1) # (WHITE)
Window.size = (1500, 800)

RPiMIB.openSPI()

# ////////////////////////////////////////////////////////////////
# //                    SLUSH/HARDWARE SETUP                    //
# ////////////////////////////////////////////////////////////////

arm = Stepper.Stepper(speed = 100)

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

freq_clock = 16000000
spiFrequency = 1000000
lowerTowerPosition = 30
upperTowerPosition = 40


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
            print('raise arm')
            #arm.setIOState(0, 1, 1)
        else:
            self.ids.armControl.text = "Lower Arm"
            print('lower arm')
            #arm.setIOState(0, 1, 0)
        self.isArmUp = isArmUp
        
    def toggleMagnet(self):
        self.ids.magnetControl.color = 0.701, 0.560, 0.078, 1
        self.isMagnetOn = not self.isMagnetOn
        self.magnetControl(self.isMagnetOn)
        
    def magnetControl(self, isMagnetOn):
        RPiMIB.reset();
        if (isMagnetOn == ON):
            self.ids.magnetControl.text = "Hold Ball"
            print('magnet on')
           # RPiMIB.sendI2C(0x41, self.staircaseSpeed)
        else:
            self.ids.magnetControl.text = "Release Ball"
            print('magnet off')
           # RPiMIB.sendI2C(0x41, 0)
        self.isMagnetOn = isMagnetOn
    
    def auto(self):
        self.ids.auto.color = 0.180, 0.188, 0.980, 1
        self.ids.auto.text = "Stop"
##        if (self.isBallAtBottomOfRamp()):
##            self.turnOnStaircase(OFF)
##            self.openGate(CLOSE)
##            self.homeRamp(TOP)
##            
##        self.turnOnStaircase(ON)
##        sleep(1)
##        self.openGate(OPEN)
        
    def setArmPosition(self, position):
        self.armPosition = position
        self.ids.armControlLabel.text = "Arm Position " + str(math.trunc(self.armPosition))
        arm.goToPosition(self.armPosition)

    def homeArm(self):
        arm.home(0)
        
    def isBallOnTallTower(self):
        return arm.getIOState(1, 1)

    def isBallOnShortTower(self):
        return arm.getIOState(0, 1)
        
    def resetColors(self):
        self.ids.armControl.color = YELLOW
        self.ids.magnetControl.color = YELLOW
        self.ids.auto.color = BLUE

    def quit(self):
        quitAll()
    # more functions here

    
def signal_handler(signal, frame):
    print ('Goodbye')
    quit()
    sys.exit(0)

sm.add_widget(MainScreen(name = 'main'))


# ////////////////////////////////////////////////////////////////
# //                          RUN APP                           //
# ////////////////////////////////////////////////////////////////

reset()

MyApp().run()
RPiMIB.closeSPI()
