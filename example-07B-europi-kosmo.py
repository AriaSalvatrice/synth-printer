import cadquery as cq
from synthprinter import *

sp = SynthPrinter()

# A port of the EuroPi to the 5U Kosmo format!
#
# EuroPi project: https://www.allensynthesis.co.uk/modules/europi.html
#
# Controls are wired directly to the original PCB, where eurorack-sized
# components would normally go.
#
# I placed the input jacks at the bottom, and placed the status LED below
# the jacks, for greater consistency with my Kosmo system.
#
# This project was built successfully:
# see ./images/full-system.jpeg (bottom-left)


sp.addKosmoPanel(3)

sp.addDisplayWindow(kcol(2), krow(0.75), 23.38, 6.58, 0, 0, 0, 0, False)

sp.addPotentiometer(kcol(1.25), krow(1.75))
sp.addPotentiometer(kcol(2.75), krow(1.75))
sp.addKnob(kcol(1.25), krow(1.75), 21, 16)
sp.addKnob(kcol(2.75), krow(1.75), 21, 16)

sp.addArcadeButton24mm(kcol(1.25), krow(3.5))
sp.addArcadeButton24mm(kcol(2.75), krow(3.5))

sp.addBigJack(kcol(1), krow(5))
sp.addBigJack(kcol(3), krow(5))
sp.addBigJack(kcol(1), krow(6))
sp.addBigJack(kcol(2), krow(6))
sp.addBigJack(kcol(3), krow(6))
sp.addBigJack(kcol(1), krow(7))
sp.addBigJack(kcol(2), krow(7))
sp.addBigJack(kcol(3), krow(7))

sp.addLed5mm(kcol(1), krow(6.5))
sp.addLed5mm(kcol(2), krow(6.5))
sp.addLed5mm(kcol(3), krow(6.5))
sp.addLed5mm(kcol(1), krow(7.5))
sp.addLed5mm(kcol(2), krow(7.5))
sp.addLed5mm(kcol(3), krow(7.5))


sp.render()

show_object(sp.panel, name="panel", options={"alpha": 0.2, "color": (0, 180, 230)})
show_object(sp.preview, name="preview", options={"alpha": 0.65, "color": (100, 30, 30)})
