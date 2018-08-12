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

RPiMIB.openSPI()

#Intialization
ON = False
OFF = True
HOME = True
TOP = False
OPEN = False
CLOSE = True
YELLOW = .180, 0.188, 0.980, 1
BLUE = 0.917, 0.796, 0.380, 1

freq_clock = 16000000
spiFrequency = 16000000

rampLength = 730
ramp = Stepper.Stepper(port = 0, speed = 100)
#ramp.initGPIOState()


# ////////////////////////////////////////////////////////////////
# //            DECLARE APP CLASS AND SCREENMANAGER             //
# //                     LOAD KIVY FILE                         //
# ////////////////////////////////////////////////////////////////
#Config.set('graphics', 'width', '500')
#Config.set('graphics', 'height', '1000')
sm = ScreenManager()

#initialize()

class MyApp(App):
    def build(self):
        self.title = "Perpetual Motion"
        return sm

Builder.load_file('main.kv')
Builder.load_file('Libraries/Kivy/DPEAButton.kv')
Builder.load_file('Libraries/Kivy/PauseScene.kv')
Window.clearcolor = (.1, .1,.1, 1) # (WHITE)
Window.size = (1500, 800)

# ////////////////////////////////////////////////////////////////
# //                    SLUSH/HARDWARE SETUP                    //
# ////////////////////////////////////////////////////////////////


# ////////////////////////////////////////////////////////////////
# //                      GLOBAL VARIABLES                      //
# //                         CONSTANTS                          //
# ////////////////////////////////////////////////////////////////




# ////////////////////////////////////////////////////////////////
# //                       MAIN FUNCTIONS                       //
# //             SHOULD INTERACT DIRECTLY WITH HARDWARE         //
# ////////////////////////////////////////////////////////////////
	
def quitAll():
    # free stepper motors, etc. before quit()
    quit() # quits program

# ////////////////////////////////////////////////////////////////
# //        DEFINE MAINSCREEN CLASS THAT KIVY RECOGNIZES        //
# //                                                            //
# //   KIVY UI CAN INTERACT DIRECTLY W/ THE FUNCTIONS DEFINED   //
# //     CORRESPONDS TO BUTTON/SLIDER/WIDGET "on_release"       //
# //                                                            //
# //   SHOULD REFERENCE MAIN FUNCTIONS WITHIN THESE FUNCTIONS   //
# //      SHOULD NOT INTERACT DIRECTLY WITH THE HARDWARE        //
# ////////////////////////////////////////////////////////////////


class MainScreen(Screen):
    staircaseSpeedText = '0'
    rampSpeed = 100
    staircaseSpeed = 40
    isGateOpen = CLOSE
    isStaircaseOn = OFF
    isRampHome = HOME


    #    self.ids.rampSpeedSlider.value = rampSpeed
    
    def toggleGate(self):
        self.ids.gate.color = 0.701, 0.560, 0.078, 1
        self.isGateOpen = not self.isGateOpen
        self.openGate(self.isGateOpen)

    def openGate(self, isOpen):
        if (isOpen == OPEN):
            self.ids.gate.text = "Close Gate"
            print('close gate')
            RPiMIB.sendPWM(4, 2000)
        else:
            self.ids.gate.text = "Open Gate"
            print('open gate')
            RPiMIB.sendPWM(4, 1000)
        self.isGateOpen = isOpen
        
    def toggleStaircase(self):
        self.ids.staircase.color = 0.701, 0.560, 0.078, 1
        self.isStaircaseOn = not self.isStaircaseOn
        self.turnOnStaircase(self.isStaircaseOn)
        
    def turnOnStaircase(self, isOn):
        if (isOn == True):
            print('staircase on')
            RPiMIB.sendPWM(5, 0)
        else: 
            print('staircase off')
            RPiMIB.sendPWM(5, int(self.staircaseSpeed) * 100)
        self.isStaircaseOn = isOn
    
    def toggleRamp(self):
        self.ids.ramp.color = 0.701, 0.560, 0.078, 1
        self.isRampHome = not self.isRampHome
        self.homeRamp(self.isRampHome)
        
    def homeRamp(self, isHome):
        if (isHome == HOME):
            self.ids.ramp.text = "Ramp To Top"
            print('ramp home') 
            ramp.home(1)
        else:
            self.ids.ramp.text = "Ramp Home"
            # If PB0 is high
            print('ramp at top')
