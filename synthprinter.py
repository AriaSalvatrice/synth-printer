import cadquery as cq

# TODO: For Eurorack and 1U, shave off some width off the edges - without messing up the measurements
# TODO: Prevent adding multiple panels


class SynthPrinter:
    defaultConfig = {
        ###########################################################
        #
        # You can override any of those settings by passing them as
        # a parameter to the constructor - see examples.
        #
        # Preview objects have their sizes hardcoded to keep
        # the size of the config in check.
        #
        ###########################################################
        ### Common Dimensions
        ###########################################################
        "tolerance": 0.4,
        "panelWidth": lambda config: 20 + 120,  # <- How it's done
        "panelHeight": 100.0,
        "panelThickness": 4.0,
        "hp": 5.08,  # 0.2 inches
        "retainingNotchDepth": lambda config: config["panelThickness"] / 3,
        ###########################################################
        ### Visualization
        ###########################################################
        "panelColorRGBA": cq.Color(0, 0.7, 0.7, 0.9),
        "previewColorRGBA": cq.Color(0.7, 0.2, 0.2, 0.4),
        ###########################################################
        ### Screws
        ###########################################################
        ###### M3
        "m3Diameter": 3.0,
        "m3DiameterWithTolerance": lambda config: config["m3Diameter"]
        + config["tolerance"],
        "m3ScrewNotchWidth": lambda config: config["m3DiameterWithTolerance"] * 2.5,
        "m3ScrewNotchHeight": lambda config: config["m3DiameterWithTolerance"],
        "m3ScrewNotchDistanceFromTop": 3.0,
        "m3ScrewNotchDistanceFromBottom": 3.0,
        "m3ScrewNotchDistanceFromSide": lambda config: config["m3DiameterWithTolerance"]
        * 1.5,
        ###### M2
        "m2Diameter": 2.0,
        "m2DiameterWithTolerance": lambda config: config["m2Diameter"]
        + config["tolerance"] * 1.5,  # More expansion with small screws
        ###########################################################
        ### Panels
        ###########################################################
        "eurorackHeight": 128.5,  # Modules are smaller than the full 3U
        "eurorackWidthTolerance": lambda config: config[
            "tolerance"
        ],  # TODO: Test & implement
        "i1UIJHeight": 39.65,  # Itellijel 1U - for our purposes, normal Euro but 1U tall
        "i1UIJWidthTolerance": lambda config: config[
            "tolerance"
        ],  # TODO: Test & implement
        "kosmoHeight": 200.0,
        "kosmoWidthTolerance": 0,  # Kosmo needs no additional tolerance due to fitting HP rails
        ###########################################################
        ### Buttons and switches
        ###########################################################
        ###### Arcade
        # Sanwas have little clips making them require more tolerance
        # (or at least, my Aliexpress clones do - gotta check the real thing)
        "sanwaOBSF24Button": 24,  # TODO: UNTESTED!! Waiting to receive them by mail
        "sanwaOBSF24ButtonWithTolerance": lambda config: config["sanwaOBSF24Button"]
        + config["tolerance"] * 1.4,
        "sanwaOBSF30Button": 30,
        "sanwaOBSF30ButtonWithTolerance": lambda config: config["sanwaOBSF30Button"]
        + config["tolerance"] * 1.4,
        ###### Mini Toggle Switches
        "miniToggleSwitchWidth": 13.2,
        "miniToggleSwitchLength": 7.9,
        "miniToggleSwitchDiameter": 6,
        "miniToggleSwitchWidthWithTolerance": lambda config: config[
            "miniToggleSwitchWidth"
        ]
        + config["tolerance"],
        "miniToggleSwitchLengthWithTolerance": lambda config: config[
            "miniToggleSwitchLength"
        ]
        + config["tolerance"],
        "miniToggleSwitchDiameterWithTolerance": lambda config: config[
            "miniToggleSwitchDiameter"
        ]
        + config["tolerance"],
        "miniToggleSwitchNotchDepth": lambda config: config["retainingNotchDepth"],
        ###########################################################
        ### Potentiometers and rotary encoders
        ###########################################################
        ###### Pots
        "potentiometerHoleDiameter": 7,
        "potentiometerHoleDiameterWithTolerance": lambda config: config[
            "potentiometerHoleDiameter"
        ]
        + config["tolerance"],
        "potentiometerNotchDistanceFromCenter": 6.9,
        "potentiometerNotchDiameter": 3.9,
        "potentiometerNotchDepth": lambda config: config["panelThickness"] / 1.5,
        ###########################################################
        ### Jacks
        ###########################################################
        ###### Big
        "bigJackDiameter": 9,
        "bigJackDiameterWithTolerance": lambda config: config["bigJackDiameter"]
        + config["tolerance"],
        "bigJackWidth": 16,
        "bigJackHeight": lambda config: config["bigJackWidth"],
        "bigJackWidthWithTolerance": lambda config: config["bigJackWidth"]
        + config["tolerance"],
        "bigJackHeightWithTolerance": lambda config: config["bigJackHeight"]
        + config["tolerance"],
        "bigJackNotchDepth": lambda config: config["retainingNotchDepth"],
        ###### Mini
        # FIXME: Untested values!! Based on the drawing of the PJ398SM
        "miniJackDiameter": 6,
        "miniJackDiameterWithTolerance": lambda config: config["miniJackDiameter"]
        + config["tolerance"],
        "miniJackWidth": 9,
        "miniJackHeight": 9.5,
        "miniJackWidthWithTolerance": lambda config: config["miniJackWidth"]
        + config["tolerance"],
        "miniJackHeightWithTolerance": lambda config: config["miniJackHeight"]
        + config["tolerance"],
        "miniJackNotchDepth": lambda config: config["retainingNotchDepth"],
        ###########################################################
        ### Blinkenlichten
        ###########################################################
        "5mmLed": 4.9,
        "5mmLedWithTolerance": lambda config: config["5mmLed"] + config["tolerance"],
        "3mmLed": 2.9,
        "3mmLedWithTolerance": lambda config: config["3mmLed"]
        + config["tolerance"] * 1.5,
    }

    def __init__(self, **kwargs):
        self.config = self.defaultConfig.copy()

        # override defaults
        for key, value in kwargs.items():
            if key in self.config:
                self.config[key] = value

        # call lambdas
        for key, value in self.config.items():
            if callable(value):
                self.config[key] = value(self.config)

        self.panel = cq.Workplane("XY")
        self.preview = cq.Workplane("XY")

    #######################################################################
    #######################################################################
    #######################################################################
    #######################################################################
    #######################################################################

    #######################################################################
    ### Helpers
    #######################################################################

    def assemble(self):
        """Prepares the models for display in CQ Editor"""
        self.panelAssembly = cq.Assembly().add(
            self.panel, color=self.config["panelColorRGBA"]
        )
        self.previewAssembly = cq.Assembly().add(
            self.preview, color=self.config["previewColorRGBA"]
        )
        # FIXME: CQ-editor choke on exporting an assembly's STL!
        # TODO: calling CQ-editor's show_object doesn't work from this scope! Can it be solved?

    def cutHole(self, x: float, y: float, diameter: float):
        """Makes a circular hole through the entire panel"""
        self.panel = (
            self.panel.faces(">Z")
            .vertices("<XY")
            .workplane(centerOption="CenterOfMass")
            .center(x, y)
            .hole(diameter)
        )

    def previewCylinderOnBack(self, x: float, y: float, diameter: float, depth: float):
        self.preview = (
            self.preview.moveTo(
                -self.config["panelWidth"] / 2 + x,
                -self.config["panelHeight"] / 2 + y,
            )
            .circle(diameter / 2)
            .extrude(depth + self.config["panelThickness"] / 2)
        )

    def previewCylinderOnFront(self, x: float, y: float, diameter: float, depth: float):
        self.preview = (
            self.preview.moveTo(
                -self.config["panelWidth"] / 2 + x,
                -self.config["panelHeight"] / 2 + y,
            )
            .circle(diameter / 2)
            .extrude(-depth - self.config["panelThickness"] / 2)
        )

    def previewBoxOnBack(
        self, x: float, y: float, width: float, height: float, depth: float
    ):
        self.preview = (
            self.preview.moveTo(
                -self.config["panelWidth"] / 2 + x,
                -self.config["panelHeight"] / 2 + y,
            )
            .rect(width, height)
            .extrude(depth + self.config["panelThickness"] / 2)
        )

    def previewBoxOnFront(
        self, x: float, y: float, width: float, height: float, depth: float
    ):
        self.preview = (
            self.preview.moveTo(
                -self.config["panelWidth"] / 2 + x,
                -self.config["panelHeight"] / 2 + y,
            )
            .rect(width, height)
            .extrude(-depth - self.config["panelThickness"] / 2)
        )

    # #######################################################################
    # ### Panels
    # #######################################################################

    def addPanel(
        self,
        screwNotches: str = "auto",
    ):
        """Adds a rectangular panel of arbitrary dimensions.

        Screw notches in the corners provide better tolerances than holes
        in a DIY printed system. If the panel is too small for four notches,
        there will be only two by default.

        screwNotches options are:
        "auto", "auto-tlbr", "auto-trbl", "auto-center", "none", "all", "tlbr", "trbl", "center"
        """

        self.panel = self.panel.box(
            self.config["panelWidth"],
            self.config["panelHeight"],
            self.config["panelThickness"],
        )

        # Do we add screw slots?
        # default to "none" configuration
        screwNotchTopLeft = False
        screwNotchTopCenter = False
        screwNotchTopRight = False
        screwNotchBottomLeft = False
        screwNotchBottomCenter = False
        screwNotchBottomRight = False
        if (  # If too small for 4 notches
            self.config["m3ScrewNotchWidth"] * 2
            + (
                self.config["m3ScrewNotchDistanceFromSide"]
                - self.config["m3ScrewNotchWidth"] / 2
            )
            * 2
        ) > self.config["panelWidth"]:
            if screwNotches == "auto":
                screwNotches = "tlbr"
            if screwNotches == "auto-tlbr":
                screwNotches = "tlbr"
            if screwNotches == "auto-trbl":
                screwNotches = "trbl"
            if screwNotches == "auto-center":
                screwNotches = "center"
        else:  # Large enough for 4 notches
            if screwNotches == "auto":
                screwNotches = "all"
            if screwNotches == "auto-tlbr":
                screwNotches = "all"
            if screwNotches == "auto-trbl":
                screwNotches = "all"
            if screwNotches == "auto-center":
                screwNotches = "all"
        if screwNotches == "tlbr":
            screwNotchTopLeft = True
            screwNotchBottomRight = True
        if screwNotches == "trbl":
            screwNotchTopRight = True
            screwNotchBottomLeft = True
        if screwNotches == "center":
            screwNotchTopCenter = True
            screwNotchBottomCenter = True
        if screwNotches == "all":
            screwNotchTopLeft = True
            screwNotchTopRight = True
            screwNotchBottomLeft = True
            screwNotchBottomRight = True

        screwPoints = []
        if screwNotchTopLeft:
            screwPoints.append(
                (
                    self.config["m3ScrewNotchDistanceFromSide"],
                    self.config["panelHeight"]
                    - self.config["m3ScrewNotchDistanceFromTop"],
                )
            )
        if screwNotchTopCenter:
            screwPoints.append(
                (
                    self.config["panelWidth"] / 2,
                    self.config["panelHeight"]
                    - self.config["m3ScrewNotchDistanceFromTop"],
                )
            )
        if screwNotchTopRight:
            screwPoints.append(
                (
                    self.config["panelWidth"]
                    - self.config["m3ScrewNotchDistanceFromSide"],
                    self.config["panelHeight"]
                    - self.config["m3ScrewNotchDistanceFromTop"],
                )
            )
        if screwNotchBottomLeft:
            screwPoints.append(
                (
                    self.config["m3ScrewNotchDistanceFromSide"],
                    self.config["m3ScrewNotchDistanceFromBottom"],
                )
            )
        if screwNotchBottomCenter:
            screwPoints.append(
                (
                    self.config["panelWidth"] / 2,
                    self.config["m3ScrewNotchDistanceFromBottom"],
                )
            )
        if screwNotchBottomRight:
            screwPoints.append(
                (
                    self.config["panelWidth"]
                    - self.config["m3ScrewNotchDistanceFromSide"],
                    self.config["m3ScrewNotchDistanceFromBottom"],
                )
            )
        if screwPoints != []:
            self.panel = (
                self.panel.faces(">Z")
                .workplane()
                .center(-self.config["panelWidth"] / 2, -self.config["panelHeight"] / 2)
                .pushPoints(screwPoints)
                .slot2D(
                    self.config["m3ScrewNotchWidth"],
                    self.config["m3ScrewNotchHeight"],
                    0,
                )
                .cutThruAll()
            )

    def addEurorackPanel(
        self,
        hp: int,
        screwNotches="auto",
    ):
        """Adds a Eurorack panel with screw notches. Eurorack width is defined in hp().

        Eurorack sizes are generally an even number of hp, such as 4hp or 8hp.
        3hp and 5hp are the only odd number sizes commonly seen in commercial hardware.

        Screw notches in the corners provide better tolerances than holes
        in a DIY printed system. If the panel is too small for four notches,
        there will be only two by default.

        screwNotches options are:
        "auto", "auto-tlbr", "auto-trbl", "auto-center", "none", "all", "tlbr", "trbl", "center"
        """
        self.config["panelWidth"] = self.config["hp"] * hp
        self.config["panelHeight"] = self.config["eurorackHeight"]
        self.addPanel(screwNotches)

    def add1UIJPanel(
        self,
        hp: int,
        screwNotches="auto",
    ):
        """Adds a 1U Tile (Intellijel size) panel with screw notches. Eurorack width is defined in hp().

        Note that there are two incompatible 1U tile standards: Intellijel and PulpLogic.

        Screw notches in the corners provide better tolerances than holes
        in a DIY printed system. If the panel is too small for four notches,
        there will be only two by default.

        screwNotches options are:
        "auto", "auto-tlbr", "auto-trbl", "auto-center", "none", "all", "tlbr", "trbl", "center"
        """
        self.config["panelWidth"] = self.config["hp"] * hp
        self.config["panelHeight"] = self.config["i1UIJHeight"]
        self.addPanel(screwNotches)

    def addKosmoPanel(
        self,
        width: int,
        screwNotches="auto",
    ):
        """Adds a Kosmo panel with screw notches. Kosmo widths must be multiples of 25mm.

        Kosmo Panels, also known as Metric 5U, are a format compatible with Eurorack
        popularized by Youtuber Sam Battle (Look Mum No Computer), that uses big jacks.
        """
        # Kosmo panels are always large enough for four notches
        self.config["panelWidth"] = width
        self.config["panelHeight"] = self.config["kosmoHeight"]
        self.addPanel(screwNotches)

    # #######################################################################
    # ### Buttons and switches
    # #######################################################################

    def cutArcadeButton30mm(self, x: float, y: float):
        self.cutHole(x, y, self.config["sanwaOBSF30ButtonWithTolerance"])

    def previewArcadeButton30mm(self, x: float, y: float):
        self.previewCylinderOnFront(x, y, 32.3, 3.4)
        self.previewCylinderOnFront(x, y, 24, 7)
        self.previewCylinderOnBack(x, y, 24, 24.4)

    def addArcadeButton30mm(self, x: float, y: float):
        """Uses the dimensions for the Sanwa OBSF-30 snap-in button.

        Sanwas have a hair trigger and a concave surface.

        Dimensions work well with cheaper reproductions of it from Aliexpress.

        30mm is the size of action buttons commonly seen in arcade cabinets.
        Smaller buttons like the start button are 24mm.
        """
        self.cutArcadeButton30mm(x, y)
        self.previewArcadeButton30mm(x, y)

    def cutArcadeButton24mm(self, x: float, y: float):
        self.cutHole(x, y, self.config["sanwaOBSF24ButtonWithTolerance"])

    def previewArcadeButton24mm(self, x: float, y: float):
        # FIXME: Untested guessed values! I will only receive them in a while.
        self.previewCylinderOnFront(x, y, 27, 3.4)
        self.previewCylinderOnFront(x, y, 22, 7)
        self.previewCylinderOnBack(x, y, 24, 24.4)

    def addArcadeButton24mm(self, x: float, y: float):
        """Uses the dimensions for the Sanwa OBSF-24 snap-in button.

        Sanwas have a hair trigger and a concave surface.

        Dimensions work well with cheaper reproductions of it from Aliexpress.

        24mm is the size of utility buttons (like the start button) commonly seen in arcade cabinets.
        Actual action buttons are 30mm.
        """
        self.cutArcadeButton24mm(x, y)
        self.previewArcadeButton24mm(x, y)

    def cutMiniToggleSwitch(self, x: float, y: float, orientation: str = "horizontal"):
        if orientation == "horizontal":
            width = self.config["miniToggleSwitchWidthWithTolerance"]
            length = self.config["miniToggleSwitchLengthWithTolerance"]
        else:
            width = self.config["miniToggleSwitchLengthWithTolerance"]
            length = self.config["miniToggleSwitchWidthWithTolerance"]

        self.cutHole(x, y, self.config["miniToggleSwitchDiameterWithTolerance"])
        self.panel = (
            self.panel.faces(">Z")
            .vertices("<XY")
            .workplane(centerOption="CenterOfMass")
            .center(x, y)
            .rect(width, length)
            .cutBlind(-self.config["miniToggleSwitchNotchDepth"])
        )

    def previewMiniToggleSwitch(
        self, x: float, y: float, orientation: str = "horizontal"
    ):
        if orientation == "horizontal":
            width = self.config["miniToggleSwitchWidth"]
            length = self.config["miniToggleSwitchLength"]
        else:
            width = self.config["miniToggleSwitchLength"]
            length = self.config["miniToggleSwitchWidth"]
        self.previewBoxOnBack(x, y, width, length, 13.6)
        self.previewCylinderOnFront(x, y, self.config["miniToggleSwitchDiameter"], 19)

    def addMiniToggleSwitch(self, x: float, y: float, orientation: str = "horizontal"):
        """A mini toggle switch, with a retaining notch.

        You can swap the orientation to vertical using the orientation="vertical" parameter.

        This will fit the switches often sold as the "MTS-100" series by Aliexpress vendors.
        """

        self.cutMiniToggleSwitch(x, y, orientation)
        self.previewMiniToggleSwitch(x, y, orientation)

    # #######################################################################
    # ### Potentiometers and rotary encoders
    # #######################################################################

    # TODO: Let you configure the notches
    def cutPotentiometer(self, x: float, y: float):
        self.cutHole(x, y, self.config["potentiometerHoleDiameterWithTolerance"])
        # Add the notches
        self.panel = (
            self.panel.faces(">Z")
            .vertices("<XY")
            .workplane(centerOption="CenterOfMass")
            .center(x, y)
            .pushPoints(
                [
                    (self.config["potentiometerNotchDistanceFromCenter"], 0),
                    (0, self.config["potentiometerNotchDistanceFromCenter"]),
                    (-self.config["potentiometerNotchDistanceFromCenter"], 0),
                    (0, -self.config["potentiometerNotchDistanceFromCenter"]),
                ]
            )
            .hole(
                self.config["potentiometerNotchDiameter"],
                self.config["potentiometerNotchDepth"],
            )
        )

    def previewPotentiometer(self, x: float, y: float):
        self.previewCylinderOnFront(x, y, 6, 21)
        self.previewCylinderOnFront(x, y, 9.6, 1.6)
        self.previewCylinderOnBack(x, y, 16, 8)
        self.previewBoxOnBack(x, y + 8, 15, 14, 2.4)

    def addPotentiometer(self, x: float, y: float):
        """Fits most types of panel-mount potentiometers with a 6mm shaft.

        There will be four notches around the hole, allowing you to catch the
        retaining tab of the potentiometer in the most convenient orientation
        possible.

        This won't fit rotary encoders!
        """
        self.cutPotentiometer(x, y)
        self.previewPotentiometer(x, y)

    def previewKnob(self, x: float, y: float, diameter: float, depth: float):
        self.previewCylinderOnFront(x, y, diameter, depth + 5)

    def addKnob(self, x: float, y: float, diameter: float, depth: float):
        self.previewKnob(x, y, diameter, depth)

    # TODO: Rotary encoders

    # #######################################################################
    # ### Jacks
    # #######################################################################

    def cutBigJack(self, x: float, y: float):
        self.cutHole(x, y, self.config["bigJackDiameterWithTolerance"])
        self.panel = (
            self.panel.faces(">Z")
            .vertices("<XY")
            .workplane(centerOption="CenterOfMass")
            .center(x, y)
            .rect(
                self.config["bigJackWidthWithTolerance"],
                self.config["bigJackHeightWithTolerance"],
            )
            .cutBlind(-self.config["bigJackNotchDepth"])
        )

    def previewBigJack(self, x: float, y: float):
        self.previewCylinderOnFront(x, y, 8.5, 7)
        self.previewCylinderOnFront(x, y, 12.6, 2.2)
        self.previewBoxOnBack(x, y, 16, 16, 27)

    def addBigJack(self, x: float, y: float):
        """This fits panel mount 6.35mm jacks with a rectangular base, as used
        in Kosmo builds.

        There is a retaining notch the size of the base to help keep it in place.
        """
        self.cutBigJack(x, y)
        self.previewBigJack(x, y)

    # FIXME: MiniJacks are 100% untested
    def cutMiniJack(self, x: float, y: float):
        self.cutHole(x, y, self.config["miniJackDiameterWithTolerance"])
        self.panel = (
            self.panel.faces(">Z")
            .vertices("<XY")
            .workplane(centerOption="CenterOfMass")
            .center(x, y)
            .rect(
                self.config["miniJackWidthWithTolerance"],
                self.config["miniJackHeightWithTolerance"],
            )
            .cutBlind(-self.config["miniJackNotchDepth"])
        )

    def previewMiniJack(self, x: float, y: float):
        self.previewCylinderOnFront(x, y, 6, 5.5)
        self.previewCylinderOnFront(x, y, 8, 2.2)
        self.previewBoxOnBack(x, y, 9, 10.5, 12.5)

    def addMiniJack(self, x: float, y: float):
        """This fits 3.5mm PJ398SM "Thonkiconn" 3.5mm jacks. UNTESTED FOOTPRINT!

        There is a retaining notch the size of the base to help keep it in place.
        """
        self.cutMiniJack(x, y)
        self.previewMiniJack(x, y)

    # #######################################################################
    # ### Blinkenlichten
    # #######################################################################

    def cutLed5mm(self, x: float, y: float):
        self.cutHole(x, y, self.config["5mmLedWithTolerance"])

    def previewLed5mm(self, x: float, y: float):
        self.previewCylinderOnFront(x, y, 4.7, 3)  # FIXME: Check value
        self.previewBoxOnBack(x, y, 4, 1, 17)

    def addLed5mm(self, x: float, y: float):
        """Creates a hole for a 5mm LED protruding entirely from the hole.

        There is no mechanism to hold it in place, but hot glue will do the trick.
        """
        self.cutLed5mm(x, y)
        self.previewLed5mm(x, y)

    def cutLed3mm(self, x: float, y: float):
        self.cutHole(x, y, self.config["3mmLedWithTolerance"])

    def previewLed3mm(self, x: float, y: float):
        self.previewCylinderOnFront(x, y, 2.8, 1)  # FIXME: Check value
        self.previewBoxOnBack(x, y, 2.7, 1, 17)

    def addLed3mm(self, x: float, y: float):
        """Creates a hole for a 3mm LED protruding entirely from the hole.

        There is no mechanism to hold it in place, but hot glue will do the trick.
        """
        self.cutLed3mm(x, y)
        self.previewLed3mm(x, y)

    # TODO: How to handle footprints without a matching preview?
    def cutDisplayWindow(
        self,
        x: float,
        y: float,
        windowWidth: float = 30,
        windowHeight: float = 15,
        windowVerticalOffset: float = -5,
        windowHorizontalOffset: float = 0,
        screwsHorizontalDistance: float = 40,
        screwsVerticalDistance: float = 40,
    ):
        # FIXME: This is the nastiest way possible to do a fillet
        # but the only one i could figure out
        cutout = (
            cq.Workplane("XY")
            .box(
                windowWidth + self.config["panelThickness"],
                windowHeight + self.config["panelThickness"],
                self.config["panelThickness"],
            )
            .edges(">Z")
            .fillet(self.config["panelThickness"] * 0.99)
            .translate(
                (
                    -self.config["panelWidth"] / 2 + x + windowHorizontalOffset,
                    -self.config["panelHeight"] / 2 + y + windowVerticalOffset,
                    0,
                )
            )
        )
        self.panel = (
            self.panel.faces(">Z")
            .vertices("<XY")
            .workplane(centerOption="CenterOfMass")
            .cut(cutout)
        )

        # Next, the actual cutout
        self.panel = (
            self.panel.faces(">Z")
            .vertices("<XY")
            .workplane(centerOption="CenterOfMass")
            .center(x + windowHorizontalOffset, y + windowVerticalOffset)
            .rect(windowWidth, windowHeight)
            .cutThruAll()
        )

        # Now, the screws
        self.panel = (
            self.panel.faces(">Z")
            .vertices("<XY")
            .workplane(centerOption="CenterOfMass")
            .center(x, y)
            .rect(
                screwsHorizontalDistance, screwsVerticalDistance, forConstruction=True
            )
            .vertices()
            .circle(self.config["m2DiameterWithTolerance"] / 2)
            .cutThruAll()
        )

    def addDisplayWindow(
        self,
        x: float,
        y: float,
        windowWidth: float = 30,
        windowHeight: float = 15,
        windowVerticalOffset: float = -5,
        windowHorizontalOffset: float = 0,
        screwsHorizontalDistance: float = 40,
        screwsVerticalDistance: float = 40,
    ):
        """Creates a window for a rectangular display mounted with four screws in the corner.

        Every single display available has different dimensions, especially the cheapo OLEDs
        from Aliexpress. Even when the display size is the same, various boards differ by
        a few millimeters.

        The defaults offered here are for a non-existent model, for preview purposes.
        Provide your own measurements instead!
        """
        self.cutDisplayWindow(
            x,
            y,
            windowWidth,
            windowHeight,
            windowVerticalOffset,
            windowHorizontalOffset,
            screwsHorizontalDistance,
            screwsVerticalDistance,
        )

    #######################################################################
    #######################################################################
    #######################################################################
    #######################################################################
    #######################################################################


