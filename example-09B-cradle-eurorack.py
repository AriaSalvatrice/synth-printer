import cadquery as cq
from synthprinter import *

sp = SynthPrinter()

# This is a cradle for two rows of 1U tiles (Intellijel) on a Eurorack panel.
# Very similar to the previous example for Kosmo.
sp.addEurorackPanel(16)

sp.add1UIJCradle(hp(8), 14, 14, True, "horizontal")
sp.add1UIJCradle(hp(8), 54, 14, True, "horizontal")

sp.addMiniJack(hp(2), 104)
sp.addMiniJack(hp(4), 104)
sp.addMiniJack(hp(7), 104)
sp.addMiniJack(hp(9), 104)
sp.addMiniJack(hp(12), 104)
sp.addMiniJack(hp(14), 104)

sp.addMiniJack(hp(2), 104 + hp(2.5))
sp.addMiniJack(hp(4), 104 + hp(2.5))
sp.addMiniJack(hp(7), 104 + hp(2.5))
sp.addMiniJack(hp(9), 104 + hp(2.5))
sp.addMiniJack(hp(12), 104 + hp(2.5))
sp.addMiniJack(hp(14), 104 + hp(2.5))

sp.supportBar(hp(5.5) - 2, 92, 4, 30, 4)
sp.supportBar(hp(10.5) - 2, 92, 4, 30, 4)

sp.render(show_object)
