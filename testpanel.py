import cadquery as cq
from synthprinter import *

# You can override any setting from the defaultConfig
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

sp.addPotentiometer(hp(4), 20)

sp.addLed5mm(32, 10)
sp.addLed5mm(37, 15)
sp.addLed5mm(32, 20)
sp.addLed5mm(37, 25)
sp.addLed5mm(32, 30)
sp.addLed5mm(37, 35)
sp.addLed5mm(32, 40)
sp.addLed5mm(37, 45)

sp.addMiniToggleSwitch(hp(4), 40)


sp.addArcadeButton24mm(hp(4), 60)
sp.addBigJack(hp(4), 83)
sp.addArcadeButton30mm(hp(4), 108)


sp.assemble()
show_object(sp.panelAssembly, "panel")
show_object(sp.previewAssembly, "preview")
