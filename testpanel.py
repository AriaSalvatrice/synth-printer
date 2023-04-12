import cadquery as cq
from synthprinter import *

panel = eurorackPanel(hp(12))

panel = arcadeButton30mmHole(panel, 20, 20)
panel = led5mmHole(panel, 10, 40)
panel = led3mmHole(panel, 10, 48)
panel = potentiometerHole(panel, 30, 45)
panel = bigJackHole(panel, 15, 60)
panel = miniToggleSwitch(panel, 46, 15)
panel = miniToggleSwitch(panel, 46, 35, orientation="vertical")
panel = miniToggleSwitch(panel, 46, 55, orientation="horizontal")

panel = displayWindow(
    panel=panel,
    x=28,
    y=95,
    windowWidth=26.0,
    windowLength=14.5,
    windowVerticalOffset=-10,
    screwsHorizontalDistance=47.2,
    screwsVerticalDistance=47.2,
)
