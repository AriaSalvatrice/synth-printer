import cadquery as cq
from synthprinter import *

# Override any setting from the defaultConfig
sp = SynthPrinter(
    tolerance=0.4,
    panelColorRGBA=cq.Color(0.5, 0.9, 0.5, 0.9),
    miniToggleSwitchDiameter=6,
)

sp.addEurorackPanel(8)  # HP

sp.addLed5mm(hp(1), 10)
sp.addMiniToggleSwitch(hp(1), 20, "vertical")
sp.addLed3mm(hp(1), 30)
sp.addMiniToggleSwitch(hp(1), 40, "vertical")
sp.addMiniToggleSwitch(hp(4), 40)

sp.addPotentiometer(hp(4), 20)
sp.addKnob(hp(4), 20, 12, 16)

sp.addLed5mm(32, 10)
sp.addLed5mm(37, 15)
sp.addLed5mm(32, 20)
sp.addLed5mm(37, 25)
sp.addLed5mm(32, 30)
sp.addLed5mm(37, 35)
sp.addLed5mm(32, 40)
sp.addLed5mm(37, 45)

sp.addArcadeButton24mm(hp(4), 60)
sp.addMiniJack(hp(1) + 1.5, 83)
sp.addBigJack(hp(4), 83)
sp.addMiniJack(hp(7) - 1.5, 83)
sp.addArcadeButton30mm(hp(4), 108)

show_object(sp.panel, name="panel", options={"alpha": 0.1, "color": (0, 180, 230)})
show_object(sp.preview, name="preview", options={"alpha": 0.65, "color": (100, 30, 30)})
