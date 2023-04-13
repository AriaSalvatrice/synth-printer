import cadquery as cq
from synthprinter import *

sp = SynthPrinter()

sp.addKosmoPanel(150, screwNotches="auto")
sp.addArcadeButton30mm(20, 20)
sp.addArcadeButton24mm(40, 40)
sp.addMiniToggleSwitch(60, 60)
sp.addPotentiometer(20, 80)
sp.addBigJack(70, 20)
sp.addLed5mm(100, 40)
sp.addLed3mm(100, 60)
sp.cutDisplayWindow(120, 120)

sp.preview = sp.preview.box(70, 70, 70)

sp.assemble()
show_object(sp.panelAssembly, "panel")
show_object(sp.previewAssembly, "preview")
