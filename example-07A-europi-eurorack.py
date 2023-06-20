import cadquery as cq
from synthprinter import *

# The EuroPi faceplate reproduced in Synth-Printer, using the original PCBs,
# but a different button type glued to the panel.
#
# EuroPi project: https://www.allensynthesis.co.uk/modules/europi.html
#
# Take a look at this handy reference:
# https://github.com/Allen-Synthesis/EuroPi/blob/main/hardware/EuroPi/panel/panel%20dimensions.svg
# Notice how I'm using directly the numbers from that drawing in the code.
#
# This project was built successfully:
# see ./images/example-07A-europi-eurorack.jpg

sp = SynthPrinter()

sp.addEurorackPanel(8)

sp.addMiniJack(10, 9.25 + 8.5)
sp.addMiniJack(hp(8) - 10, 9.25 + 8.5)

sp.addDisplayWindow(hp(4), 9.25 + 27 - 6.80 / 2, 24.4, 7.5, 0, 0, 0, 0, False)

sp.addPotentiometer(10, 9.25 + 43.25, "none", "none")
sp.addPotentiometer(hp(8) - 10, 9.25 + 43.25, "none", "none")

sp.addKnob(10, 9.25 + 43.25, 12, 16)
sp.addKnob(hp(8) - 10, 9.25 + 43.25, 12, 16)

# Using a less expensive & easier to source pushbutton type than those
# recommended by the BOM: a common 12mm tactile switch often used with
# breadboards. It's glued in place and wired to the PCB.
# The switch cover was printed using this STL as base:
# https://www.thingiverse.com/thing:493729
sp.cutRect(10, 9.25 + 58.75 + 3, 12.2, 12.2, False)
sp.cutRect(hp(8) - 10, 9.25 + 58.75 + 3, 12.2, 12.2, False)

sp.addLed3mm(7.5, 9.25 + 74.5)
sp.addLed3mm(hp(4), 9.25 + 74.5)
sp.addLed3mm(hp(8) - 7.5, 9.25 + 74.5)

sp.addMiniJack(7.5, 9.25 + 83)
sp.addMiniJack(hp(4), 9.25 + 83)
sp.addMiniJack(hp(8) - 7.5, 9.25 + 83)

sp.addLed3mm(7.5, 9.25 + 93.5)
sp.addLed3mm(hp(4), 9.25 + 93.5)
sp.addLed3mm(hp(8) - 7.5, 9.25 + 93.5)

sp.addMiniJack(7.5, 9.25 + 102)
sp.addMiniJack(hp(4), 9.25 + 102)
sp.addMiniJack(hp(8) - 7.5, 9.25 + 102)

sp.render(show_object)
