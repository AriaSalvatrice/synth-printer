import cadquery as cq
from synthprinter import *

# This one is for a Quad VCA in Kosmo format.
#
# khp, kcol and krow are helpers to align to a 25mm grid.
#
# engraveLine has a default depth of 1.02mm, to ensure that at
# 0.20mm print settings, it has 5 layers instead of 4. This
# greatly helps with color changes, with fewer layers, the
# first color might be a bit translucent.

# Start by creating a SynthPrinter object
sp = SynthPrinter()

# You can only add one panel
sp.addKosmoPanel(100)  # width in millimeters
# sp.addKosmoPanel(khp(25)) <- Identical to above


# sp.addPotentiometer(x, y)
# sp.addKnob(x, y, diameter, depth)
# Adding a pot doesn't automatically add a corresponding knob
# Knobs are for preview purposes only
sp.addPotentiometer(kcol(1.5), krow(1))
sp.addKnob(kcol(1.5), krow(1), 21, 16)
sp.addBigJack(kcol(1), krow(4.5))
sp.addBigJack(kcol(1), krow(6))
sp.addBigJack(kcol(1), krow(7))

# sp.engraveLine(FromX, FromY, Angle, Distance, Width)
sp.engraveLine(kcol(1.5), khp(1), 180 + 45, 18.3, 2)
sp.engraveLine(kcol(1), khp(1.5) - 0.1, 180, khp(5.5), 2)

sp.addPotentiometer(kcol(2), krow(2.75))
sp.addKnob(kcol(2), krow(2.75), 21, 16)
sp.addBigJack(kcol(2), krow(4.5))
sp.addBigJack(kcol(2), krow(6))
sp.addBigJack(kcol(2), krow(7))

sp.engraveLine(kcol(2), krow(2.75), 180, khp(4.25), 2)

sp.addPotentiometer(kcol(3), krow(1))
sp.addKnob(kcol(3), krow(1), 21, 16)
sp.addBigJack(kcol(3), krow(4.5))
sp.addBigJack(kcol(3), krow(6))
sp.addBigJack(kcol(3), krow(7))

sp.engraveLine(kcol(3), krow(1), 180, khp(6), 2)

sp.addPotentiometer(kcol(3.5), krow(2.75))
sp.addKnob(kcol(3.5), krow(2.75), 21, 16)
sp.addBigJack(kcol(4), krow(4.5))
sp.addBigJack(kcol(4), krow(6))
sp.addBigJack(kcol(4), krow(7))

sp.engraveLine(kcol(3.5), khp(2.75), 180 - 45, 18.3, 2)
sp.engraveLine(kcol(4), khp(3.24) - 0.1, 180, khp(3.75), 2)

# Only CQ-Editor supports this command
show_object(sp.panel, name="panel", options={"alpha": 0, "color": (0, 180, 230)})
show_object(sp.preview, name="preview", options={"alpha": 0.65, "color": (100, 30, 30)})
