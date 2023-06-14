import cadquery as cq
from synthprinter import *

sp = SynthPrinter()

sp.addKosmoPanel(10)

sp.addPotentiometer(kcol(1.5), krow(1))
sp.addKnob(kcol(1.5), krow(1), 37, 24)
sp.addSlider(kcol(1), krow(3.5), 11.6, 68.4, 4, 50)
sp.addLed5mm(kcol(1), krow(5) + 5)
sp.addLed3mm(kcol(1), krow(5) + 20)
sp.addBigJack(kcol(1), krow(6.5))
sp.addMiniJack(kcol(1), krow(7.25))

sp.addMiniToggleSwitch(kcol(2), krow(2.5), "horizontal")
sp.addMiniToggleSwitch(kcol(2), krow(3.5), "vertical")
sp.addArcadeButton30mm(kcol(2), krow(5))
sp.addArcadeButton24mm(kcol(2), krow(7))

sp.addDisplayWindow(kcol(3), krow(1), 25, 15, 10, -5, 35, 35, True)


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
