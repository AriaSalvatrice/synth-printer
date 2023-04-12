import cadquery as cq
from decimal import Decimal

#######################################################################
### Common Dimensions

_tolerance = 0.4  # Default tolerance for most holes
_panelHeight = 100.0
_panelThickness = 4.0
_hp = 5.08
_retainingNotchDepth = _panelThickness / 3


#######################################################################
### Screws

_m3Diameter = 3.0
_m3DiameterWithTolerance = _m3Diameter + _tolerance
_ScrewNotchDistanceFromTop = 3.0
_ScrewNotchDistanceFromBottom = 3.0
_ScrewNotchDistanceFromSide = _m3DiameterWithTolerance * 1.5


#######################################################################
### Buttons and switches

_sanwaOBSF24Button = 24  # FIXME: UNTESTED!!
_sanwaOBSF24ButtonWithTolerance = _sanwaOBSF24Button + _tolerance
_sanwaOBSF30Button = 30
_sanwaOBSF30ButtonWithTolerance = _sanwaOBSF30Button + _tolerance
_miniToggleSwitchWidth = 13.2
_miniToggleSwitchLength = 7.9
_miniToggleSwitchDiameter = 6
_miniToggleSwitchWidthWithTolerance = _miniToggleSwitchWidth + _tolerance
_miniToggleSwitchLengthWithTolerance = _miniToggleSwitchLength + _tolerance
_miniToggleSwitchDiameterWithTolerance = _miniToggleSwitchDiameter + _tolerance
_miniToggleSwitchNotchDepth = _retainingNotchDepth


#######################################################################
### Potentiometers and rotary encoders

_potentiometerShaftDiameter = 6  # FIXME: I used to use 7.35!!
_potentiometerShaftDiameterWithTolerance = _potentiometerShaftDiameter + _tolerance
_potentiometerNotchDistanceFromCenter = 6.9
_potentiometerNotchDiameter = 3.9
_potentiometerNotchDepth = _panelThickness / 1.5

#######################################################################
### Jacks
_bigJackDiameter = 10
_bigJackDiameterWithTolerance = 10 + _tolerance
_bigJackWidth = 16
_bigJackLength = _bigJackWidth
_bigJackWidthWithTolerance = _bigJackWidth + _tolerance
_bigJackLengthWithTolerance = _bigJackLength + _tolerance
_bigJackNotchDepth = _retainingNotchDepth

#######################################################################
### Blinkenlichten

_5mmLed = 5
_5mmLedWithTolerance = _5mmLed + _tolerance
_3mmLed = 3
_3mmLedWithTolerance = _3mmLed + _tolerance  # FIXME: UNTESTED!!


#######################################################################
### Eurorack

_eurorackHeight = 128.5  # Modules are smaller than the full 3U
_eurorackScrewNotchDistanceFromSide = _ScrewNotchDistanceFromSide
_eurorackScrewNotchDistanceFromTop = _ScrewNotchDistanceFromTop
_eurorackScrewNotchDistanceFromBottom = _ScrewNotchDistanceFromBottom
_i1UHeight = 39.65  # Itellijel 1U - for our purposes, normal Euro but 1U tall


#######################################################################
### Kosmo

_kosmoHeight = 200.0
_kosmoScrewNotchDistanceFromSide = _ScrewNotchDistanceFromSide
_kosmoScrewNotchDistanceFromTop = _ScrewNotchDistanceFromTop
_kosmoScrewNotchDistanceFromBottom = _ScrewNotchDistanceFromBottom


#######################################################################
#######################################################################
#######################################################################
#######################################################################
#######################################################################


#######################################################################
### Helpers


def hp(hp: int) -> float:
    """Converts Horizontal Pitch to millimeters.

    1 HP == 0.2 inches == 5.08 millimeters

    Eurorack sizes are generally an even number of hp, such as 4hp.
    3hp and 5hp are the only odd number sizes commonly seen in commercial hardware.
    """
    return hp * _hp


def makeHole(panel, x: float, y: float, width: float = _5mmLedWithTolerance):
    panel = (
        panel.faces(">Z")
        .vertices("<XY")
        .workplane(centerOption="CenterOfMass")
        .center(x, y)
        .hole(width)
    )
    return panel


