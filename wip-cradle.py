import cadquery as cq
from synthprinter import *

sp = SynthPrinter()

sp.addKosmoPanel(11)

sp.addEurorackCradle(kcol(1), krow(1), 6, False, "vertical")
sp.addMiniJack(kcol(1), krow(1))

sp.addEurorackCradle(kcol(1), krow(5), 18, True, "vertical")
sp.addMiniJack(kcol(1), krow(5))

sp.addEurorackCradle(kcol(7), krow(1), 5, False, "horizontal")
sp.addMiniJack(kcol(7), krow(1))

sp.addEurorackCradle(kcol(10), krow(1), 11, True, "horizontal")
sp.addMiniJack(kcol(10), krow(1))

# Mults
# sp.addMiniJack(kcol(1), krow(6.2))
# sp.addMiniJack(kcol(2), krow(6.2))
# sp.addMiniJack(kcol(3), krow(6.2))
# sp.addMiniJack(kcol(4), krow(6.2))
# sp.addMiniJack(kcol(1), krow(6.7))
# sp.addMiniJack(kcol(2), krow(6.7))
# sp.addMiniJack(kcol(3), krow(6.7))
# sp.addMiniJack(kcol(4), krow(6.7))
# sp.addBigJack(kcol(1), krow(7.3))
# sp.addBigJack(kcol(2), krow(7.3))
# sp.addBigJack(kcol(3), krow(7.3))
# sp.addBigJack(kcol(4), krow(7.3))

sp.render(show_object)
