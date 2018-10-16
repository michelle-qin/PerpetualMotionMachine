# Michelle Qin

# ////////////////////////////////////////////////////////////////
# //                     IMPORT STATEMENTS                      //
# ////////////////////////////////////////////////////////////////

import math
import sys
#sys.path.insert(1, "/home/pi/kivy")
#import kivy
#kivy.require("1.8.0")

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
from time import sleep
import RPi.GPIO as GPIO
sys.path.insert(0, "/home/pi/Documents/RaspberryPiCommon/Libraries/Hardware")
import Stepper 
sys.path.insert(0, "/home/pi/Documents/RaspberryPiCommon/Libraries/Hardware/RPiMIB")
import RPiMIB
import threading

#imports for sensor
import Slush
RPiMIB.openSPI()
SlushEngine = Slush.sBoard()

#Intialization
ON = False
OFF = True
HOME = True
TOP = False
OPEN = False
CLOSE = True
YELLOW = .180, 0.188, 0.980, 1
BLUE = 0.917, 0.796, 0.380, 1

#730 is the default length, but sometimes it only goes up 1/4 of the way up the ramp. In those cases, use 2950. If you
#notice the ramp is crashing into the other end, switch to 730.
rampLength = 2950 #730
ramp = Stepper.Stepper(port = 0, speed = 100)
ramp.home(0)


# ////////////////////////////////////////////////////////////////
# //            DECLARE APP CLASS AND SCREENMANAGER             //
# //                     LOAD KIVY FILE                         //
# ////////////////////////////////////////////////////////////////
#Config.set('graphics', 'width', '500')
#Config.set('graphics', 'height', '1000')
sm = ScreenManager()

class MyApp(App):
    def build(self):
        self.title = "Perpetual Motion"
        return sm

Builder.load_file('main.kv')
Builder.load_file('/home/pi/Documents/RaspberryPiCommon/Libraries/Kivy/DPEAButton.kv')
Builder.load_file('/home/pi/Documents/RaspberryPiCommon/Libraries/Kivy/PauseScene.kv')
Window.clearcolor = (.1, .1,.1, 1) # (WHITE)
#Window.size = (1500, 800)

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


# "reliableSetPWM" accounts for discrepancies with inconsistent hardware - sometimes, the 1st signal doesn't get passed,
# so this ensures that it gets passed if the 1st signal doesn't go through. Even if the 1st signal gets passed,
# this will still work b/c the 2nd signal will quickly override it.
def reliableSetPWM(port, PWM):
    RPiMIB.sendPWM(port, PWM)
    sleep(0.05) 
    RPiMIB.sendPWM(port, PWM)

class MainScreen(Screen):
    staircaseSpeedText = '0'
    rampSpeed = 100
    staircaseSpeed = 40
    isGateOpen = False
    isStaircaseOn = False
    isRampHome = HOME
    submitRamp = False  
    notRampSubmissionComplete = False
    # numberOfCycles keeps track of how many cycles have passed (for "Start" process). Default # cycles = 0
    numberOfCycles = 0
    counter = 0

    #    self.ids.rampSpeedSlider.value = rampSpeed
    
# "update" -------
    def update(self, timeElapsed):
        #pull ramp state
        print('update')
        if self.notRampSubmissionComplete:
            # readSwitch returns true if the ramp is home
            if (self.isRampHome == HOME) and ramp.readSwitch():
                ramp.hardStop()
                ramp.setAsHome()
                self.notRampSubmissionComplete = False
            # in Motor.py a relativeMove is done if the second bit of
            # getStatus is set
            elif (self.isRampHome == TOP) and \
                    (ramp.getStatus() & 0x2) != 0:
                self.notRampSubmissionComplete = False     

# isGateOpen is the value for whether the gate is open or closed
# When you press the "Open/Close Gate" button, it will call "toggleGate" (if you want to confirm, check main.kv).
# "toggleGate" switches the value of isGateOpen and then calls "resubmitState" (check the explanation for that method
# where it's defined). When you press the button, you want to change its current state (i.e. if the gate is currently
# closed, you want it to be opened when you press the button & vice versa).
# That's what switching the value of isGateOpen is for.
    def toggleGate(self):
        self.ids.gate.color = 0.701, 0.560, 0.078, 1
        print("[debug]", self.isGateOpen)
        self.isGateOpen = not self.isGateOpen
        #self.openGate(not self.isGateOpen)
        #sleep(0.2)
        #self.openGate(not self.isGateOpen)
        #sleep(0.2)
        #self.openGate(not self.isGateOpen)
        self.resubmitState()

