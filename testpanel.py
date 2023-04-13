import cadquery as cq
from synthprinter import *

sp = SynthPrinter()

sp.addEurorackPanel(8)

sp.addLed5mm(hp(1), 10)
sp.addMiniToggleSwitch(hp(1), 20, "vertical")
sp.addLed3mm(hp(1), 30)

sp.addPotentiometer(hp(4), 20)

sp.addLed5mm(hp(7), 10)
sp.addLed5mm(hp(7), 20)
sp.addLed5mm(hp(7), 30)
sp.addLed5mm(hp(7), 40)

sp.addMiniToggleSwitch(hp(4), 40)


sp.addArcadeButton24mm(hp(4), 60)
sp.addBigJack(hp(4), 83)
sp.addArcadeButton30mm(hp(4), 108)


sp.assemble()
show_object(sp.panelAssembly, "panel")
show_object(sp.previewAssembly, "preview")