#######################################################################
### Panels


def panel(
    width: float = _panelHeight,
    height: float = _panelHeight,
    thickness: float = _panelThickness,
    screwNotchBottomLeft: bool = True,
    screwNotchBottomRight: bool = True,
    screwNotchTopLeft: bool = True,
    screwNotchTopRight: bool = True,
    screwNotchDistanceFromSide: float = _ScrewNotchDistanceFromSide,
    screwNotchDistanceFromTop: float = _ScrewNotchDistanceFromTop,
    screwNotchDistanceFromBottom: float = _ScrewNotchDistanceFromBottom,
    screwNotchWidth: float = _m3DiameterWithTolerance * 2.5,
    screwNotchHeight: float = _m3DiameterWithTolerance,
):
    """Returns a rectangular panel of arbitrary dimensions.

    Screw notches in the corners provide better tolerances than holes
    in a DIY printed system.
    """

    panel = cq.Workplane("XY").box(width, height, thickness)

    screwPoints = []
    if screwNotchBottomLeft:
        screwPoints.append((screwNotchDistanceFromSide, screwNotchDistanceFromBottom))
    if screwNotchBottomRight:
        screwPoints.append(
            (width - screwNotchDistanceFromSide, screwNotchDistanceFromBottom)
        )
    if screwNotchTopLeft:
        screwPoints.append(
            (screwNotchDistanceFromSide, height - screwNotchDistanceFromTop)
        )
    if screwNotchTopRight:
        screwPoints.append(
            (width - screwNotchDistanceFromSide, height - screwNotchDistanceFromTop)
        )

    panel = (
        panel.faces(">Z")
        .workplane()
        .center(-width / 2, -height / 2)
        .pushPoints(screwPoints)
        .slot2D(screwNotchWidth, screwNotchHeight, 0)
        .cutThruAll()
    )

    return panel


def eurorackPanel(
    width: float = hp(2),
    height: float = _eurorackHeight,
    thickness: float = _panelThickness,
):
    """Returns a Eurorack panel with screw notches. Eurorack width must be defined in hp().

    A thickness of 4mm minimum is recommended for solidity."""

    if width < hp(2):
        raise Warning("Eurorack panels should be at least 2hp wide")

    # Skip two notches if the panel is too small
    if width >= hp(4):
        addAllScrewNotches = True
    else:
        addAllScrewNotches = False

    return panel(
        width=width,
        height=height,
        thickness=thickness,
        screwNotchDistanceFromSide=_eurorackScrewNotchDistanceFromSide,
        screwNotchDistanceFromTop=_eurorackScrewNotchDistanceFromTop,
        screwNotchDistanceFromBottom=_eurorackScrewNotchDistanceFromBottom,
        screwNotchBottomLeft=addAllScrewNotches,
        screwNotchBottomRight=True,
        screwNotchTopLeft=True,
        screwNotchTopRight=addAllScrewNotches,
    )


def i1UPanel(width: float = hp(8), thickness: float = _panelThickness):
    """Returns a 1U Tile (Intellijel size) panel with screw notches. Eurorack 1U tile width must be defined in hp().

    A thickness of 4mm minimum is recommended for solidity."""

    if width < hp(2):
        raise Warning("1U tiles (Intellijel size) should be at least 2hp wide")

    return eurorackPanel(
        width=width,
        height=_i1UHeight,
    )


def kosmoPanel(width: float = 25, thickness: float = _panelThickness):
    """Returns a Kosmo (Metric 5U) panel with screw notches. Kosmo widths must be multiples of 25.

    A thickness of 4mm minimum is recommended for solidity."""

    if width % 25 != 0:
        raise Warning("Kosmo panels should be multiples of 25mm")

    return panel(
        width=width,
        height=_kosmoHeight,
        thickness=thickness,
        screwNotchDistanceFromSide=_kosmoScrewNotchDistanceFromSide,
        screwNotchDistanceFromTop=_kosmoScrewNotchDistanceFromTop,
        screwNotchDistanceFromBottom=_kosmoScrewNotchDistanceFromBottom,
    )


