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
sp.addSupportBar(0, 10, 200, 5, 6)
sp.addSupportBar(0, 190, 200, 5, 6)
sp.addSupportBar(10, 10, 5, 180, 6)
sp.addSupportBar(190, 10, 5, 180, 6)

sp.render()

# If you add supports, you must also display this layer.
# To export as a single STL, in CQ-editor, simply shift-click both
# "panel" and "supports" in the Objects outliner, then right-click and export as STL.
show_object(sp.panel, name="panel", options={"alpha": 0.1, "color": (0, 180, 230)})
show_object(
    sp.supports, name="supports", options={"alpha": 0.1, "color": (180, 230, 0)}
)
show_object(sp.preview, name="preview", options={"alpha": 0.65, "color": (100, 30, 30)})
