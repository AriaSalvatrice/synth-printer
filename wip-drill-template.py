import cadquery as cq
from synthprinter import *

sp = SynthPrinter(
    drillTemplateShow=True,
    previewShow=False,
)

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

sp.render(show_object)

sp.exportDrillTemplate()
