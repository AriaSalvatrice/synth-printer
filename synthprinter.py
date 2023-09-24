import cadquery as cq


class SynthPrinter:
    """Each SynthPrinter object corresponds to a panel. You must add one, and
    only one panel, before performing operations on it.

    Once you're done placing elements, you must call `render()` before
    exporting your work, to post-process things correctly.
    Elements will be aligned and oriented wrong if you skip this call.

    The naming convention of methods is as follows:

    - `addX()`: calls methods such as `cutX()`, `previewX()`, etc, operating on multiple
    layers. Skips drawing to disabled layers for performance, so disable unnecessary
    layers in the constructor while making your layout.
    In most cases, you want to call those methods instead of making the individual calls
    bundled in the `addX()` methods.
    - `cutX()`: makes a hole for X on the **panel** layer
    - `markX()`: draws marks for X on the **drillTemplate** layer.
    *Exporting a drill template is a WIP, it still takes a bit of tinkering to
    make the PDF the proper size.*
    - `previewX()`: draws boxes and cylinders to preview the size of footprints
    on the **preview** layer
    - `embossX()`: creates an element on the **emboss** layer. You can only 3D print
    quality embossings if you orient your panel with the back as the first layer.
    *Not implemented yet*
    - `engraveX()`: carves an engraving that does not cut all the way through the
    **panel** layer
    - `supportX()`: creates an element on the **supports** layer, used to strenghten
    panels and hold in place PCBs. You can only 3D print supports if you orient
    your panel with the front as the first layer.

    Be sure to take a look at the bundled examples!
    """

    defaultConfig = {
        ###########################################################
        # You can override any of these settings from the defaultConfig by
        # passing them as a parameter to the constructor.
        #
        # Preview objects have their sizes hardcoded to keep
        # the size of this config in check.
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
        ### Visualization in CQ Editor
        ###########################################################
        "panelRender": True,
        "supportsRender": True,
        "embossRender": True,
        "previewRender": True,  # Disable to improve render performance
        "drillTemplateRender": False,
        "panelShowOptions": {"alpha": 0.2, "color": (0, 180, 230)},
        "supportsShowOptions": {"alpha": 0.1, "color": (180, 230, 0)},
        "embossShowOptions": {"alpha": 0.2, "color": (50, 180, 230)},
        "previewShowOptions": {"alpha": 0.65, "color": (100, 30, 30)},
        "drillTemplateShowOptions": {"alpha": 0.1, "color": (20, 20, 20)},
        ###########################################################
        ### Screws
        ###########################################################
        ###### M3
        "m3Diameter": 3.0,
        "m3DiameterWithTolerance": lambda config: config["m3Diameter"]
        + config["tolerance"],
        "m3screwSlotWidth": lambda config: config["m3DiameterWithTolerance"] * 2.5,
        "m3screwSlotHeight": lambda config: config["m3DiameterWithTolerance"],
        "m3screwSlotDistanceFromTop": 3.0,
        "m3screwSlotDistanceFromBottom": 3.0,
        "m3screwSlotDistanceFromSide": lambda config: config["m3DiameterWithTolerance"]
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
        "1UIJHeight": 39.65,  # Itellijel 1U - for our purposes, normal Euro but 1U tall
        "1UIJWidthTolerance": lambda config: config["tolerance"],
        "kosmoHeight": 200.0,
        "kosmoWidthTolerance": 0,  # Kosmo needs no additional tolerance as HP rails are larger
        "panelWidthTolerance": 0,  # Set when adding the panel
        ###########################################################
        ### Panel engravings
        ###########################################################
        "panelEngravingDepth": lambda config: config["panelThickness"] / 3,
        ###########################################################
        ### Rails & Cradles
        ###########################################################
        "railsFrontRecess": 2,  # 1.6 PCB + junk leftover from supports
        "railsSupportDepthBack": 4.0,  # How much to protrude behind panel, not full depth
        "railsHeight": 8,
        "railsScrewDiameter": lambda config: config[
            "m3Diameter"
        ],  # Not adding the tolerance holds better
        "cradleTolerance": lambda config: config["tolerance"],
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
        ###### PBS-110 7mm Momentary Pushbuttons
        "momentaryPushbutton7mmDiameter": 7.2,
        "momentaryPushbutton7mmDiameterWithTolerance": lambda config: config[
            "momentaryPushbutton7mmDiameter"
        ]
        + config["tolerance"],
        "momentaryPushbutton7mmNotchDiameter": 9.5,
        "momentaryPushbutton7mmNotchDiameterWithTolerance": lambda config: config[
            "momentaryPushbutton7mmNotchDiameter"
        ]
        + config["tolerance"],
        "momentaryPushbutton7mmNotchDepth": lambda config: config["panelThickness"] / 2,
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
        "rotaryEncoderWidth": 14,
        "rotaryEncoderWidthWithTolerance": lambda config: config["rotaryEncoderWidth"]
        + config["tolerance"],
        "rotaryEncoderHeight": 12,
        "rotaryEncoderHeightWithTolerance": lambda config: config["rotaryEncoderHeight"]
        + config["tolerance"],
        "rotaryEncoderNotchDepth": lambda config: config["retainingNotchDepth"],
        "sliderNotchDepth": lambda config: config["retainingNotchDepth"],
        ###########################################################
        ### Jacks & Sockets
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
        "miniJackDiameter": 6,
        "miniJackDiameterWithTolerance": lambda config: config["miniJackDiameter"]
        + config["tolerance"],
        "miniJackSize": 9.5,
        "miniJackSizeWithTolerance": lambda config: config["miniJackSize"]
        + config["tolerance"] * 2,
        "miniJackNotchDepth": lambda config: config["retainingNotchDepth"],
        ###### MIDI
        "midiSocketDiameter": 15,
        "midiSocketDiameterWithTolerance": lambda config: config["midiSocketDiameter"]
        + config["tolerance"] * 2,
        "midiSocketScrewDistance": 21.6,
        "midiSocketScrewDiameterWithTolerance": lambda config: config[
            "m3DiameterWithTolerance"
        ],
        ###########################################################
        ### Blinkenlichten
        ###########################################################
        "5mmLed": 4.9,
        "5mmLedWithTolerance": lambda config: config["5mmLed"] + config["tolerance"],
        "3mmLed": 2.9,
        "3mmLedWithTolerance": lambda config: config["3mmLed"]
        + config["tolerance"] * 1.5,
        "RectangularLedWidth": 2,
        "RectangularLedWidthWithTolerance": lambda config: config["RectangularLedWidth"]
        + config["tolerance"],
        "RectangularLedHeight": 5,
        "RectangularLedHeightWithTolerance": lambda config: config[
            "RectangularLedHeight"
        ]
        + config["tolerance"],
        ###########################################################
        ### Drill Template
        ###########################################################
        "DrillTemplateMarkLength": 10,
        "DrillTemplateMarkThickness": 0.2,
        "DrillTemplateDistance": -80,
    }
    """
    You can override any of the defaultConfig settings by passing them as a
    parameter to the constructor. Look at the code for the full list of
    settings. Some are dynamically calculated from other settings, 
    in particular, the tolerances of most elements are expressed as a
    multiplier of the main tolerance value.

    For example, to replace the main tolerance value of 0.4mm, create a
    new object as follows:

        sp = SynthPrinter(
            tolerance=0.6,
        )

    defaultConfig values are mostly dimensions that have been tested to
    work well with 3D printing. You are encouraged to try out the defaults 
    first. But with a different process than FDM 3D printing, you will want to
    make your own configuration profile."""

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

        # Create layers
        self.panel = cq.Workplane("XY")
        self.preview = cq.Workplane("XY")
        self.emboss = cq.Workplane("XY")
        self.supports = cq.Workplane("XY")
        self.drillTemplate = cq.Workplane("XY")

        self.panelAdded = False  # We can only have one or horrible things happen

    #######################################################################
    #######################################################################
    #######################################################################
    #######################################################################
    #######################################################################

    #######################################################################
    ### Rendering & Export
    #######################################################################

    def render(self, show_object=False):
        """You must call this before displaying or exporting your panel
        to post-process it properly.

        If you give it the show_object function from Cq Editor as an
        argument, it will also display the object. When using Synth Printer
        from a different environment, just call without any argument.
        """
        # Shave off the sides of the panel if needed
        self.cutPanelWidthTolerance()
        # Move the supports where they belong
        self.supports = self.supports.translate(
            (0, 0, self.config["panelThickness"] / 2)
        )
        # Move the drill template above the panel
        self.drillTemplate = self.drillTemplate.translate(
            (0, 0, self.config["DrillTemplateDistance"])
        )
        # Rotate the layers for viewing
        self.panel = self.panel.rotate((0, 0, 0), (1, 0, 0), 180)
        self.preview = self.preview.rotate((0, 0, 0), (1, 0, 0), 180)
        self.emboss = self.emboss.rotate((0, 0, 0), (1, 0, 0), 180)
        self.supports = self.supports.rotate((0, 0, 0), (1, 0, 0), 180)
        self.drillTemplate = self.drillTemplate.rotate((0, 0, 0), (1, 0, 0), 180)
        # Display the layers if we're in CQ Editor
        if show_object and self.config["panelRender"]:
            show_object(
                self.panel,
                name="panel",
                options=self.config["panelShowOptions"],
            )
        if show_object and self.config["supportsRender"]:
            show_object(
                self.supports,
                name="supports",
                options=self.config["supportsShowOptions"],
            )
        if show_object and self.config["embossRender"]:
            show_object(
                self.emboss,
                name="emboss",
                options=self.config["embossShowOptions"],
            )
        if show_object and self.config["previewRender"]:
            show_object(
                self.preview,
                name="preview",
                options=self.config["previewShowOptions"],
            )
        if show_object and self.config["drillTemplateRender"]:
            show_object(
                self.drillTemplate,
                name="drillTemplate",
                options=self.config["drillTemplateShowOptions"],
            )

    def exportDrillTemplate(self, filename: str = "DrillTemplate.svg"):
        """Exports the drill template as a SVG file.

        Before you print it, crop and scale it up or down in image editing
        software to match the size of one side!

        TODO: Make it the perfect size out of the box.

        You must activate the layer in the constructor first! Otherwise,
        drill marks are not rendered, for performance."""
        cq.exporters.export(
            self.drillTemplate,
            filename,
            opt={
                "width": 2000,
                "height": 2000,
                "marginLeft": 0,
                "marginTop": 0,
                "showAxes": False,
                "projectionDir": (0.0, 0.0, 1.0),
                "strokeWidth": 0.25,
                "strokeColor": (255, 0, 0),
                "hiddenColor": (0, 0, 255),
                "showHidden": False,
            },
        )

    #######################################################################
    #######################################################################
    #######################################################################
    #######################################################################
    #######################################################################

    #######################################################################
    ### Basic operations
    #######################################################################

    def cutHole(self, x: float, y: float, diameter: float, depth: float = None):
        """Makes a circular hole, default depth is through the entire panel

        x, y define the center."""
        self.panel = (
            self.panel.faces(">Z")
            .vertices("<XY")
            .workplane(centerOption="CenterOfMass")
            .center(x, y)
            .hole(diameter, depth)
        )

    def cutRect(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        depth: float = 0,
        centered: bool = True,
    ):
        """Cuts a rectangular shape through the panel.

        x, y define the center

        `depth = 0` cuts through all.
        """

        if depth == 0:
            depth = self.config["panelThickness"]

        cutout = cq.Workplane("XY").box(width, height, depth)

        if centered:
            cutout = cutout.translate(
                (
                    -self.config["panelWidth"] / 2 + x,
                    -self.config["panelHeight"] / 2 + y,
                    0,
                )
            )
        else:
            cutout = cutout.translate(
                (
                    -self.config["panelWidth"] / 2 + x + width / 2,
                    -self.config["panelHeight"] / 2 + y + height / 2,
                    0,
                )
            )

        self.panel = (
            self.panel.faces(">Z")
            .vertices("<XY")
            .workplane(centerOption="CenterOfMass")
            .cut(cutout)
        )

    # TODO: Top-left support!
    def previewCylinderOnBack(self, x: float, y: float, diameter: float, depth: float):
        """Adds a cylinder for preview on the back of the panel.
        It will be deeper by half the panel thickness.

        x, y define the center."""
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
        It will be deeper by half the panel thickness.

        x, y define the center."""
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
        It will be deeper by half the panel thickness.

        x, y define the center."""
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
        It will be deeper by half the panel thickness.

        x, y define the center.
        """
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
        screwSlots: str = "auto",
    ):
        """Adds a rectangular panel of arbitrary dimensions.
        You can only add one.

        Screw slots in the corners provide better tolerances than holes
        in a DIY printed system. If the panel is too small for four slots,
        there will be only two by default.


        TODO: Add Slots to the drill template


        screwSlots: options are "auto", "auto-tlbr", "auto-trbl", "auto-center", "none", "all", "tlbr", "trbl", "center"
        """

        if self.panelAdded == True:
            raise Warning("Only one panel can be added")
        else:
            self.panelAdded = True

        self.config["panelWidth"] = width
        self.config["panelHeight"] = height

        # Make the main panel shape
        self.panel = self.panel.box(
            self.config["panelWidth"],
            self.config["panelHeight"],
            self.config["panelThickness"],
        )

        # Initialize the drill template
        self.markOutline()

        # Do we add screw slots?
        # default to "none" configuration
        screwSlotTopLeft = False
        screwSlotTopCenter = False
        screwSlotTopRight = False
        screwSlotBottomLeft = False
        screwSlotBottomCenter = False
        screwSlotBottomRight = False
        if (  # If too small for 4 slots
            self.config["m3screwSlotWidth"] * 2
            + (
                self.config["m3screwSlotDistanceFromSide"]
                - self.config["m3screwSlotWidth"] / 2
            )
            * 2
        ) > self.config["panelWidth"]:
            if screwSlots == "auto":
                screwSlots = "tlbr"
            if screwSlots == "auto-tlbr":
                screwSlots = "tlbr"
            if screwSlots == "auto-trbl":
                screwSlots = "trbl"
            if screwSlots == "auto-center":
                screwSlots = "center"
        else:  # Large enough for 4 slots
            if screwSlots == "auto":
                screwSlots = "all"
            if screwSlots == "auto-tlbr":
                screwSlots = "all"
            if screwSlots == "auto-trbl":
                screwSlots = "all"
            if screwSlots == "auto-center":
                screwSlots = "all"
        if screwSlots == "tlbr":
            screwSlotTopLeft = True
            screwSlotBottomRight = True
        if screwSlots == "trbl":
            screwSlotTopRight = True
            screwSlotBottomLeft = True
        if screwSlots == "center":
            screwSlotTopCenter = True
            screwSlotBottomCenter = True
        if screwSlots == "all":
            screwSlotTopLeft = True
            screwSlotTopRight = True
            screwSlotBottomLeft = True
            screwSlotBottomRight = True

        screwPoints = []
        if screwSlotTopLeft:
            screwPoints.append(
                (
                    self.config["m3screwSlotDistanceFromSide"],
                    self.config["panelHeight"]
                    - self.config["m3screwSlotDistanceFromTop"],
                )
            )
        if screwSlotTopCenter:
            screwPoints.append(
                (
                    self.config["panelWidth"] / 2,
                    self.config["panelHeight"]
                    - self.config["m3screwSlotDistanceFromTop"],
                )
            )
        if screwSlotTopRight:
            screwPoints.append(
                (
                    self.config["panelWidth"]
                    - self.config["m3screwSlotDistanceFromSide"],
                    self.config["panelHeight"]
                    - self.config["m3screwSlotDistanceFromTop"],
                )
            )
        if screwSlotBottomLeft:
            screwPoints.append(
                (
                    self.config["m3screwSlotDistanceFromSide"],
                    self.config["m3screwSlotDistanceFromBottom"],
                )
            )
        if screwSlotBottomCenter:
            screwPoints.append(
                (
                    self.config["panelWidth"] / 2,
                    self.config["m3screwSlotDistanceFromBottom"],
                )
            )
        if screwSlotBottomRight:
            screwPoints.append(
                (
                    self.config["panelWidth"]
                    - self.config["m3screwSlotDistanceFromSide"],
                    self.config["m3screwSlotDistanceFromBottom"],
                )
            )
        if screwPoints != []:
            self.panel = (
                self.panel.faces(">Z")
                .workplane()
                .center(-self.config["panelWidth"] / 2, -self.config["panelHeight"] / 2)
                .pushPoints(screwPoints)
                .slot2D(
                    self.config["m3screwSlotWidth"],
                    self.config["m3screwSlotHeight"],
                    0,
                )
                .cutThruAll()
            )

    def addEurorackPanel(
        self,
        hp: int,
        screwSlots="auto",
    ):
        """Adds a Eurorack panel with screw slots. Eurorack width is defined in hp().

        Eurorack sizes are generally an even number of hp, such as 4hp or 8hp.
        3hp and 5hp are the only odd number sizes commonly seen in commercial hardware.

        Screw slots in the corners provide better tolerances than holes
        in a DIY printed system. If the panel is too small for four slots,
        there will be only two by default.

        screwSlots: options are "auto", "auto-tlbr", "auto-trbl", "auto-center", "none", "all", "tlbr", "trbl", "center"
        """
        self.config["panelWidthTolerance"] = self.config["eurorackWidthTolerance"]
        self.addPanel(self.config["hp"] * hp, self.config["eurorackHeight"], screwSlots)

    def add1UIJPanel(
        self,
        hp: int,
        screwSlots="auto",
    ):
        """Adds a 1U Tile (Intellijel size) panel with screw slots. Eurorack width is defined in hp().

        Note that there are two incompatible 1U tile standards: Intellijel and PulpLogic.

        Screw slots in the corners provide better tolerances than holes
        in a DIY printed system. If the panel is too small for four slots,
        there will be only two by default.

        screwSlots: options are "auto", "auto-tlbr", "auto-trbl", "auto-center", "none", "all", "tlbr", "trbl", "center"
        """
        self.config["panelWidthTolerance"] = self.config["1UIJWidthTolerance"]
        self.addPanel(self.config["hp"] * hp, self.config["1UIJHeight"], screwSlots)

    def addKosmoPanel(
        self,
        khp: int,
        screwSlots="auto",
    ):
        """Adds a Kosmo panel with screw slots. khp argument is the amount of 25mm columns.

        Kosmo, also known as Metric 5U, is a format compatible with Eurorack
        popularized by Youtuber Sam Battle (Look Mum No Computer), that uses big jacks.
        It has a horizontal pitch of 25mm (called khp in Synth Printer for simplicity)

        Screw slots in the corners provide better tolerances than holes
        in a DIY printed system. Kosmo panels are always large enough for four slots,
        but you can explicitly set a different configuration of slots.

        screwSlots: options are "auto", "auto-tlbr", "auto-trbl", "auto-center", "none", "all", "tlbr", "trbl", "center"
        """
        self.config["panelWidthTolerance"] = self.config["kosmoWidthTolerance"]
        self.addPanel(
            self.config["khp"] * khp,
            self.config["kosmoHeight"],
            screwSlots=screwSlots,
        )

    def cutPanelWidthTolerance(self):
        """Automatically called during `render()` for Eurorack and 1UIJ:
        makes the panel a bit smaller than its nominal size laterally to account
        for thermal expansion and misaligned neighboring panels.
        Kosmo panels are naturally a bit smaller than the hp grid (they are on a
        25mm grid, while hp are on a 5.08mm grid), as a result, they don't need
        this shave.
        """
        # FIXME: Trial and error values that make no sense.
        # Something's broken elsewhere!
        # FIXME: Test print Euro / IJ: Do the tolerances provide enough extrusions?
        if self.config["panelWidthTolerance"] == 0:
            return
        self.cutRect(
            0,
            0,
            self.config["panelWidthTolerance"],
            self.config["panelHeight"] * 2,
            False,
        )

        self.cutRect(
            self.config["panelWidth"] - self.config["panelWidthTolerance"] / 2,
            0,
            self.config["panelWidthTolerance"],
            self.config["panelHeight"] * 2,
            False,
        )

    #######################################################################
    ### Panel engravings
    #######################################################################

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
        if not self.config["panelRender"]:
            return
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
    ### Rails
    #######################################################################

    # All this stuff is some real spaghetti.
    # It deserves a complete rewrite, and could take 1/5th the code.
    # But it works, so rewrite it yourself if you care.
    # Otherwise, don't bother me about it.

    def cutRail(
        self,
        x: float,
        y: float,
        hpWidth: int,
        centered: bool = True,
        orientation: str = "horizontal",
    ):
        """Make a hole for a hp rail. The rail is added to the supports layer,
        not the panel layer."""
        if not self.config["panelRender"]:
            return
        width = hp(hpWidth) + self.config["cradleTolerance"] * 2
        height = self.config["railsHeight"] + self.config["cradleTolerance"] * 2
        if orientation == "vertical":
            width, height = height, width
        if centered:
            self.cutRect(x, y, width, height, 0, centered)
        else:
            self.cutRect(
                x - self.config["cradleTolerance"],
                y - self.config["cradleTolerance"],
                width,
                height,
                0,
                centered,
            )

    def supportRail(
        self,
        _x: float,
        _y: float,
        hpWidth: int,
        centered: bool = True,
        orientation: str = "horizontal",
    ):
        """Adds a hp rail to the support layer. Requires a hole from cutRail()."""
        if not self.config["supportsRender"]:
            return
        width = hp(hpWidth) + self.config["cradleTolerance"] * 2
        height = self.config["railsHeight"] + self.config["cradleTolerance"] * 2
        if orientation != "horizontal":
            width, height = height, width

        if centered:
            x = -self.config["panelWidth"] / 2 + _x
            y = -self.config["panelHeight"] / 2 + _y
        else:
            x = (
                -self.config["panelWidth"] / 2
                + _x
                + width / 2
                - self.config["cradleTolerance"]
            )
            y = (
                -self.config["panelHeight"] / 2
                + _y
                + height / 2
                - self.config["cradleTolerance"]
            )

        self.supports = (
            # Extrude on the inside
            self.supports.moveTo(x, y)
            .rect(width, height)
            .extrude(-self.config["panelThickness"] + self.config["railsFrontRecess"])
            # Extrude on the back
            .moveTo(x, y)
            .rect(width, height)
            .extrude(self.config["railsSupportDepthBack"])
        )

        if orientation == "horizontal":
            x = (
                -self.config["panelWidth"] / 2
                + _x
                + (self.config["hp"] - self.config["railsScrewDiameter"]) / 2
                + self.config["railsScrewDiameter"] / 2
            )
            if centered:
                x = x - hp(hpWidth) / 2
        else:
            y = (
                -self.config["panelHeight"] / 2
                + _y
                + (self.config["hp"] - self.config["railsScrewDiameter"]) / 2
                + self.config["railsScrewDiameter"] / 2
            )
            if centered:
                y = y - hp(hpWidth) / 2

        # Can't get rarray to work here.
        if orientation == "horizontal":
            for n in range(hpWidth):
                self.supports = (
                    self.supports.moveTo(x + n * self.config["hp"], y)
                    .circle(self.config["railsScrewDiameter"] / 2)
                    .cutThruAll()
                )
        else:
            for n in range(hpWidth):
                self.supports = (
                    self.supports.moveTo(x, y + n * self.config["hp"])
                    .circle(self.config["railsScrewDiameter"] / 2)
                    .cutThruAll()
                )

    def addRail(
        self,
        x: float,
        y: float,
        hpWidth: int,
        centered: bool = True,
        orientation: str = "horizontal",
    ):
        """Adds a recessed hp rail. The rail is added to the supports layer,
         not the panel layer. Good to build cradles: put a Eurorack modules on
        a Kosmo faceplate, or 1U on a Eurorack one.

        x, y define the center.

        orientation is "horizontal" by default, otherwise "vertical"
        """
        self.cutRail(x, y, hpWidth, centered, orientation)
        self.supportRail(x, y, hpWidth, centered, orientation)

    def previewPanel(
        self,
        x: float,
        y: float,
        hpWidth: int,
        height: float,
        centered: bool = True,
        orientation: str = "horizontal",
    ):
        if not self.config["previewRender"]:
            return
        if orientation == "horizontal":
            if centered:
                self.previewBoxOnFront(
                    x + self.config["cradleTolerance"],
                    y
                    + height / 2
                    - self.config["railsHeight"] / 2
                    + self.config["cradleTolerance"] * 2,
                    hp(hpWidth),
                    height,
                    1.6,
                )
            else:
                self.previewBoxOnFront(
                    x + hp(hpWidth) / 2 + self.config["cradleTolerance"],
                    y + height / 2 + self.config["cradleTolerance"] * 2,
                    hp(hpWidth),
                    height,
                    1.6,
                )
        else:  # vertical
            if centered:
                self.previewBoxOnFront(
                    x
                    + height / 2
                    - self.config["railsHeight"] / 2
                    + self.config["cradleTolerance"] * 2,
                    y + self.config["cradleTolerance"],
                    height,
                    hp(hpWidth),
                    1.6,
                )
            else:
                self.previewBoxOnFront(
                    x + height / 2 + self.config["cradleTolerance"] * 2,
                    y + hp(hpWidth) / 2 + self.config["cradleTolerance"],
                    height,
                    hp(hpWidth),
                    1.6,
                )

    def addCradle(
        self,
        x: float,
        y: float,
        hpWidth: int,
        height: float,
        centered: bool = True,
        orientation: str = "horizontal",
        supportTop: bool = True,
        supportRight: bool = True,
        supportBottom: bool = True,
        supportLeft: bool = True,
    ):
        """Adds a pair of recessed hp rails and a hole for modules.
        The rail is added to the supports layer, not the panel layer.
        You probably want to use `addEurorackCradle()` or
        `add1UIJCradle()` instead.
        """
        # Add the two rails
        self.addRail(x, y, hpWidth, centered, orientation)
        if orientation == "horizontal":
            self.addRail(
                x,
                y + height - self.config["m3Diameter"] * 2,
                hpWidth,
                centered,
                orientation,
            )
        else:
            self.addRail(
                x + height - self.config["m3Diameter"] * 2,
                y,
                hpWidth,
                centered,
                orientation,
            )
        # Cut a hole between those rails
        if orientation == "horizontal":
            if centered:
                self.cutRect(
                    x,
                    y + height / 2 - self.config["railsHeight"] / 2,
                    hp(hpWidth) + self.config["cradleTolerance"] * 2,
                    height + self.config["cradleTolerance"] * 2,
                    0,
                    centered,
                )
                offset = -hp(hpWidth) / 2
                x1 = x - 3 + offset
                x2 = x + hp(hpWidth) + offset
                y1 = y - self.config["railsHeight"] / 2 - 3
                y2 = y + height - 2
            else:
                self.cutRect(
                    x - self.config["cradleTolerance"],
                    y - self.config["cradleTolerance"],
                    hp(hpWidth) + self.config["cradleTolerance"] * 2,
                    height + self.config["cradleTolerance"] * 2,
                    0,
                    centered,
                )
                offset = 0
                x1 = x - 3 + offset
                x2 = x + hp(hpWidth) + offset
                y1 = y - 3
                y2 = y + height + 2
            w = hp(hpWidth) + 6
            h = height + 6
        else:  # vertical
            if centered:
                self.cutRect(
                    x + height / 2 - self.config["railsHeight"] / 2,
                    y,
                    height + self.config["cradleTolerance"] * 2,
                    hp(hpWidth) + self.config["cradleTolerance"] * 2,
                    0,
                    centered,
                )
                x1 = (
                    x - self.config["railsHeight"] * 0.7
                )  # FIXME: IDK why it needs this number. This prolly breaks alt values.
                x2 = x + height - 2
                y1 = y - hp(hpWidth) / 2 - 3
                y2 = y + hp(hpWidth) / 2
            else:
                self.cutRect(
                    x - self.config["cradleTolerance"],
                    y - self.config["cradleTolerance"],
                    height + self.config["cradleTolerance"] * 2,
                    hp(hpWidth) + self.config["cradleTolerance"] * 2,
                    0,
                    centered,
                )
                x1 = x - 3
                x2 = x + height + 2
                y1 = y - 3
                y2 = y + hp(hpWidth)
            w = height + 6
            h = hp(hpWidth) + 6
        if supportTop:
            self.supportBar(
                x1,
                y1,
                w,
                3 + self.config["cradleTolerance"] * 2,
                self.config["railsSupportDepthBack"],
                False,
            )
        if supportBottom:
            self.supportBar(
                x1,
                y2 - self.config["cradleTolerance"] * 2,
                w,
                3 + self.config["cradleTolerance"] * 2,
                self.config["railsSupportDepthBack"],
                False,
            )
        if supportLeft:
            self.supportBar(
                x1,
                y1,
                3 + self.config["cradleTolerance"] * 2,
                h,
                self.config["railsSupportDepthBack"],
                False,
            )
        if supportRight:
            self.supportBar(
                x2 - self.config["cradleTolerance"] * 2,
                y1,
                3 + self.config["cradleTolerance"] * 2,
                h,
                self.config["railsSupportDepthBack"],
                False,
            )

        self.previewPanel(x, y, hpWidth, height, centered, orientation)

    def addEurorackCradle(
        self,
        x: float,
        y: float,
        hpWidth: int,
        centered: bool = True,
        orientation: str = "horizontal",
        supportTop: bool = True,
        supportRight: bool = True,
        supportBottom: bool = True,
        supportLeft: bool = True,
    ):
        """Adds a pair of recessed hp rails and a hole for modules.
        The rail is added to the supports layer, not the panel layer.
        Screw holes are spaced vertically 122.5mm apart for Eurorack.
        There are supports around the cradle for increased strength.

        This footprint will probbly not work with custom values
        without modifying the code.

        Printed rails hold modules satisfactorily using M3x8mm screws, and
        the holes last a dozen screwing cycles before becoming too enlarged
        to hold things well. For increased safety, use longer screws and nuts.

        Strongly advised to print with supports, but will still print OK without.

        x, y define the center hole of the top rail if centered, that is,
        if the rail is 3hp, the coordinates define the center of the 2nd hole.
        If not centered, the coordinates define the top-left of the
        opening window.

        orientation is "horizontal" by default, otherwise "vertical"

        supportTop, supportRight, supportBottom, supportLeft can be set to False
        to allow stacking rails next to each other."""
        self.addCradle(
            x,
            y,
            hpWidth,
            self.config["eurorackHeight"],
            centered,
            orientation,
            supportTop,
            supportRight,
            supportBottom,
            supportLeft,
        )

    def add1UIJCradle(
        self,
        x: float,
        y: float,
        hpWidth: int,
        centered: bool = True,
        orientation: str = "horizontal",
        supportTop: bool = True,
        supportRight: bool = True,
        supportBottom: bool = True,
        supportLeft: bool = True,
    ):
        """Adds a pair of recessed hp rails and a hole for modules.
        The rail is added to the supports layer, not the panel layer.
        Screw holes are spaced vertically 33.65mm apart for 1U (Intellijel).
        There are supports around the cradle for increased strength.

        This footprint will probbly not work with custom values
        without modifying the code.

        Printed rails hold modules satisfactorily using M3x8mm screws, and
        the holes last a dozen screwing cycles before becoming too enlarged
        to hold things well. For increased safety, use longer screws and nuts.

        Strongly advised to print with supports, but will still print OK without.

        x, y define the center hole of the top rail if centered, that is,
        if the rail is 3hp, the coordinates define the center of the 2nd hole.
        If not centered, the coordinates define the top-left of the
        opening window.

        orientation is "horizontal" by default, otherwise "vertical"

        supportTop, supportRight, supportBottom, supportLeft can be set to False
        to allow stacking rails next to each other.
        """
        self.addCradle(
            x,
            y,
            hpWidth,
            self.config["1UIJHeight"],
            centered,
            orientation,
            supportTop,
            supportRight,
            supportBottom,
            supportLeft,
        )

    #######################################################################
    ### Support structures
    #######################################################################

    # Every function adding to the supports layer has support at the
    # start of the name.

    def supportBar(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        depth: float,
        centered: bool = False,
    ):
        """Adds a box on the supports layer.

        x, y define the top-left of the box as seen from the front
        """
        if not self.config["supportsRender"]:
            return
        if centered:
            x = -self.config["panelWidth"] / 2 + x
            y = -self.config["panelHeight"] / 2 + y
        else:
            x = -self.config["panelWidth"] / 2 + x + width / 2
            y = -self.config["panelHeight"] / 2 + y + height / 2
        self.supports = (
            self.supports.moveTo(
                x,
                y,
            )
            .rect(width, height)
            .extrude(depth)
        )

    #######################################################################
    ### Drill template marks
    #######################################################################

    # Drill template marks are simple cross shapes that will more or less
    # look like crosses when exported at typical sizes.
    # Every function adding to the drillTemplate layer has mark at the
    # start of the name

    def markOutline(self):
        """Add an outline to the drill template layer. This ensures proper
        SVG export. This is automatically done when adding a panel."""

        self.drillTemplate = (
            self.drillTemplate.moveTo(  # Top
                0,
                -self.config["panelHeight"] / 2
                + self.config["DrillTemplateMarkThickness"] / 2,
            )
            .rect(
                self.config["panelWidth"],
                self.config["DrillTemplateMarkThickness"],
            )
            .extrude(self.config["DrillTemplateMarkThickness"])
            .moveTo(  # Bottom
                0,
                self.config["panelHeight"] / 2
                - self.config["DrillTemplateMarkThickness"] / 2,
            )
            .rect(
                self.config["panelWidth"],
                self.config["DrillTemplateMarkThickness"],
            )
            .extrude(self.config["DrillTemplateMarkThickness"])
            .moveTo(  # Left
                -self.config["panelWidth"] / 2
                + self.config["DrillTemplateMarkThickness"] / 2,
                0,
            )
            .rect(
                self.config["DrillTemplateMarkThickness"],
                self.config["panelHeight"],
            )
            .extrude(self.config["DrillTemplateMarkThickness"])
            .moveTo(  # Right
                self.config["panelWidth"] / 2
                - self.config["DrillTemplateMarkThickness"] / 2,
                0,
            )
            .rect(
                self.config["DrillTemplateMarkThickness"],
                self.config["panelHeight"],
            )
            .extrude(self.config["DrillTemplateMarkThickness"])
        )

    def markCross(self, x: float, y: float):
        """Adds a mark on the drill template layer. At typical synth panel
        sizes, it will show up as a cross the perfect size for printing out and
        using as a drill template.

        x, y define the center of the mark as seen from the front.
        """
        self.drillTemplate = (
            self.drillTemplate.moveTo(
                -self.config["panelWidth"] / 2 + x,
                -self.config["panelHeight"] / 2 + y,
            )
            .rect(
                self.config["DrillTemplateMarkLength"],
                self.config["DrillTemplateMarkThickness"],
            )
            .extrude(self.config["DrillTemplateMarkThickness"])
            .moveTo(
                -self.config["panelWidth"] / 2 + x,
                -self.config["panelHeight"] / 2 + y,
            )
            .rect(
                self.config["DrillTemplateMarkThickness"],
                self.config["DrillTemplateMarkLength"],
            )
            .extrude(self.config["DrillTemplateMarkThickness"])
        )

    def markRect(self, x: float, y: float, width: float, height: float):
        """Marks a rectangle on the drill template.

        x, y define the center."""

        self.drillTemplate = (
            self.drillTemplate.moveTo(
                -self.config["panelWidth"] / 2 + x,
                -self.config["panelHeight"] / 2 + y,
            )
            .rect(width, height)
            .extrude(1)
            .moveTo(
                -self.config["panelWidth"] / 2 + x,
                -self.config["panelHeight"] / 2 + y,
            )
            .rect(
                width - self.config["DrillTemplateMarkThickness"] * 2,
                height - self.config["DrillTemplateMarkThickness"] * 2,
            )
            .cutThruAll()
        )

    def markHole(self, x: float, y: float, diameter: float):
        """Marks a circular hole on the drill template.

        x, y define the center.

        FIXME: Nasty implementation, and requires marking circles before crosses

        """
        self.drillTemplate = (
            self.drillTemplate.moveTo(
                -self.config["panelWidth"] / 2 + x,
                -self.config["panelHeight"] / 2 + y,
            )
            .circle(diameter / 2)
            .extrude(1)
            .moveTo(
                -self.config["panelWidth"] / 2 + x,
                -self.config["panelHeight"] / 2 + y,
            )
            .circle(diameter / 2 - self.config["DrillTemplateMarkThickness"])
            .cutThruAll()
        )
        return

    #######################################################################
    ### Buttons and switches
    #######################################################################

    ### 30mm Arcade Buttons

    def cutArcadeButton30mm(self, x: float, y: float):
        if not self.config["panelRender"]:
            return
        self.cutHole(x, y, self.config["arcade30mmButtonWithTolerance"])

    def previewArcadeButton30mm(self, x: float, y: float):
        if not self.config["previewRender"]:
            return
        self.previewCylinderOnFront(x, y, 32.3, 3.4)
        self.previewCylinderOnFront(x, y, 24, 7)
        self.previewCylinderOnBack(x, y, 24, 24.4)
        self.previewCylinderOnBack(x, y, 34.8, 6.5)

    def markArcadeButton30mm(self, x: float, y: float):
        if not self.config["drillTemplateRender"]:
            return
        self.markHole(x, y, self.config["arcade30mmButtonWithTolerance"])
        self.markCross(x, y)

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
        self.markArcadeButton30mm(x, y)

    ### 24mm Arcade Buttons

    def cutArcadeButton24mm(self, x: float, y: float):
        if not self.config["panelRender"]:
            return
        self.cutHole(x, y, self.config["arcade24mmButtonWithTolerance"])
        self.cutHole(
            x,
            y,
            self.config["arcade24mmButtonAdditionalClearanceDiameter"],
            self.config["arcade24mmButtonAdditionalClearanceDepth"],
        )

    def previewArcadeButton24mm(self, x: float, y: float):
        if not self.config["previewRender"]:
            return
        self.previewCylinderOnFront(x, y, 27, 3.4)
        self.previewCylinderOnFront(x, y, 22, 7)
        self.previewCylinderOnBack(x, y, 24, 24.4)
        self.previewCylinderOnBack(x, y, 28, 6)

    def markArcadeButton24mm(self, x: float, y: float):
        if not self.config["drillTemplateRender"]:
            return
        self.markHole(x, y, self.config["arcade24mmButtonWithTolerance"])
        self.markCross(x, y)

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
        self.markArcadeButton24mm(x, y)

    ### Mini Toggle Switches

    def cutMiniToggleSwitch(self, x: float, y: float, orientation: str = "horizontal"):
        if not self.config["panelRender"]:
            return
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
        if not self.config["previewRender"]:
            return
        if orientation == "horizontal":
            width = self.config["miniToggleSwitchWidth"]
            length = self.config["miniToggleSwitchLength"]
        else:
            width = self.config["miniToggleSwitchLength"]
            length = self.config["miniToggleSwitchWidth"]
        self.previewBoxOnBack(x, y, width, length, 13.6)
        self.previewCylinderOnFront(x, y, self.config["miniToggleSwitchDiameter"], 19)

    def markMiniToggleSwitch(self, x: float, y: float):
        if not self.config["drillTemplateRender"]:
            return
        self.markHole(x, y, self.config["miniToggleSwitchDiameterWithTolerance"])
        self.markCross(x, y)

    def addMiniToggleSwitch(self, x: float, y: float, orientation: str = "horizontal"):
        """A mini toggle switch, with a retaining notch.

        This will fit the switches often sold as the "MTS-100" series by Aliexpress vendors that have only a single row of pins.

        It will not fit DPDT switches that have two rows of pins, those are bigger.

        orientation: "horizontal" (default) or "vertical".
        """
        self.cutMiniToggleSwitch(x, y, orientation)
        self.previewMiniToggleSwitch(x, y, orientation)
        self.markMiniToggleSwitch(x, y)

    ### PBS-110 7mm Momentary Pushbutton

    def cutMomentaryPushbutton7mm(self, x: float, y: float):
        if not self.config["panelRender"]:
            return
        self.cutHole(x, y, self.config["momentaryPushbutton7mmDiameterWithTolerance"])
        self.cutHole(
            x,
            y,
            self.config["momentaryPushbutton7mmNotchDiameterWithTolerance"],
            self.config["momentaryPushbutton7mmNotchDepth"],
        )

    def previewMomentaryPushbutton7mm(self, x: float, y: float):
        if not self.config["previewRender"]:
            return
        self.previewCylinderOnFront(x, y, 7.5, 12)
        self.previewCylinderOnBack(x, y, 9.5, 13)

    def markMomentaryPushbutton7mm(self, x: float, y: float):
        if not self.config["drillTemplateRender"]:
            return
        self.markHole(x, y, self.config["momentaryPushbutton7mmDiameterWithTolerance"])
        self.markCross(x, y)

    # TODO: Recess?
    def addMomentaryPushbutton7mm(self, x: float, y: float):
        """PBS-110 momentary pushbuttons are commonly used and easy to find in many colors.

        As the screw thread can be rather short, the retaining notch isn't just for alignment
        but also ensures enough of the thread is exposed for a strong grip.
        """
        self.cutMomentaryPushbutton7mm(x, y)
        self.previewMomentaryPushbutton7mm(x, y)
        self.markMomentaryPushbutton7mm(x, y)

    #######################################################################
    ### Potentiometers, rotary encoders, sliders
    #######################################################################

    def cutPotentiometer(
        self,
        x: float,
        y: float,
        notchOrientation: str = "all",
        rotaryEncoderNotch: bool = False,
    ):
        if not self.config["panelRender"]:
            return
        self.cutHole(x, y, self.config["potentiometerHoleDiameterWithTolerance"])
        # List the notches
        points = []  # default to "none" configuration
        if notchOrientation == "top" or notchOrientation == "all":
            points.append((0, -self.config["potentiometerNotchDistanceFromCenter"]))
        if notchOrientation == "right" or notchOrientation == "all":
            points.append((self.config["potentiometerNotchDistanceFromCenter"], 0))
        if notchOrientation == "bottom" or notchOrientation == "all":
            points.append((0, self.config["potentiometerNotchDistanceFromCenter"]))
        if notchOrientation == "left" or notchOrientation == "all":
            points.append((-self.config["potentiometerNotchDistanceFromCenter"], 0))
        # Cut the notches
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
        # Notch for the encoder
        if rotaryEncoderNotch:
            self.panel = (
                self.panel.faces(">Z")
                .vertices("<XY")
                .workplane(centerOption="CenterOfMass")
                .center(x, y)
                .rect(
                    self.config["rotaryEncoderWidthWithTolerance"],
                    self.config["rotaryEncoderHeightWithTolerance"],
                )
                .cutBlind(-self.config["rotaryEncoderNotchDepth"])
            )

    def previewPotentiometer(self, x: float, y: float, lugsOrientation: str = "all"):
        if not self.config["previewRender"]:
            return
        self.previewCylinderOnFront(x, y, 6, 21)
        self.previewCylinderOnFront(x, y, 9.6, 1.6)
        self.previewCylinderOnBack(x, y, 16, 8)
        if lugsOrientation == "all" or lugsOrientation == "bottom":
            self.previewBoxOnBack(x, y + 8, 15, 18, 2.4)
        if lugsOrientation == "top":
            self.previewBoxOnBack(x, y - 8, 15, 18, 2.4)
        if lugsOrientation == "left":
            self.previewBoxOnBack(x - 8, y, 18, 15, 2.4)
        if lugsOrientation == "right":
            self.previewBoxOnBack(x + 8, y, 18, 15, 2.4)

    def markPotentiometer(self, x: float, y: float):
        if not self.config["drillTemplateRender"]:
            return
        self.markHole(x, y, self.config["potentiometerHoleDiameterWithTolerance"])
        self.markCross(x, y)

    def addPotentiometer(
        self,
        x: float,
        y: float,
        notchOrientation: str = "all",
        lugsOrientation: str = "all",
        rotaryEncoderNotch: bool = False,
    ):
        """Fits most types of panel-mount potentiometers with a 6mm shaft.

        There will be four notches around the hole, allowing you to catch the
        retaining tab of the potentiometer in the most convenient orientation
        possible.

        Common rotary encoders such as EC11 could use a thinner panel for the
        shaft to protrude sufficiently, in which case, set `rotaryEncoderNotch`
        to `True` to cut a rectangle in the back of the  panel.

        If you want a knob, add it separately with addKnob()

        The orientation parameters are seen from the front, and are:
        "all", "none", "top", "left", "right", "bottom".

        The retaining notches aren't always on the same side, depending on the
        type of potentiometer! If in doubt, just leave it to "all" to add 4 notches.

        The preview size for the lugs doesn't account for the possibility of bending them,
        so it might be safe to have this area overlap other stuff a little.
        """
        self.cutPotentiometer(x, y, notchOrientation, rotaryEncoderNotch)
        self.previewPotentiometer(x, y, lugsOrientation)
        self.markPotentiometer(x, y)

    def previewKnob(self, x: float, y: float, diameter: float, depth: float):
        if not self.config["previewRender"]:
            return
        self.previewCylinderOnFront(x, y, diameter, depth + 5)

    def addKnob(self, x: float, y: float, diameter: float, depth: float):
        """Adds a knob for preview only. Place it at the same location as
        potentiometers and rotary encoders!

        Since there is a lot of variation in knob sizes, and sometimes the
        shaft is left exposed without a knob, it's not added automatically."""
        self.previewKnob(x, y, diameter, depth)

    def cutSlider(
        self,
        x: float,
        y: float,
        sliderWidth: float,
        sliderHeight: float,
        slotWidth: float,
        slotHeight: float,
    ):
        if not self.config["panelRender"]:
            return
        self.panel = (
            self.panel.faces(">Z")
            .vertices("<XY")
            .workplane(centerOption="CenterOfMass")
            .center(x, y)
            .rect(
                sliderWidth,
                sliderHeight,
            )
            .cutBlind(-self.config["sliderNotchDepth"])
        )
        self.cutRect(x, y, slotWidth, slotHeight, 0, True)

    def previewSlider(
        self, x: float, y: float, sliderWidth: float, sliderHeight: float
    ):
        if not self.config["previewRender"]:
            return
        self.previewCylinderOnFront(x, y, 15, 10)
        self.previewBoxOnBack(x, y, sliderWidth, sliderHeight, 22)

    def markSlider(
        self,
        x: float,
        y: float,
        sliderWidth: float,
        sliderHeight: float,
        slotWidth: float,
        slotHeight: float,
    ):
        if not self.config["drillTemplateRender"]:
            return
        self.markRect(x, y, sliderWidth, sliderHeight)
        self.markRect(x, y, slotWidth, slotHeight)

    def addSlider(
        self,
        x: float,
        y: float,
        sliderWidth: float,
        sliderHeight: float,
        slotWidth: float,
        slotHeight: float,
    ):
        """For slide potentiomenters. Multiple sizes are common, so you have to
        specify yours.

        No special provision are made to hold them in place, it's assumed you
        have a PCB or are will add some glue or something similarly nasty.

        x, y: center
        """
        self.cutSlider(x, y, sliderWidth, sliderHeight, slotWidth, slotHeight)
        self.previewSlider(x, y, sliderWidth, sliderHeight)
        self.markSlider(x, y, sliderWidth, sliderHeight, slotWidth, slotHeight)

    #######################################################################
    ### Jacks & Sockets
    #######################################################################

    def cutBigJack(self, x: float, y: float):
        if not self.config["panelRender"]:
            return
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
        if not self.config["previewRender"]:
            return
        self.previewCylinderOnFront(x, y, 8.5, 7)
        self.previewCylinderOnFront(x, y, 12.6, 2.2)
        self.previewBoxOnBack(x, y, 16, 16, 27)

    def markBigJack(self, x: float, y: float):
        if not self.config["drillTemplateRender"]:
            return
        self.markHole(x, y, self.config["bigJackDiameterWithTolerance"])
        self.markCross(x, y)

    def addBigJack(self, x: float, y: float):
        """This fits panel mount 6.35mm jacks with a rectangular base, as used
        in Kosmo builds.

        There is a retaining notch the size of the base to help keep it in place.
        """
        self.cutBigJack(x, y)
        self.previewBigJack(x, y)
        self.markBigJack(x, y)

    def cutMiniJack(self, x: float, y: float):
        if not self.config["panelRender"]:
            return
        self.cutHole(x, y, self.config["miniJackDiameterWithTolerance"])
        self.panel = (
            self.panel.faces(">Z")
            .vertices("<XY")
            .workplane(centerOption="CenterOfMass")
            .center(x, y)
            .rect(
                self.config["miniJackSizeWithTolerance"],
                self.config["miniJackSizeWithTolerance"],
            )
            .cutBlind(-self.config["miniJackNotchDepth"])
        )

    def previewMiniJack(self, x: float, y: float):
        if not self.config["previewRender"]:
            return
        self.previewCylinderOnFront(x, y, 6, 5.5)
        self.previewCylinderOnFront(x, y, 8, 2.2)
        self.previewBoxOnBack(x, y, 9, 10.5, 12.5)

    def markMiniJack(self, x: float, y: float):
        if not self.config["drillTemplateRender"]:
            return
        self.markHole(x, y, self.config["miniJackDiameterWithTolerance"])
        self.markCross(x, y)

    def addMiniJack(self, x: float, y: float):
        """This fits 3.5mm PJ398SM "Thonkiconn" 3.5mm jacks and similar.

        There is a retaining notch the size of the base to help keep it in place.
        """
        self.cutMiniJack(x, y)
        self.previewMiniJack(x, y)
        self.markMiniJack(x, y)

    def cutMidiSocket(self, x: float, y: float, screws: str = "horizontal"):
        if not self.config["panelRender"]:
            return
        self.cutHole(x, y, self.config["midiSocketDiameterWithTolerance"])
        if screws == "horizontal":
            self.cutHole(
                x - self.config["midiSocketScrewDistance"] / 2,
                y,
                self.config["midiSocketScrewDiameterWithTolerance"],
            )
            self.cutHole(
                x + self.config["midiSocketScrewDistance"] / 2,
                y,
                self.config["midiSocketScrewDiameterWithTolerance"],
            )
        if screws == "vertical":
            self.cutHole(
                x,
                y - self.config["midiSocketScrewDistance"] / 2,
                self.config["midiSocketScrewDiameterWithTolerance"],
            )
            self.cutHole(
                x,
                y + self.config["midiSocketScrewDistance"] / 2,
                self.config["midiSocketScrewDiameterWithTolerance"],
            )

    def previewMidiSocket(self, x: float, y: float, screws: str = "horizontal"):
        if not self.config["previewRender"]:
            return
        self.previewCylinderOnBack(x, y, 14, 16)
        if screws == "horizontal":
            self.previewBoxOnFront(x, y, 28, 19, 1)
        if screws == "vertical":
            self.previewBoxOnFront(x, y, 19, 28, 1)

    def markMidiSocket(self, x: float, y: float, screws: str = "horizontal"):
        if not self.config["drillTemplateRender"]:
            return
        self.markHole(x, y, self.config["midiSocketDiameterWithTolerance"])
        self.markCross(x, y)
        if screws == "horizontal":
            self.markHole(
                x - self.config["midiSocketScrewDistance"] / 2,
                y,
                self.config["midiSocketScrewDiameterWithTolerance"],
            )
            self.markHole(
                x + self.config["midiSocketScrewDistance"] / 2,
                y,
                self.config["midiSocketScrewDiameterWithTolerance"],
            )
            self.markCross(x - self.config["midiSocketScrewDistance"] / 2, y)
            self.markCross(x + self.config["midiSocketScrewDistance"] / 2, y)
        if screws == "vertical":
            self.markHole(
                x,
                y - self.config["midiSocketScrewDistance"] / 2,
                self.config["midiSocketScrewDiameterWithTolerance"],
            )
            self.markHole(
                x,
                y + self.config["midiSocketScrewDistance"] / 2,
                self.config["midiSocketScrewDiameterWithTolerance"],
            )
            self.markCross(x, y - self.config["midiSocketScrewDistance"] / 2)
            self.markCross(x, y + self.config["midiSocketScrewDistance"] / 2)

    def addMidiSocket(self, x: float, y: float, screws: str = "horizontal"):
        """Adds a panel mount female DIN socket.

        It fits the aluminum sockets that have two M3 screws on each side.

        screws: "horizontal", "vertical", or "none"
        """
        self.cutMidiSocket(x, y, screws)
        self.previewMidiSocket(x, y, screws)
        self.markMidiSocket(x, y, screws)

    #######################################################################
    ### Blinkenlichten
    #######################################################################

    def cutLed5mm(self, x: float, y: float):
        if not self.config["panelRender"]:
            return
        self.cutHole(x, y, self.config["5mmLedWithTolerance"])

    def previewLed5mm(self, x: float, y: float):
        if not self.config["previewRender"]:
            return
        self.previewCylinderOnFront(x, y, 4.7, 3)
        self.previewBoxOnBack(x, y, 4, 1, 17)

    def markLed5mm(self, x: float, y: float):
        if not self.config["drillTemplateRender"]:
            return
        self.markHole(x, y, self.config["5mmLedWithTolerance"])
        self.markCross(x, y)

    def addLed5mm(self, x: float, y: float):
        """Creates a hole for a 5mm LED protruding from the hole.

        There is no mechanism to hold it in place, but hot glue will do the trick.
        """
        self.cutLed5mm(x, y)
        self.previewLed5mm(x, y)
        self.markLed5mm(x, y)

    def cutLed3mm(self, x: float, y: float):
        if not self.config["panelRender"]:
            return
        self.cutHole(x, y, self.config["3mmLedWithTolerance"])

    def previewLed3mm(self, x: float, y: float):
        if not self.config["previewRender"]:
            return
        self.previewCylinderOnFront(x, y, 2.8, 1)
        self.previewBoxOnBack(x, y, 2.7, 1, 17)

    def markLed3mm(self, x: float, y: float):
        if not self.config["drillTemplateRender"]:
            return
        self.markHole(x, y, self.config["3mmLedWithTolerance"])
        self.markCross(x, y)

    def addLed3mm(self, x: float, y: float):
        """Creates a hole for a 3mm LED fitting inside the hole.
        On default settings, it will not protrude past the hole, and might
        diffuse a bit of light in the surrounding plastic.

        There is no mechanism to hold it in place, but hot glue will do the trick.
        """
        self.cutLed3mm(x, y)
        self.previewLed3mm(x, y)
        self.markLed3mm(x, y)

    def cutLedRectangular(self, x: float, y: float, orientation: str = "vertical"):
        if not self.config["panelRender"]:
            return
        if orientation == "vertical":
            self.cutRect(
                x,
                y,
                self.config["RectangularLedWidthWithTolerance"],
                self.config["RectangularLedHeightWithTolerance"],
            )
        else:
            self.cutRect(
                x,
                y,
                self.config["RectangularLedHeightWithTolerance"],
                self.config["RectangularLedWidthWithTolerance"],
            )

    def previewLedRectangular(self, x: float, y: float, orientation: str = "vertical"):
        if not self.config["previewRender"]:
            return
        # self.previewCylinderOnFront(x, y, 4.7, 3)
        # self.previewBoxOnBack(x, y, 4, 1, 17)
        if orientation == "vertical":
            self.previewBoxOnBack(x, y, 1, 4, 17)
            self.previewBoxOnFront(x, y, 2, 5, 2)
        else:
            self.previewBoxOnBack(x, y, 4, 1, 17)
            self.previewBoxOnFront(x, y, 5, 2, 2)

    def markLedRectangular(self, x: float, y: float, orientation: str = "vertical"):
        if not self.config["drillTemplateRender"]:
            return
        if orientation == "vertical":
            self.markRect(
                x,
                y,
                self.config["RectangularLedWidthWithTolerance"],
                self.config["RectangularLedHeightWithTolerance"],
            )
        else:
            self.markRect(
                x,
                y,
                self.config["RectangularLedHeightWithTolerance"],
                self.config["RectangularLedWidthWithTolerance"],
            )
        self.markCross(x, y)

    def addLedRectangular(self, x: float, y: float, orientation: str = "vertical"):
        """Creates a slot for a rectangular 2×5mm LED.

        FIXME: This footprint is currently untested.

        There is no mechanism to hold it in place, but hot glue will do the trick.
        """
        self.cutLedRectangular(x, y, orientation)
        self.previewLedRectangular(x, y, orientation)
        self.markLedRectangular(x, y, orientation)

    def cutDisplayWindow(
        self,
        x: float,
        y: float,
        windowWidth: float = 30,
        windowHeight: float = 15,
        windowHorizontalOffset: float = 0,
        windowVerticalOffset: float = -5,
        screwsHorizontalDistance: float = 40,
        screwsVerticalDistance: float = 40,
        addScrews: bool = True,
    ):
        # FIXME: This is the nastiest way possible to implement a fillet
        # but the only one I could figure out.

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
        if addScrews:
            self.panel = (
                self.panel.faces(">Z")
                .vertices("<XY")
                .workplane(centerOption="CenterOfMass")
                .center(x, y)
                .rect(
                    screwsHorizontalDistance,
                    screwsVerticalDistance,
                    forConstruction=True,
                )
                .vertices()
                .circle(self.config["m2DiameterWithTolerance"] / 2)
                .cutThruAll()
            )

    def markDisplayWindow(
        self,
        x: float,
        y: float,
        windowWidth: float = 30,
        windowHeight: float = 15,
        windowHorizontalOffset: float = 0,
        windowVerticalOffset: float = -5,
        screwsHorizontalDistance: float = 40,
        screwsVerticalDistance: float = 40,
        addScrews: bool = True,
    ):
        if not self.config["drillTemplateRender"]:
            return
        self.markRect(
            x + windowHorizontalOffset,
            y + windowVerticalOffset,
            windowWidth,
            windowHeight,
        )
        if addScrews:
            self.markHole(
                x - screwsHorizontalDistance / 2,
                y - screwsVerticalDistance / 2,
                self.config["m2DiameterWithTolerance"],
            )
            self.markHole(
                x + screwsHorizontalDistance / 2,
                y - screwsVerticalDistance / 2,
                self.config["m2DiameterWithTolerance"],
            )
            self.markHole(
                x - screwsHorizontalDistance / 2,
                y + screwsVerticalDistance / 2,
                self.config["m2DiameterWithTolerance"],
            )
            self.markHole(
                x + screwsHorizontalDistance / 2,
                y + screwsVerticalDistance / 2,
                self.config["m2DiameterWithTolerance"],
            )
            self.markCross(
                x - screwsHorizontalDistance / 2,
                y - screwsVerticalDistance / 2,
            )
            self.markCross(
                x + screwsHorizontalDistance / 2,
                y - screwsVerticalDistance / 2,
            )
            self.markCross(
                x - screwsHorizontalDistance / 2,
                y + screwsVerticalDistance / 2,
            )
            self.markCross(
                x + screwsHorizontalDistance / 2,
                y + screwsVerticalDistance / 2,
            )

    def addDisplayWindow(
        self,
        x: float,
        y: float,
        windowWidth: float = 30,
        windowHeight: float = 15,
        windowHorizontalOffset: float = 0,
        windowVerticalOffset: float = -5,
        screwsHorizontalDistance: float = 40,
        screwsVerticalDistance: float = 40,
        addScrews: bool = True,
    ):
        """Creates a window for a rectangular display mounted with four screws in the corner.

        Every single display available has different dimensions, especially the cheapo OLEDs
        from Aliexpress. Even when the display size is the same, various boards differ by
        a few millimeters.

        The defaults offered are for a non-existent model, for preview purposes.
        Provide your own measurements instead!

        There is no preview widget for this footprint.
        """
        self.cutDisplayWindow(
            x,
            y,
            windowWidth,
            windowHeight,
            windowHorizontalOffset,
            windowVerticalOffset,
            screwsHorizontalDistance,
            screwsVerticalDistance,
            addScrews,
        )

        self.markDisplayWindow(
            x,
            y,
            windowWidth,
            windowHeight,
            windowHorizontalOffset,
            windowVerticalOffset,
            screwsHorizontalDistance,
            screwsVerticalDistance,
            addScrews,
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
    """Converts Eurorack Horizontal Pitch to millimeters (1hp = 0.2in = 5.08mm).
    Useful to align things to the grid."""
    return hp * 5.08


def khp(khp: float):
    """Converts khp (Kosmo HP) to millimeters (1khp = 25mm).
    Useful to align things to the the custom kcol / krow grid."""
    return khp * 25


def kcol(kcol: float):
    """Custom Kosmo grid system: each kcol is at the center of a 25mm section"""
    return (kcol - 1) * 25 + 12.5


def krow(krow: float):
    """Custom Kosmo grid system: each krow is 25mm, first starts 25mm from top"""
    return (krow) * 25


def hcol(hcol: float):
    """Custom Eurorack grid system: each hcol is at the center of a 1hp section"""
    return (hcol - 1) * hp(1) + hp(0.5)


def hrow(hrow: float):
    """Custom Eurorack grid system: each hrow is 1hp but vertically,
    first starts 1hp from top"""
    return (hrow) * hp(1)


# To generate API reference: ``pdoc synthprinter.py -o ./``