# "openGate" is the function that actually opens/closes the gate.
    def openGate(self, isOpen):
        # if you want the gate to be closed, it will change the button to say "Open Gate"  (for next round)
        # and send 500 PWM to port 4
        # Note: 500 PWM is the amount to close the gate
        if (isOpen == False):
            self.ids.gate.text = "Open Gate"
            reliableSetPWM(4, 500)
            #RPiMIB.sendPWM(4, 500)
            print('close gate')
        # if you want the gate to beopened, it will change the button to say "Close Gate"  (for next round)
        # and send 4000 PWM to port 4
        # Note: 4000 PWM is the amount to open the gate
        else:
            self.ids.gate.text = "Close Gate"
            print('open gate')
            reliableSetPWM(4, 4000)
        self.isGateOpen = isOpen

# isStaircaseOn is the value for whether the staircase is on or off
# When you press the "Staircase On/Off" button, it will call "toggleStaircase" (if you want to confirm, check main.kv).
# "toggleStaircase" switches the value of isStaircaseOn and then calls "resubmitState" (check the explanation for
# that method where it's defined). When you press the button, you want to change its current state (i.e. if  the
# staircase is currently off, you want it to be on when you press the button & vice versa).
# That's what switching the value of isStaircaseOn is for.
    def toggleStaircase(self):
        self.ids.staircase.color = 0.701, 0.560, 0.078, 1
        self.isStaircaseOn = not self.isStaircaseOn 
        #self.turnOnStaircase(not self.isStaircaseOn)
        #self.turnOnStaircase(not self.isStaircaseOn)
        #self.turnOnStaircase(not self.isStaircaseOn)
        self.resubmitState()

# "turnOnStaircase" is the function that actually turns on/off the staircase.
    def turnOnStaircase(self, isOn):
        # if you want the staircase to be opened, it will change the button to say "Staircase Off"  (for next round)
        # and send int(self.staircaseSpeed) * 125 PWM to port 5
        # Note: int(self.staircaseSpeed) * 125 PWM is the default amount to turn on the staircase
        if (isOn):
            self.ids.staircase.text = "Staircase Off" 
            print('staircase on')
            #RPiMIB.sendPWM(5, 0)
            reliableSetPWM(5, int(self.staircaseSpeed) * 125)
        # if you want the staircase to be closed, it will change the button to say "Staircase On"  (for next round)
        # and send 0 PWM to port 5
        # Note: 0 PWM is the amount to turn off the staircase
        else: 
            self.ids.staircase.text = "Staircase On" 
            print('staircase off')
            #RPiMIB.sendPWM(5, int(self.staircaseSpeed) * 125)
            #RPiMIB.sendPWM(5, 1)
            #sleep(0.2)
            reliableSetPWM(5, 0)
        self.isStaircaseOn = isOn

# isRampHome is the value for whether the ramp is home or not
# When you press the "Ramp Home/Top" button, it will call "toggleRamp" (if you want to confirm, check main.kv).
# "toggleRamp" switches the value of isRampHome and then calls "resubmitState" (check the explanation for
# that method where it's defined). When you press the button, you want to change its current state (i.e. if  the
# ramp is currently home, you want it to go to the top when you press the button & vice versa).
# That's what switching the value of isRampHome is for.
    def toggleRamp(self):
        self.ids.ramp.color = 0.701, 0.560, 0.078, 1
        self.isRampHome = not self.isRampHome
        #self.homeRamp(not self.isRampHome)
        self.submitRamp = True
        self.resubmitState()

# "homeRamp" is the function that actually brings the ramp home or top.
    def homeRamp(self, isHome):
        # if you want the ramp to go home, it will change the button to say "Ramp To Top"  (for next round)
        # and --------- (not sure what ramp.run does??
        # Note:
        if (isHome == HOME):
            self.ids.ramp.text = "Ramp To Top"
            print('ramp home') 
            ramp.run(0, ramp.speed)
        # if you want the ramp to go to the top, it will change the button to say "Ramp Home"  (for next round)
        # and tell the ramp to move to the top along the rampLength (defined near the top of this file).
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
#            ramp.relativeMove(rampLength)
            ramp.relativeMove(rampLength)           
            print('ramp done');              
        self.isRampHome = isHome
        #self.turnOnStaircase(self.isStaircaseOn)
        
    def isBallAtBottomOfRamp(self):
        return ramp.getIOState(1, 1)
    
#    def start(self):
#        while(self.numberOfCycles < 5):
#            if (SlushEngine.getIOState(0, 0) == False):
#                self.auto()
#            self.numberOfCycles = self.numberOfCycles + 1
#        self.ids.auto.text = "Start"

