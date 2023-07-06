import cadquery as cq
from synthprinter import *

sp = SynthPrinter()

# This is a cradle for two rows of 1U tiles (Intellijel) on a Eurorack panel.
# Very similar to the previous example for Kosmo.
sp.addEurorackPanel(16)

# To allow stacking two rails close to each other, skip overlapping supports
sp.add1UIJCradle(hp(8), 14, 14, True, "horizontal", supportBottom=False)
sp.add1UIJCradle(hp(8), 54, 14, True, "horizontal", supportTop=False)

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

sp.supportBar(hp(5.5) - 2, 92, 4, 25, 4)
sp.supportBar(hp(10.5) - 2, 92, 4, 25, 4)

# Here's an alternate 12hp version I made for my own use:

# sp.addEurorackPanel(12)
# sp.add1UIJCradle(hp(6), 14, 10, True, "horizontal", supportBottom=False)
# sp.add1UIJCradle(hp(6), 54, 10, True, "horizontal", supportTop=False)
# sp.addMiniJack(hp(2), 104)
# sp.addMiniJack(hp(4), 104)
# sp.addMiniJack(hp(8), 104)
# sp.addMiniJack(hp(10), 104)
# sp.addMiniJack(hp(2), 104 + hp(2.5))
# sp.addMiniJack(hp(4), 104 + hp(2.5))
# sp.addMiniJack(hp(8), 104 + hp(2.5))
# sp.addMiniJack(hp(10), 104 + hp(2.5))
# sp.supportBar(hp(6) - 2, 92, 4, 25, 4)

sp.render(show_object)
