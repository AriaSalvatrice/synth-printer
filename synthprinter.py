import cadquery as cq


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
        "panelWidth": 100.0,
        "panelHeight": 100.0,
        "panelThickness": 4.0,
        "hp": 5.08,  # 0.2 inches
        "khp": 25,  # Kosmo horizontal pitch
        # default depth of 1.02mm, to ensure that at 0.20mm print settings,
        # it hollows out 5 layers instead of 4. This helps making the notches
        # better at keeping things in place.
        "retainingNotchDepth": lambda config: config["panelThickness"] / 3.9,
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
        "eurorackWidthTolerance": lambda config: config["tolerance"],
        "i1UIJHeight": 39.65,  # Itellijel 1U - for our purposes, normal Euro but 1U tall
        "i1UIJWidthTolerance": lambda config: config["tolerance"],
        "kosmoHeight": 200.0,
        "kosmoWidthTolerance": 0,  # Kosmo needs no additional tolerance due to fitting HP rails
        ###########################################################
        ### Panel engravings
        ###########################################################
        # default depth of 1.02mm, to ensure that at 0.20mm print settings,
        # it engraves 5 layers instead of 4. This greatly helps with color
        # changes, with fewer layers, the first color might be a bit translucent.
        "panelEngravingDepth": lambda config: config["panelThickness"] / 3.9,
        ###########################################################
        ### Buttons and switches
        ###########################################################
        ###### Arcade
        # Sanwas have little clips making them require more tolerance
        # and the 24mm one require a thinner panel than the default
        # to snap in properly
        "arcade24mmButton": 24,
        "arcade24mmButtonWithTolerance": lambda config: config["arcade24mmButton"]
        + config["tolerance"] * 1.4,
        "arcade24mmButtonAdditionalClearanceDiameter": 27,
        "arcade24mmButtonAdditionalClearanceDepth": lambda config: config[
            "retainingNotchDepth"
        ],
        "arcade30mmButton": 30,
        "arcade30mmButtonWithTolerance": lambda config: config["arcade30mmButton"]
        + config["tolerance"] * 1.4,
        ###### Mini Toggle Switches
        # FIXME: It works but you can't add the washers on the back. Do they matter anyway? It seems sturdy enough without.
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
        # TODO: What are other common types?
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

        self.panelAdded = False  # We can only have one or horrible things happen

    #######################################################################
    #######################################################################
    #######################################################################
    #######################################################################
    #######################################################################

    #######################################################################
    ### Helpers
    #######################################################################

    def cutHole(self, x: float, y: float, diameter: float, depth: float = None):
        """Makes a circular hole, default depth is through the entire panel"""
        self.panel = (
            self.panel.faces(">Z")
            .vertices("<XY")
            .workplane(centerOption="CenterOfMass")
            .center(x, y)
            .hole(diameter, depth)
        )

    def previewCylinderOnBack(self, x: float, y: float, diameter: float, depth: float):
        """Adds a cylinder for preview on the back of the panel.
        It will be deeper by half the panel thickness."""
        self.preview = (
            self.preview.moveTo(
                -self.config["panelWidth"] / 2 + x,
                -self.config["panelHeight"] / 2 + y,
            )
            .circle(diameter / 2)
            .extrude(depth + self.config["panelThickness"] / 2)
        )

    def previewCylinderOnFront(self, x: float, y: float, diameter: float, depth: float):
        """Adds a cylinder for preview on the front of the panel.
        It will be deeper by half the panel thickness."""
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
        """Adds a box for preview on the back of the panel.
        It will be deeper by half the panel thickness."""
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
        """Adds a box for preview on the front of the panel.
        It will be deeper by half the panel thickness."""
        self.preview = (
            self.preview.moveTo(
                -self.config["panelWidth"] / 2 + x,
                -self.config["panelHeight"] / 2 + y,
            )
            .rect(width, height)
            .extrude(-depth - self.config["panelThickness"] / 2)
        )

    #######################################################################
    ### Panels
    #######################################################################

    def addPanel(
        self,
        width: float,
        height: float,
        screwNotches: str = "auto",
    ):
        """Adds a rectangular panel of arbitrary dimensions.
        You can only add one.

        Screw notches in the corners provide better tolerances than holes
        in a DIY printed system. If the panel is too small for four notches,
        there will be only two by default.

        :param screwNotches: options are "auto", "auto-tlbr", "auto-trbl", "auto-center", "none", "all", "tlbr", "trbl", "center"
        """

        if self.panelAdded == True:
            raise Warning("Only one panel can be added")
        else:
            self.panelAdded = True

        self.config["panelWidth"] = width
        self.config["panelHeight"] = height

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

        :param screwNotches: options are "auto", "auto-tlbr", "auto-trbl", "auto-center", "none", "all", "tlbr", "trbl", "center"
        """
        self.addPanel(
            self.config["hp"] * hp, self.config["eurorackHeight"], screwNotches
        )

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

        :param screwNotches: options are "auto", "auto-tlbr", "auto-trbl", "auto-center", "none", "all", "tlbr", "trbl", "center"
        """
        self.addPanel(self.config["hp"] * hp, self.config["i1UIJHeight"], screwNotches)

    def addKosmoPanel(
        self,
        khp: int,
        screwNotches="auto",
    ):
        """Adds a Kosmo panel with screw notches. khp argument is the amount of 25mm columns.

        Kosmo, also known as Metric 5U, is a format compatible with Eurorack
        popularized by Youtuber Sam Battle (Look Mum No Computer), that uses big jacks.
        It has a vertical pitch of 25mm (called khp in Synth Printer for simplicity)
        """
        # Kosmo panels are always large enough for four notches
        self.addPanel(
            self.config["hp"] * khp,
            self.config["kosmoHeight"],
            screwNotches=screwNotches,
        )

    #######################################################################
    ### Panel engravings
    #######################################################################

    # TODO: engraveLineTo that takes toX toY

    def engraveLine(
        self,
        fromX: float,
        fromY: float,
        angle: float,
        length: float,
        width: float,
        depth: float = 0,
    ):
        """Engraves a line on the front of the panel.

        If the depth parameter is omitted or 0, the default depth is used.

        Be sure to inspect both sides of the print to make sure there aren't
        any sections that are too thin!
        """
        if depth == 0:
            depth = self.config["panelEngravingDepth"]
        cutout = (
            cq.Workplane("XY")
            .lineTo(-width / 2, 0)
            .lineTo(-width / 2, -length)
            .lineTo(width / 2, -length)
            .lineTo(width / 2, 0)
            .close()
            .extrude(depth)
            .rotate((0, 0, 0), (0, 0, 1), angle)
            .translate(
                (
                    -self.config["panelWidth"] / 2 + fromX,
                    -self.config["panelHeight"] / 2 + fromY,
                    -self.config["panelThickness"] / 2,
                )
            )
        )
        self.panel = (
            self.panel.faces(">Z")
            .vertices("<XY")
            .workplane(centerOption="CenterOfMass")
            .cut(cutout)
        )

    #######################################################################
    ### Buttons and switches
    #######################################################################

    # TODO: Other types of common buttons and switches.... Not sure what's super common.

    def cutArcadeButton30mm(self, x: float, y: float):
        self.cutHole(x, y, self.config["arcade30mmButtonWithTolerance"])

    def previewArcadeButton30mm(self, x: float, y: float):
        self.previewCylinderOnFront(x, y, 32.3, 3.4)
        self.previewCylinderOnFront(x, y, 24, 7)
        self.previewCylinderOnBack(x, y, 24, 24.4)
        self.previewCylinderOnBack(x, y, 34.8, 6.5)

    def addArcadeButton30mm(self, x: float, y: float):
        """Should work with all major types of 30mm arcade buttons.

        30mm is the size of action buttons commonly seen in arcade cabinets.
        Smaller buttons like the start button are 24mm.

        Tested with the Sanwa OBSF-30 snap-in button.
        Sanwas have a hair trigger and a concave surface.

        Also tested with an unidentified screw-in type. The preview includes its retaining ring.

        Also tested with an unidentified Happ type.
        Happ buttons are concave are more commonly seen on American games.
        They are much deeper than on the preview.
        """
        self.cutArcadeButton30mm(x, y)
        self.previewArcadeButton30mm(x, y)

    # FIXME: untested footprint revision!!
    def cutArcadeButton24mm(self, x: float, y: float):
        self.cutHole(x, y, self.config["arcade24mmButtonWithTolerance"])
        self.cutHole(
            x,
            y,
            self.config["arcade24mmButtonAdditionalClearanceDiameter"],
            self.config["arcade24mmButtonAdditionalClearanceDepth"],
        )

    def previewArcadeButton24mm(self, x: float, y: float):
        self.previewCylinderOnFront(x, y, 27, 3.4)
        self.previewCylinderOnFront(x, y, 22, 7)
        self.previewCylinderOnBack(x, y, 24, 24.4)
        self.previewCylinderOnBack(x, y, 28, 6)

    def addArcadeButton24mm(self, x: float, y: float):
        """Should work with all major types of 24mm arcade buttons.

        24mm is the size of utility buttons (like the start button) commonly seen in arcade cabinets.
        Actual action buttons are 30mm.

        Uses the dimensions for the Sanwa OBSF-24 snap-in button.
        Sanwas have a hair trigger and a concave surface.

        Also tested with an unidentified screw-in type. The preview includes its retaining ring.
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

        This will fit the switches often sold as the "MTS-100" series by Aliexpress vendors that have only a single row of pins.

        It will not fit DPDT switches that have two rows of pins, those are bigger.

        :param orientation: "horizontal" (default) or "vertical".
        """

        # TODO: DPDT

        self.cutMiniToggleSwitch(x, y, orientation)
        self.previewMiniToggleSwitch(x, y, orientation)

    #######################################################################
    ### Potentiometers and rotary encoders
    #######################################################################

    def cutPotentiometer(
        self,
        x: float,
        y: float,
        notchOrientation: str = "all",
    ):
        self.cutHole(x, y, self.config["potentiometerHoleDiameterWithTolerance"])
        # Add the notches

        # default to "none" configuration
        points = []
        if notchOrientation == "top" or notchOrientation == "all":
            points.append((0, -self.config["potentiometerNotchDistanceFromCenter"]))
        if notchOrientation == "right" or notchOrientation == "all":
            points.append((self.config["potentiometerNotchDistanceFromCenter"], 0))
        if notchOrientation == "bottom" or notchOrientation == "all":
            points.append((0, self.config["potentiometerNotchDistanceFromCenter"]))
        if notchOrientation == "left" or notchOrientation == "all":
            points.append((-self.config["potentiometerNotchDistanceFromCenter"], 0))

        self.panel = (
            self.panel.faces(">Z")
            .vertices("<XY")
            .workplane(centerOption="CenterOfMass")
            .center(x, y)
            .pushPoints(points)
            .hole(
                self.config["potentiometerNotchDiameter"],
                self.config["potentiometerNotchDepth"],
            )
        )

    def previewPotentiometer(self, x: float, y: float, lugsOrientation: str = "all"):
        self.previewCylinderOnFront(x, y, 6, 21)
        self.previewCylinderOnFront(x, y, 9.6, 1.6)
        self.previewCylinderOnBack(x, y, 16, 8)
        if lugsOrientation == "all" or lugsOrientation == "bottom":
            self.previewBoxOnBack(x, y + 10, 15, 18, 2.4)
        if lugsOrientation == "top":
            self.previewBoxOnBack(x, y - 10, 15, 18, 2.4)
        if lugsOrientation == "left":
            self.previewBoxOnBack(x - 10, y, 18, 15, 2.4)
        if lugsOrientation == "right":
            self.previewBoxOnBack(x + 10, y, 18, 15, 2.4)

    def addPotentiometer(
        self,
        x: float,
        y: float,
        notchOrientation: str = "all",
        lugsOrientation: str = "all",
    ):
        """Fits most types of panel-mount potentiometers with a 6mm shaft.

        There will be four notches around the hole, allowing you to catch the
        retaining tab of the potentiometer in the most convenient orientation
        possible.

        This won't fit rotary encoders!

        If you want a knob, add it separately with addKnob()

        The orientation parameters are seen from the front, and are:
        "all", "none", "top", "left", "right", "bottom".

        The retaining notches aren't always on the same side, depending on the
        type of potentiometer! If in doubt, just leave it to "all" to add 4 notches.

        The preview size for the lugs doesn't account for the possibility of bending them,
        so it's probably safe to have potentiometers overlap a little.
        """
        self.cutPotentiometer(x, y, notchOrientation)
        self.previewPotentiometer(x, y, lugsOrientation)

    def previewKnob(self, x: float, y: float, diameter: float, depth: float):
        self.previewCylinderOnFront(x, y, diameter, depth + 5)

    def addKnob(self, x: float, y: float, diameter: float, depth: float):
        self.previewKnob(x, y, diameter, depth)

    # TODO: Rotary encoders

    #######################################################################
    ### Jacks
    #######################################################################

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

    # FIXME: MiniJacks are untested with Thonk ones, but work with my stock of generic ones
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

    #######################################################################
    ### Blinkenlichten
    #######################################################################

    def cutLed5mm(self, x: float, y: float):
        self.cutHole(x, y, self.config["5mmLedWithTolerance"])

    def previewLed5mm(self, x: float, y: float):
        self.previewCylinderOnFront(x, y, 4.7, 3)
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
        self.previewCylinderOnFront(x, y, 2.8, 1)
        self.previewBoxOnBack(x, y, 2.7, 1, 17)

    def addLed3mm(self, x: float, y: float):
        """Creates a hole for a 3mm LED protruding entirely from the hole.

        There is no mechanism to hold it in place, but hot glue will do the trick.
        """
        self.cutLed3mm(x, y)
        self.previewLed3mm(x, y)

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

        The defaults offered are for a non-existent model, for preview purposes.
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
    """Converts Eurorack hp to millimeters (1hp = 0.2in = 5.08mm).
    Useful to align things to the grid."""
    return hp * 5.08


def khp(khp: float):
    """Converts khp (Kosmo HP) to millimeters (1khp = 25mm).
    Useful to align things to the grid."""
    return khp * 25


def kcol(kcol: float):
    """Custom Kosmo grid system: each kcol is at the center of a 25mm section"""
    return (kcol - 1) * 25 + 12.5


def krow(krow: float):
    """Custom Kosmo grid system: each krow is 25mm, first starts 25mm from top"""
    return (krow) * 25


#######################################################################
### TEST CODE
#######################################################################
# CQ-Editor can't autoreload modules, so placing test code here
# is simpler than figuring out a workaround.
