import cadquery as cq
from synthprinter import *

# This project was built successfully.
# https://fedi.aria.dog/media/71dd4bd2ba8773d143337a12ba7a4d5b9e01c9e783cacab8c24a8f35734db232.jpg

sp = SynthPrinter()
sp.addKosmoPanel(3)

# Col 1
sp.addPotentiometer(kcol(1), krow(1), "all", "right")
sp.addKnob(kcol(1), krow(1), 21, 16)
sp.addPotentiometer(kcol(1), krow(2), "all", "right")
sp.addKnob(kcol(1), krow(2), 12, 16)
sp.addSlider(kcol(1), 100, 11.6, 68.4, 4, 50)
sp.addBigJack(kcol(1), krow(6))
sp.addBigJack(kcol(1), krow(7))
sp.engraveLine(kcol(1), krow(1), 180, 155, 2)
sp.engraveLine(kcol(1), krow(7), 45, 40, 2)

# Col 3
sp.addPotentiometer(kcol(3), krow(1), "all", "left")
sp.addKnob(kcol(3), krow(1), 21, 16)
sp.addPotentiometer(kcol(3), krow(2), "all", "left")
sp.addKnob(kcol(3), krow(2), 12, 16)
sp.addSlider(kcol(3), 100, 11.6, 68.4, 4, 50)
sp.addBigJack(kcol(3), krow(6))
sp.addBigJack(kcol(3), krow(7))
sp.engraveLine(kcol(3), krow(1), 180, 155, 2)
sp.engraveLine(kcol(3), krow(7), -45, 40, 2)

# Col 2
sp.addPotentiometer(kcol(2), krow(4), "all", "left")
sp.addKnob(kcol(2), krow(4), 21, 16)
sp.addBigJack(kcol(2), krow(6))
sp.addBigJack(kcol(2), krow(7))
sp.addLed5mm(kcol(1.75), krow(2.75))
sp.addLed5mm(kcol(2.25), krow(2.75))
sp.addLed5mm(kcol(1.75), krow(3.25))
sp.addLed5mm(kcol(2.25), krow(3.25))
sp.addLed5mm(kcol(2), krow(4.75))
sp.addLed5mm(kcol(2), krow(5.25))
sp.engraveLine(kcol(2), krow(4), 180, 75, 2)
sp.engraveLine(kcol(1.75), krow(2.75), -90, 18, 2)
sp.engraveLine(kcol(2.25), krow(2.75), 90, 18, 2)
sp.engraveLine(kcol(1.75), krow(3.25), -90, 18, 2)
sp.engraveLine(kcol(2.25), krow(3.25), 90, 18, 2)

sp.supportBar(0, 9, 75, 5, 6)
sp.supportBar(0, 185, 75, 5, 6)
sp.supportBar(48, 59, 5, 130, 6)
sp.supportBar(48, 59, -20, 5, 6)
sp.supportBar(37.5, 9, 5, 50, 6)

sp.render()

show_object(sp.panel, name="panel", options={"alpha": 0.2, "color": (0, 180, 230)})
show_object(
    sp.supports, name="supports", options={"alpha": 0.1, "color": (180, 230, 0)}
)
show_object(sp.preview, name="preview", options={"alpha": 0.65, "color": (100, 30, 30)})
