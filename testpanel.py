import cadquery as cq
from synthprinter import *

panel = eurorackPanel(hp(8))

panel = arcadeButton30mmHole(panel, 20, 20)
panel = led5mmHole(panel, 10, 40)
panel = led3mmHole(panel, 10, 48)
panel = potentiometerHole(panel, 30, 45)
panel = bigJackHole(panel, 20, 65)
panel = miniToggleSwitch(panel, 8, 85)
panel = miniToggleSwitch(panel, 20, 85, orientation="vertical")
panel = miniToggleSwitch(panel, 32, 85, orientation="horizontal")
