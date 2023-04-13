import cadquery as cq
import synthprinter

sp = synthprinter.SynthPrinter(
    # tolerance=3,
    panelWidth=200,
    panelHeight=200,
)
sp.addPanel()
sp.cutArcadeButton30mm(20, 20)
sp.cutArcadeButton24mm(40, 40)
sp.cutMiniToggleSwitch(60, 60)
sp.cutPotentiometer(20, 80)
sp.cutPotentiometer(20, 80)
sp.cutBigJack(70, 20)
sp.cutLed5mm(100, 40)
sp.cutLed3mm(100, 60)
sp.cutDisplayWindow(120, 120)

show_object(sp.panel, name="Panel")
