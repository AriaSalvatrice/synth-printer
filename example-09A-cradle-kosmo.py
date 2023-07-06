import cadquery as cq
from synthprinter import *

sp = SynthPrinter()

# This panel is a cradle for a Eurorack module, on a Kosmo faceplate.

sp.addKosmoPanel(3)

#                    Can also make the rails "vertical" _
#                  False to align to top-left _          \
#                                     hp _     \         |
#                                         \    |         |
#                                         |    |         |
sp.addEurorackCradle(kcol(2), krow(0.7), 12, True, "horizontal")

# Some passive mults converting between mini jacks and big jacks.
# Another good way to make the leftover space useful would be
# to add attenuators.
sp.addMiniJack(kcol(1), krow(6.2))
sp.addMiniJack(kcol(2), krow(6.2))
sp.addMiniJack(kcol(3), krow(6.2))
sp.addMiniJack(kcol(1), krow(6.7))
sp.addMiniJack(kcol(2), krow(6.7))
sp.addMiniJack(kcol(3), krow(6.7))
sp.addBigJack(kcol(1), krow(7.3))
sp.addBigJack(kcol(2), krow(7.3))
sp.addBigJack(kcol(3), krow(7.3))

# Additional supports
sp.supportBar(kcol(1.5) - 2, 145, 4, 45, 4)
sp.supportBar(kcol(2.5) - 2, 145, 4, 45, 4)

sp.render(show_object)
