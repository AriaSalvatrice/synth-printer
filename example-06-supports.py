import cadquery as cq
from synthprinter import *

# You can override the default panel thickness, but bear in mind footprints
# are only guaranteed to work well at the default of 4mm
sp = SynthPrinter(
    panelThickness=2,
)

sp.addKosmoPanel(8)
sp.addBigJack(30, 30)

# To reinforce a panel thinner than the default, you can add support bars
# in both directions, to increase stiffness.
# You could even do it for a panel the default thickness, but I don't find
# it necessary.
sp.supportBar(0, 10, 200, 5, 6)
sp.supportBar(0, 190, 200, 5, 6)
sp.supportBar(10, 10, 5, 180, 6)
sp.supportBar(190, 10, 5, 180, 6)

sp.render(show_object)
