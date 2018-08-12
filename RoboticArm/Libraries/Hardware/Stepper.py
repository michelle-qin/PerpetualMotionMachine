import Slush
from Slush.Devices import L6470Registers as LReg
b = Slush.sBoard()


class Stepper(Slush.Motor):
    
    #Stepper constructor, if no parameter is specified they will default to given values
    def __init__(self, **kwargs):
        super().__init__(kwargs.get("port", 0))
        self.resetDev()
        self.microSteps = kwargs.get("microSteps", 64)
        self.setMicroSteps(self.microSteps)
        self.setCurrent(kwargs.get("runCurrent", 20), kwargs.get("accelCurrent", 20), kwargs.get("deaccelCurrent", 20), kwargs.get("holdCurrent", 20))
        self.stepsPerUnit = kwargs.get("stepsPerUnit", 200 / 25.4)
        self.speed = kwargs.get("speed", 1)
        self.setSpeed(self.speed)
        self.getParam(LReg.CONFIG) == 0x2e88 # Allow for GPIO on the slushengine

    def getMicroSteps(self):
        return self.microSteps

    def setMicroSteps(self, microSteps):
        self.microSteps = microSteps

    def setSpeed(self, speed):
        self.speed = speed * self.stepsPerUnit
        self.setMaxSpeed(self.speed)
  
    def home(self, direction):
        self.run(direction, self.speed)
        
        while self.readSwitch() == False:
            continue
            
        self.hardStop()
        self.setAsHome()

    def readSwitch(self):
        if self.getStatus() & 0x4: return 1
        else: return 0
    
    #relative move that blocks movement
    def relativeMove(self, distance):
        numberOfSteps = distance * self.microSteps * self.stepsPerUnit
        self.move(int(numberOfSteps))
        self.waitMoveFinish()
    
    #start relative move that does not block movements
    def startRelativeMove(self, distance):
        numberOfSteps = distance * self.microSteps * self.stepsPerUnit
        self.move(int(numberOfSteps))
    
    #goes to position while blocking other movements
    def goToPosition(self, distance):
        numberOfSteps = distance * self.microSteps * self.stepsPerUnit
        self.goTo(int(numberOfSteps))
        self.waitMoveFinish()
    
    #goes to position with no blocking
    def startGoToPosition(self, distance):
        numberOfSteps = distance * self.microSteps * self.stepsPerUnit
        self.goTo(int(numberOfSteps))
        
    def stop(self):
        self.hardStop()
