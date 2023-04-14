import cadquery as cq
from synthprinter import *

# This is the print you can see at the top of the documentation!

# Start by creating a SynthPrinter object
# You can override any setting from the defaultConfig
# found in synthprinter.py
sp = SynthPrinter(
    panelThickness=4.1,
    miniToggleSwitchDiameter=6.2,
)

# You can only add one panel
sp.addEurorackPanel(8)  # width in HP

# sp.addLed5mm(x, y)
# 0, 0 is at the top left
# functions that start with "add" generally both perform a
# cut on the faceplate, and place a preview object on the
# preview layer. You can call separately the corresponding
# functions that start with "cut" or "preview" instead.
sp.addLed5mm(hp(1), 10)
sp.addLed3mm(hp(1), 30)

# hp() is a little helper that multiplies its argument by
# 5.08, helping you align stuff to a grid system.

# Some add functions have special parameters. For example,
# addMiniToggleSwitch() lets you specify the orientation.
sp.addMiniToggleSwitch(hp(1), 20, "vertical")
sp.addMiniToggleSwitch(hp(1), 40, "vertical")
sp.addMiniToggleSwitch(hp(4), 40)

# sp.addPotentiometer(x, y)
# sp.addKnob(x, y, diameter, depth)
# Adding a pot doesn't automatically add a corresponding knob
# Knobs are for preview purposes only
sp.addPotentiometer(hp(4), 20)
sp.addKnob(hp(4), 20, 12, 16)

sp.addLed5mm(32, 10)
sp.addLed5mm(37, 15)
sp.addLed5mm(32, 20)
sp.addLed5mm(37, 25)
sp.addLed5mm(32, 30)
sp.addLed5mm(37, 35)
sp.addLed5mm(32, 40)
sp.addLed5mm(37, 45)

# Be sure to take a look at the functions in synthprinter.py!
# Their docstring comments often include more information about
# which hardware the footprints were tested to work with
sp.addArcadeButton24mm(hp(4), 60)
sp.addMiniJack(hp(1) + 1.5, 83)
sp.addBigJack(hp(4), 83)
sp.addMiniJack(hp(7) - 1.5, 83)
sp.addArcadeButton30mm(hp(4), 108)

# Only CQ-Editor supports this command
show_object(sp.panel, name="panel", options={"alpha": 0.1, "color": (0, 180, 230)})
show_object(sp.preview, name="preview", options={"alpha": 0.65, "color": (100, 30, 30)})
