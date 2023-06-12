import cadquery as cq
from synthprinter import *

sp = SynthPrinter()

sp.addKosmoPanel(4)

# Only pots are supported for now

sp.addPotentiometer(kcol(2.5), krow(1.75))
sp.addKnob(kcol(2.5), krow(1.75), 37, 24)

sp.addPotentiometer(kcol(1), krow(4))
sp.addKnob(kcol(1), krow(4), 18, 16)

sp.addPotentiometer(kcol(4), krow(4))
sp.addKnob(kcol(4), krow(4), 18, 16)

sp.render()

# TODO: Make this unnecessary for users
sp.panel = sp.panel.rotate((0, 0, 0), (1, 0, 0), 180)
sp.preview = sp.preview.rotate((0, 0, 0), (1, 0, 0), 180)
sp.supports = sp.supports.rotate((0, 0, 0), (1, 0, 0), 180)
sp.drillTemplate = sp.drillTemplate.rotate((0, 0, 0), (1, 0, 0), 180)

show_object(sp.panel, name="panel", options={"alpha": 0.2, "color": (0, 180, 230)})
show_object(
    sp.supports, name="supports", options={"alpha": 0.1, "color": (180, 230, 0)}
)
show_object(sp.preview, name="preview", options={"alpha": 0.65, "color": (100, 30, 30)})
show_object(
    sp.drillTemplate,
    name="drillTemplate",
    options={"alpha": 0.1, "color": (50, 200, 50)},
)

cq.exporters.export(
    sp.drillTemplate,
    "testTemplate.svg",
    opt={
        "width": 2000,
        "height": 2000,
        "marginLeft": 0,
        "marginTop": 0,
        "showAxes": False,
        "projectionDir": (0.0, 0.0, 1.0),
        "strokeWidth": 0.25,
        "strokeColor": (255, 0, 0),
        "hiddenColor": (0, 0, 255),
        "showHidden": False,
    },
)
