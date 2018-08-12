# dpeaMixPanel

# Python module to send analytic Events/Properties to MixPanel

# Example

from dpea.utilities import MixPanel

INFINITY_MIRROR_TOKEN = "yourMixPanelProjectToken"

#
# Sends a "Color Selected" event with a color property of 'blue'
#
colorEvent = MixPanel("Infinity Mirror", INFINITY_MIRROR_TOKEN)

colorEvent.setEventName("Color Selected");

colorEvent.addProperty("color", "blue");

colorEvent.sendEvent()

#
# Sends a "Idle" event with a 'duration' property of 232 seconds
#
demoEvent = MixPanel("Infinity Mirror", INFINITY_MIRROR_TOKEN)

demoEvent.setEventName("Idle");

# You can have up to 256 properties
demoEvent.addProperty("Duration", 232);
demoEvent.addProperty("Range (in minutes)", "1-5");

demoEvent.sendEvent()

