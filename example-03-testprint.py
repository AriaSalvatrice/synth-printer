import cadquery as cq
from synthprinter import *

sp = SynthPrinter()

# To quickly test the fit of a footprint, you can skip the
# format-specific panel creation helper functions and directly
# make a panel no bigger than necessary.
sp.addPanel(50, 50, screwNotches="none")
sp.addArcadeButton30mm(25, 25)

show_object(sp.panel, name="panel", options={"alpha": 0.1, "color": (0, 180, 230)})
show_object(sp.preview, name="preview", options={"alpha": 0.65, "color": (100, 30, 30)})
