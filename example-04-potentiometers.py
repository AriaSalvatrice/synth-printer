import cadquery as cq
from synthprinter import *

sp = SynthPrinter()

# 1U panels are following the Intellijel dimensions.
sp.add1UIJPanel(8, screwSlots="center")

sp.addLed5mm(hp(1.5), 14)

# sp.addPotentiometer(x, y, notchOrientation, lugsOrientation)
# The optional orientation parameters are seen from the front, and are:
# "all", "none", "top", "left", "right", "bottom".
#
# The retaining notches aren't always on the same side, depending on the
# type of potentiometer!
# Unless you're printing with a transparent material, there should be no
# real drawbacks to leaving in all 4 notches, and you'll be happy to
# have a plan B for # kludges or component substitutions. Only change
# this option if you have a good reason to.
#
# The size of the preview box for the lugs doesn't account for the
# possibility of bending them upwards, so it might be safe to have this
# area overlap other stuff a little.
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

sp.render()

show_object(sp.panel, name="panel", options={"alpha": 0.1, "color": (0, 180, 230)})
show_object(sp.preview, name="preview", options={"alpha": 0.65, "color": (100, 30, 30)})
