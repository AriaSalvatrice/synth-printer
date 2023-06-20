import cadquery as cq
from synthprinter import *

sp = SynthPrinter()

# To quickly test the fit of a footprint, you can skip the
# format-specific panel creation helper functions and directly
# make a panel no bigger than necessary.
sp.addPanel(50, 50, screwSlots="none")
sp.addArcadeButton30mm(25, 25)

sp.render(show_object)