#            print(ramp.getIOState(1, 1))
#            print(ramp.getIOState(1, 2))
#            print(ramp.getIOState(1, 3))
#            print(ramp.getIOState(1, 4))
#            print(ramp.getIOState(1, 5))
#            print(ramp.getIOState(1, 6))
#            print(ramp.getIOState(1, 7))
#            print(ramp.getIOState(1, 0))

#            if (ramp.getIOState(1, 0) == 0):
            ramp.relativeMove(-rampLength)
            print('ramp done');
               
        self.isRampHome = isHome
        
    def isBallAtBottomOfRamp(self):
        return ramp.getIOState(1, 1)
    
    def auto(self):
        self.ids.auto.text = "Stop"
        self.ids.auto.color = 0.180, 0.188, 0.980, 1
        
        self.initialize()
        sleep(1)
        #if (self.isBallAtBottomOfRamp()):
        self.homeRamp(TOP)
        sleep(1)
        
        self.turnOnStaircase(ON)
        self.homeRamp(HOME)

        self.turnOnStaircase(OFF)
        sleep(0.5)
        self.openGate(OPEN)
        sleep(1)
        self.openGate(CLOSE)
        self.ids.auto.text = "Start"
        
    def setRampSpeed(self, speed):
        self.rampSpeed = speed
        self.ids.rampSpeedLabel.text = "Ramp Speed: " + str(math.trunc(self.rampSpeed))
        print("Setting ramp speed: " + str(self.rampSpeed))
        ramp.setSpeed(self.rampSpeed)
        
    def setStaircaseSpeed(self, speed):
        self.staircaseSpeed = speed
        self.ids.staircaseSpeedLabel.text = "Staircase Speed: " + str(math.trunc(self.staircaseSpeed))
        print("Setting staircase speed: " + str(speed))
        
    def isBallAtBottomOfRamp(self):
        return ramp.getIOState(1, 1)

    def isBallAtTopOfRamp(self):
        return ramp.getIOState(0, 1)
        
    def resetColors(self):
        self.ids.gate.color = YELLOW
        self.ids.staircase.color = YELLOW
        self.ids.ramp.color = YELLOW
        self.ids.auto.color = BLUE
    
    def initialize(self):
        self.openGate(CLOSE)
        self.turnOnStaircase(OFF)
        self.homeRamp(HOME)

    def exitProgram(self):
        quitAll()

#    def __init__(self, **kwargs):
#        self.initialize();

class PauseScene(Screen):
    pass

def pause(text, sec, originalScene):
    sm.transition.direction = 'left'
    sm.current = 'pauseScene'
    sm.current_screen.ids.pauseText.text = text
    Clock.schedule_once(partial(transitionBack, originalScene), sec)
    load = Animation(size = (150, 10), duration = sec) + Animation(size = (10, 10), duration = 0)
    load.start(sm.current_screen.ids.progressBar)

def transitionBack(originalScene, *largs):
    sm.transition.direction = 'right'
    sm.current = originalScene
    
def signal_handler(signal, frame):
    print ('Goodbye')
    quit()
    sys.exit(0)

sm.add_widget(MainScreen(name = 'main'))
sm.add_widget(PauseScene(name = 'pauseScene'))


# ////////////////////////////////////////////////////////////////
# //                          RUN APP                           //
# ////////////////////////////////////////////////////////////////


MyApp().run()
RPiMIB.closeSPI()
