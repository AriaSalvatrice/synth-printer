panel = eurorackPanel(hp(12))
preview = previewLayer()


panel = arcadeButton30mmHole(panel, 20, 20)
panel = led5mmHole(panel, 10, 40)
panel = led3mmHole(panel, 10, 48)
panel = potentiometerHole(panel, 30, 45)
panel = bigJackHole(panel, 15, 60)
panel = miniToggleSwitchHole(panel, 46, 15)
panel = miniToggleSwitchHole(panel, 46, 35, orientation="vertical")
panel = miniToggleSwitchHole(panel, 46, 55, orientation="horizontal")

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

preview = preview.box(24, 24, 24)

panelAssembly = cq.Assembly().add(panel, color=cq.Color(0, 0.7, 0.7, 0.9))
previewAssembly = cq.Assembly().add(preview, color=cq.Color(0.3, 0.2, 0.2, 0.5))

show_object(panelAssembly, name="Panel")
show_object(previewAssembly, name="Preview")
