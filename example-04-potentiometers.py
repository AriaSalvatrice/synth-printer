import cadquery as cq
from synthprinter import *

sp = SynthPrinter()

# Normally, Synth Printer decides for you how
# many screwNotches to add, but you can force the matter.
# 1U panel are following the Intellijel dimensions.
sp.add1UIJPanel(8, screwNotches="center")


# sp.addArcadeButton30mm(25, 25)
sp.addLed5mm(hp(1.5), 14)

# sp.addPotentiometer(x, y, notchOrientation, lugsOrientation)
# The optional orientation parameters are seen from the front, and are:
# "all", "none", "top", "left", "right", "bottom".
#
# The retaining notches aren't always on the same side, depending on the
# type of potentiometer! If in doubt, just leave it to "all" to add 4 notches.
#
# The preview size for the lugs doesn't account for the possibility of bending them,
# so it might be safe to have this area overlap other stuff a little.
sp.addPotentiometer(hp(4), 14, "top", "right")

# sp.addKnob(x, y, diameter, depth)
# Adding a potentiometer only adds a preview for a shaft.
# If you want a knob on it, add it separately with addKnob()
# It's only for preview purposes. Make sure there's enough room
# for your fingies to grab them! It's easy to design faceplates
# too densely packed where controls are a pain to tweak.
sp.addKnob(hp(4), 14, 16, 20)

sp.addMiniJack(hp(1.5), 28)
sp.addMiniJack(hp(6.5), 28)

show_object(sp.panel, name="panel", options={"alpha": 0.1, "color": (0, 180, 230)})
show_object(sp.preview, name="preview", options={"alpha": 0.65, "color": (100, 30, 30)})
