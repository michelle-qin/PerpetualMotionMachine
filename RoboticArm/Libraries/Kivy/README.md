# Kivy UI Libraries for the DPEA

These are the libraries to be used for all Mechatronics projects that require the use of Python with Kivy. Please refer to this doc as well as the comments in the code files themselves for help on how to use these libraries/Kivy in general

Before using these libraries, make sure you have these imports in your python file:
```
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.animation import Animation
from functools import partial
```

## DPEAButton

A button that's a colored, rounded rectangle with a drop shadow. Text has a bolded white body and a black outline.

### Required Setup

Build the ```DPEAButton.kv``` into your main python file (the one you run to launch the UI) by using ```Builder.load_file('DPEAButton.kv')```
(This line is already included in the RaspberryPiCommon/PiKivyProjects/NewProject template)

In your kivy file, add these four required lines of code to declare a ```DPEAButton```:
```
DPEAButton:
    background_color: 0, 0, 0, 0
    background_normal: ''
    size_hint: None, None
```

These three lines allow you to specify the button's ```size``` explicitly and makes the background for the button transparent.

### Appearance Customization

You can specify the ```text```, ```color```, ```size```, ```center_x```, and ```center_y```. Here's an example of what your kivy code should look like now:
```
DPEAButton:
    background_color: 0, 0, 0, 0
    background_normal: ''
    size_hint: None, None
    text: 'Hello World!'
    size: 40, 40
    center_x: root.width * 0.97
    center_y: root.height * 0.955
    color: 1, 0, 0, 1
```

The parameters for ```color``` are red, green, blue, alpha (think of alpha as opacity), so in this case, a bright red.

### Touch Event Handling

For the DPEAButton, in order to add the color change animations and handle touches, you need to specify ```id```, ```on_press```, ```on_touch_up```, and ```on_release```. The ```id``` is especially important as it can be used later to change any characteristic of the button. Here's an example of what your kivy code should look like now:
```
DPEAButton:
    background_color: 0, 0, 0, 0
    background_normal: ''
    size_hint: None, None
    text: 'Hello World!'
    size: 40, 40
    center_x: root.width * 0.97
    center_y: root.height * 0.955
    color: 1, 0, 0, 1
    id: ExampleButton
    on_press: root.ExampleButtonDown()
    on_touch_up: root.resetColors()
    on_release: root.exampleAction()
```

The ```on_press``` method is used to change the button to a darker color It should be in your main python file and look something like this:
```
def ExampleButtonDown(self):
    self.ids.ExampleButton.color = 0.5, 0, 0, 1
```

Notice how the ```id``` that we set earlier is used now to access our button and change the ```color``` characteristic to a darker red.

The ```on_touch_up``` method is used to reset all buttons to their original colors. The reason the color resets are bound to ```on_touch_up``` and not ```on_release``` is so that the colors will reset even if the user's finger lifts after leaving the button. This also separates the color reset from the actual action that the button performs, increasing code readability. It should also be in the main python file and look something like this:
```
def resetColors(self):
    self.ids.ExampleButton.color = 1, 0, 0, 1
    # add color resets for all the buttons in your UI here
    # so that you can call the same method for every on_touch_up action
```

Finally, the ```on_release``` method is used for what you actually want the button to do and should call predefined hardware functions that you have written.

## Image Button

An Image with button-like behavior since kivy unfortunately does not have a default ```ImageButton``` class.

### Required Setup

At the top of your file with your import statements, add ```import ImageButton```. To use the ```ImageButton```, simply initialize it in your kivy file like so:
```
ImageButton:
    # your parameters
    # will go here
```

### Appearance Customization

You can specify the ```source``` (which is a string containing the location of the image that you want the button to be), ```size```, ```center_x```, and ```center_y```. Here's an example of what your kivy code should look like now:
```
ImageButton:
    source: 'HelloWorld.png'
    size: 50, 150
    center_x: root.width * 0.75
    center_y: root.height * 0.25
```

### Touch Event Handling

Binding an ```on_release``` method to the ```ImageButton``` should be enough, but feel free to use ```on_press``` and ```on_touch_up``` as well. Also note that ```id``` can also be used to change you button's characteristics.

## Pause Scene

A pause scene to disable the UI whilst hardware processes are in progress.

### Required Setup

Build the ```PauseScene.kv``` into your main python file (the one you run to launch the UI) by using ```Builder.load_file('PauseScene.kv')```

Create the ```PasueScene``` class in the main python file like so:
```
class PauseScene(Screen):
    pass
```

Add the pause scene screen to the screen manager after you add your main scenes:
```
sm.add_widget(MainScreen(name = 'examples'))
# your other screens here
sm.add_widget(PauseScene(name = 'pauseScene'))
```

Copy and paste these two required methods into your main python file:
```
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
```

### Usage

To use the pause scene, simply call the pause method like so:
```
pause('Scene Paused', 5, 'examples')
```

The parameters in order are: ```text``` which is the text you wish the pause scene to display, ```sec``` which is the time you want the pause to be in seconds, and ```originalScene``` which is the string name you assigned to the scene you wish to switch back to.

## Admin Screen

An admin screen that requires a password to be entered to continue

### Required Setup

At the top of your file with your import statements, add ```import AdminScreen```.

Add the admin screen to the screen manager after you add your main scenes:
```
sm.add_widget(MainScreen(name = 'examples'))
# your other screens here
sm.add_widget(AdminScreen.AdminScreen(name = 'admin'))
```

Set the action that the admin screen will execute if the password is entered correctly by editing the ```AdminScreen.py``` file. Find the ```checkPass``` method that should look like the following:
```
def checkPass(self):
      global password
      global userPW
      if (password == userPW):
          print('correct')
          self.ids.pw.text = ' '
          userPW = ''
          self.parent.current = 'examples'
```

On the line that says ```self.parent.current = 'examples'```, modify it to run the action that you want it to

You also need to set the scene that the "Back to Game" button will transition to by editing the ```AdminScreen.kv``` file. Below is the code for the very first button in the file that you will be editing:
```
DPEAButton:
      background_color: 0, 0, 0, 0
      background_normal: ''
      size_hint: None, None
      text: 'Back to Game'
      id: back
      center_x: root.center_x
      center_y: root.center_y + 260
      color: 0.019, 0.337, 1, 1
      size: 280, 80
      on_press: root.backButtonDown()
      on_release: root.manager.current = 'examples'
      on_touch_up: root.resetColors()
```

On the line that says ```on_release: root.manager.current = 'examples'``` change ```'examples'``` to the name of the scene that you want the back button to go back to

### Password

The default password is ```2018```. To change this password, open the ```AdminScreen.py``` file and edit the line that says ```password = '2018'``` near the top of the file.

Passwords can be any length but must only contain numbers.