# When you press the "Start" button, it will call "auto" (if you want to confirm, check main.kv)
# The Start process essentially combines all the separate components (ramp, staircase, gate) to get the ball across
# the sculpture & fulfill its name of the "Perpetual Motion Machine"
# Description: First, the ramp will bring the ball to the top and to the staircase; staircase will turn on to
# bring ball to gate; gate will open to let ball through and back to the ramp. The sensor at the home of the ramp
# detects the ball and starts the entire process again
    def auto(self):
        # changes "Start" button to say "Stop" when it's running
        self.ids.auto.text = "Stop"
        self.ids.auto.color = 0.180, 0.188, 0.980, 1

        # initializes each component (check explanation of this function where it's defined)
        self.initialize()
        sleep(1)
            #if (SlushEngine.getIOState(j, i) == 
            #if (self.isBallAtBottomOfRamp()):

        # First, the ramp brings the ball to the top
        self.homeRamp(TOP)

        # After bringing the ball to the top, the ramp will return home
        self.homeRamp(HOME)

        self.turnOnStaircase(False)
            
        sleep(1)

        # While ramp is going back home, the staircase turns on to bring ball to gate
        self.turnOnStaircase(True)
        sleep(5)
        #gate opens to let the ball through
        self.openGate(True)
        sleep(1)
        self.openGate(CLOSE)
        self.turnOnStaircase(False)
        self.openGate(False)
            #self.ids.auto.text = "Start"
        sleep(2)

        # the sensor: 1st parameter represents Board (A); 2nd parameter represents port (0)
        # When SlushEngine(Board, port) = False, that means there's an object (ball) in front of it
        if (SlushEngine.getIOState(0, 0) == False):
            # after the ball comes to the sensor/home of ramp, a cycle will pass (increment by 1)
            self.numberOfCycles = self.numberOfCycles + 1
            # NOTE: 3 is the number of cycles to run "perpetually". This can be changed in the code. I'm  trying
            # to add a slider on the user interface so the user can decide how many cycles to run. But, when I tried to
            # do that, I got many errors (something to do with kivy I think). Will work on this later.
            if(self.numberOfCycles < 3):
                #If 3 cycles haven't passed, it will start the process again by calling auto()
                self.auto()
            # once 3 cycles have passed and the process is done, will change the button back to "Start"
            self.ids.auto.text = "Start"

    # main.kv calls "setRampSpeed" when changes are made on the slider for the ramp speed
    # When slider is changed to a new value, "setRampSpeed" will set the ramp speed to that new value
    def setRampSpeed(self, speed):
        self.rampSpeed = speed
        self.ids.rampSpeedLabel.text = "Ramp Speed: " + str(math.trunc(self.rampSpeed))
        print("Setting ramp speed: " + str(speed))
        ramp.setSpeed(self.rampSpeed)

    # main.kv calls "setStaircaseSpeed" when changes are made on the slider for the staircase speed
    # When slider is changed to a new value, "setStaircaseSpeed" will set the staircase speed to that new value
    def setStaircaseSpeed(self, speed):
        self.staircaseSpeed = speed
        self.ids.staircaseSpeedLabel.text = "Staircase Speed: " + str(math.trunc(self.staircaseSpeed))
        print("Setting staircase speed: " + str(speed))

#    def setNumberOfCycles(self, number):
#        self.numberOfCycles = number
#        self.ids.numberOfCyclesLabel.text = "Number of Cycles: " + str(math.trunc(self.numberOfCycles))
#        print("Setting number of cycles: " + str(number))
        
    def isBallAtBottomOfRamp(self):
        return ramp.getIOState(1, 4)

    def isBallAtTopOfRamp(self):
        return ramp.getIOState(1, 5)

    def resetColors(self):
        self.ids.gate.color = YELLOW
        self.ids.staircase.color = YELLOW
        self.ids.ramp.color = YELLOW
        self.ids.auto.color = BLUE

    # Will initialize all components - i.e. gate will close, ramp will go home, staircase will turn off (assuming these
    # components are not yet initialized; otherwise, nothing will happen.
    def initialize(self):
        self.isGateOpen = False
        self.isRampHome = HOME
        self.isStaircaseOn = False
        # The following 3 lines of code were implemented after the ramp was not cooperating
        self.submitRamp = False  
        self.notRampSubmissionComplete = False
        self.resubmitState()
        
    def exitProgram(self):
        quitAll()

    # This "init" was overridden so that right when the program runs, all the components will initialize
    def __init__(self, **kwargs):
        super(Screen,self).__init__(**kwargs)
        self.initialize()
        print("Stopyjkhhkh")
        
    def resubmitState(self):
        if self.submitRamp:
            self.homeRamp(self.isRampHome)
            self.submitRamp = False
        self.turnOnStaircase(self.isStaircaseOn)
        self.openGate(self.isGateOpen)

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

screen = MainScreen(name = 'main')

#implemented..
Clock.schedule_interval(screen.update, 1.0/30.0)

sm.add_widget(screen)
sm.add_widget(PauseScene(name = 'pauseScene'))

# ////////////////////////////////////////////////////////////////
# //                          RUN APP                           //
# ////////////////////////////////////////////////////////////////

MyApp().run()
RPiMIB.closeSPI()