#######################################################################
### LEDs


def led5mmHole(panel, x: float, y: float):
    return makeHole(panel, x, y, _5mmLedWithTolerance)


def led3mmHole(panel, x: float, y: float):
    return makeHole(panel, x, y, _3mmLedWithTolerance)


#######################################################################
### Buttons and switches


def arcadeButton30mmHole(panel, x: float, y: float):
    """Uses the dimensions for the Sanwa OBSF-30 snap-in button.

    Sanwas have a hair trigger and a concave surface.

    Dimensions work well with cheaper reproductions of it from Aliexpress.

    30mm is the size of action buttons commonly seen in arcade cabinets.
    Smaller buttons like the start button are 24mm.
    """
    return makeHole(panel, x, y, _sanwaOBSF30ButtonWithTolerance)


def arcadeButton24mmHole(panel, x: float, y: float):
    """Uses the dimensions for the Sanwa OBSF-24 snap-in button.

    Sanwas have a hair trigger and a concave surface.

    Dimensions work well with cheaper reproductions of it from Aliexpress.

    24mm is the size of utility buttons (like the start button) commonly seen in arcade cabinets.
    Actual action buttons are 30mm.
    """
    return makeHole(panel, x, y, _sanwaOBSF24ButtonWithTolerance)


def miniToggleSwitch(panel, x: float, y: float, orientation: str = "horizontal"):
    if orientation != "horizontal" and orientation != "vertical":
        raise Warning("Orientation must be either horizontal or vertical")
    if orientation == "horizontal":
        width = _miniToggleSwitchWidthWithTolerance
        length = _miniToggleSwitchLengthWithTolerance
    else:
        width = _miniToggleSwitchLengthWithTolerance
        length = _miniToggleSwitchWidthWithTolerance

    panel = makeHole(panel, x, y, _miniToggleSwitchDiameterWithTolerance)
    panel = (
        panel.faces(">Z")
        .vertices("<XY")
        .workplane(centerOption="CenterOfMass")
        .center(x, y)
        .rect(width, length)
        .cutBlind(-_miniToggleSwitchNotchDepth)
    )
    return panel


#######################################################################
### Potentiometers and rotary encoders


def potentiometerHole(panel, x: float, y: float):
    panel = makeHole(
        panel=panel, x=x, y=y, width=_potentiometerShaftDiameterWithTolerance
    )
    # Add the notches
    panel = (
        panel.faces(">Z")
        .vertices("<XY")
        .workplane(centerOption="CenterOfMass")
        .center(x, y)
        .pushPoints(
            [
                (_potentiometerNotchDistanceFromCenter, 0),
                (0, _potentiometerNotchDistanceFromCenter),
                (-_potentiometerNotchDistanceFromCenter, 0),
                (0, -_potentiometerNotchDistanceFromCenter),
            ]
        )
        .hole(_potentiometerNotchDiameter, _potentiometerNotchDepth)
    )
    return panel


#######################################################################
### Jacks


def bigJackHole(panel, x: float, y: float):
    panel = makeHole(panel=panel, x=x, y=y, width=_bigJackDiameterWithTolerance)
    panel = (
        panel.faces(">Z")
        .vertices("<XY")
        .workplane(centerOption="CenterOfMass")
        .center(x, y)
        .rect(_bigJackWidthWithTolerance, _bigJackLengthWithTolerance)
        .cutBlind(-_bigJackNotchDepth)
    )
    return panel


#######################################################################
### TEST CODE
# CQ-Editor can't autoreload modules, so placing all test code here
# is simpler than figuring out a workaround.

# panel = eurorackPanel(hp(8))

# panel = arcadeButton30mmHole(panel, 20, 20)
# panel = led5mmHole(panel, 10, 40)
# panel = led3mmHole(panel, 10, 48)
# panel = potentiometerHole(panel, 30, 45)
# panel = bigJackHole(panel, 20, 65)
# panel = miniToggleSwitch(panel, 8, 85)
# panel = miniToggleSwitch(panel, 20, 85, orientation="vertical")
# panel = miniToggleSwitch(panel, 32, 85, orientation="horizontal")
