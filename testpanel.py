import cadquery as cq
from synthprinter import *

sp = SynthPrinter()

sp.addKosmoPanel(25, screwNotches="center")
sp.cutArcadeButton30mm(20, 20)
sp.cutArcadeButton24mm(40, 40)
sp.cutMiniToggleSwitch(60, 60)
sp.cutPotentiometer(20, 80)
sp.cutPotentiometer(20, 80)
sp.cutBigJack(70, 20)
sp.cutLed5mm(100, 40)
sp.cutLed3mm(100, 60)
sp.cutDisplayWindow(120, 120)

sp.preview = sp.preview.box(70, 70, 70)

sp.assemble()
show_object(sp.panelAssembly, "panel")
show_object(sp.previewAssembly, "preview")