#######################################################################
### Helpers
#######################################################################


def hp(hp: float):
    return hp * 5.08


#######################################################################
### TEST CODE
#######################################################################
# CQ-Editor can't autoreload modules, so placing test code here
# is simpler than figuring out a workaround.


# Override any setting from the defaultConfig
# sp = SynthPrinter(
#     tolerance=0.4,
#     panelColorRGBA=cq.Color(0.5, 0.9, 0.5, 0.9),
#     miniToggleSwitchDiameter=6,
# )

# sp.addEurorackPanel(8)  # HP

# sp.addLed5mm(hp(1), 10)
# sp.addMiniToggleSwitch(hp(1), 20, "vertical")
# sp.addLed3mm(hp(1), 30)
# sp.addMiniToggleSwitch(hp(1), 40, "vertical")
# sp.addMiniToggleSwitch(hp(4), 40)

# sp.addPotentiometer(hp(4), 20)
# sp.addKnob(hp(4), 20, 12, 16)

# sp.addLed5mm(32, 10)
# sp.addLed5mm(37, 15)
# sp.addLed5mm(32, 20)
# sp.addLed5mm(37, 25)
# sp.addLed5mm(32, 30)
# sp.addLed5mm(37, 35)
# sp.addLed5mm(32, 40)
# sp.addLed5mm(37, 45)

# sp.addArcadeButton24mm(hp(4), 60)
# sp.addMiniJack(hp(1) + 1.5, 83)
# sp.addBigJack(hp(4), 83)
# sp.addMiniJack(hp(7) - 1.5, 83)
# sp.addArcadeButton30mm(hp(4), 108)

# show_object(sp.panel, name="panel", options={"alpha": 0.1, "color": (0, 180, 230)})
# show_object(sp.preview, name="preview", options={"alpha": 0.8, "color": (100, 30, 30)})
