import cadquery as cq
from synthprinter import *

sp = SynthPrinter()

# Normally, Synth Printer decides for you how many screwNotches
# to add, but you can force the matter.
#
# Your options are:
# auto, auto-tlbr:
#   4 notches if enough room, otherwise, 2 notches in the top-left and bottom-right
# tlbr:
#   2 notches in the top-left and bottom-right
# auto-trbl:
#   4 notches if enough room, otherwise, 2 notches in the top-right and bottom-left
# auto-center:
#   4 notches if enough room, otherwise, 2 notches in the center (not guaranteed to line up with rails)
# center:
#   2 notches in the center (not guaranteed to line up with rails)
# all:
#   4 notches. if not enough room, they will be merged.
# none:
#   yup
sp.addEurorackPanel(3, screwNotches="auto-trbl")

sp.addMiniJack(hp(1.5), 30)
sp.addMiniJack(hp(1.5), 60)
sp.addLed5mm(hp(1.5), 90)

show_object(sp.panel, name="panel", options={"alpha": 0.1, "color": (0, 180, 230)})
show_object(sp.preview, name="preview", options={"alpha": 0.65, "color": (100, 30, 30)})
