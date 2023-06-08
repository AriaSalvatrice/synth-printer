import cadquery as cq
from synthprinter import *

# This is a faceplate for the North Coast Synthesis MSK 006,
# an exponential VCA made out of discrete components:
# https://northcoastsynthesis.com/synth-diy-projects/
#
# This project was built successfully:
# see ./images/example-02-quad-vca.jpg

# The panel engraving depth is increased from the default to achieve
# a more pronounced visual effect, but this weakens the panel, so
# pot notches in the way of the engravings are removed on the back,
# and the retaining notches for jacks are reduced.
sp = SynthPrinter(
    panelEngravingDepth=1.82,
    bigJackNotchDepth=0.6,
)

# width in kosmo horizontal pitch of 25mm
# This results in a 100mm wide panel
sp.addKosmoPanel(4)


# sp.addPotentiometer(x, y)
# sp.addKnob(x, y, diameter, depth)
# Adding a pot doesn't automatically add a corresponding knob
# Knobs are for preview purposes only
sp.addPotentiometer(kcol(1.5), krow(1), "left")
sp.addKnob(kcol(1.5), krow(1), 21, 16)
sp.addBigJack(kcol(1), krow(4.5))
sp.addBigJack(kcol(1), krow(6))
sp.addBigJack(kcol(1), krow(7))
# khp, kcol and krow are helpers to align to a 25mm grid.


# sp.engraveLine(FromX, FromY, Angle, Distance, Width)
#
# engraveLine has a default depth of 1.02mm, to ensure that at
# 0.20mm print settings, it has 5 layers instead of 4. This
# greatly helps with color changes, with fewer layers, the
# first color might be a bit translucent.
sp.engraveLine(kcol(1.5), khp(1), 180 + 45, 18.3, 2)
sp.engraveLine(kcol(1), khp(1.5) - 0.1, 180, khp(5.5), 2)

sp.addPotentiometer(kcol(2), krow(2.75), "right", "top")
sp.addKnob(kcol(2), krow(2.75), 21, 16)
sp.addBigJack(kcol(2), krow(4.5))
sp.addBigJack(kcol(2), krow(6))
sp.addBigJack(kcol(2), krow(7))

sp.engraveLine(kcol(2), krow(2.75), 180, khp(4.25), 2)

sp.addPotentiometer(kcol(3), krow(1), "left")
sp.addKnob(kcol(3), krow(1), 21, 16)
sp.addBigJack(kcol(3), krow(4.5))
sp.addBigJack(kcol(3), krow(6))
sp.addBigJack(kcol(3), krow(7))

sp.engraveLine(kcol(3), krow(1), 180, khp(6), 2)

sp.addPotentiometer(kcol(3.5), krow(2.75), "right", "top")
sp.addKnob(kcol(3.5), krow(2.75), 21, 16)
sp.addBigJack(kcol(4), krow(4.5))
sp.addBigJack(kcol(4), krow(6))
sp.addBigJack(kcol(4), krow(7))

sp.engraveLine(kcol(3.5), khp(2.75), 180 - 45, 18.3, 2)
sp.engraveLine(kcol(4), khp(3.24) - 0.1, 180, khp(3.75), 2)

sp.render()

show_object(sp.panel, name="panel", options={"alpha": 0, "color": (0, 180, 230)})
show_object(sp.preview, name="preview", options={"alpha": 0.65, "color": (100, 30, 30)})
