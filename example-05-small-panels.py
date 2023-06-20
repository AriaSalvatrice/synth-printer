import cadquery as cq
from synthprinter import *

sp = SynthPrinter()

# Normally, Synth Printer decides for you how many screwSlots
# to add, but you can force the matter.
#
# Your options are:
# auto, auto-tlbr:
#   4 slots if enough room, otherwise, 2 slots in the top-left and bottom-right
# tlbr:
#   2 slots in the top-left and bottom-right
# auto-trbl:
#   4 slots if enough room, otherwise, 2 slots in the top-right and bottom-left
# auto-center:
#   4 slots if enough room, otherwise, 2 slots in the center (not guaranteed to line up with rails)
# center:
#   2 slots in the center (not guaranteed to line up with rails)
# all:
#   4 slots. if not enough room, they will be merged.
# none:
#   yup
sp.addEurorackPanel(3, screwSlots="auto-trbl")

sp.addMiniJack(hp(1.5), 30)
sp.addMiniJack(hp(1.5), 60)
sp.addLed5mm(hp(1.5), 90)

sp.render(show_object)
