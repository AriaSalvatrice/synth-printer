# Synth Printer: WIP Experiment with CadQuery

**This is not ready for general use yet!**

I don't really know python btw, I just did enough hacks with it to have kinda picked it up by accident. 

-----------------

Hey kid, wanna extrude a synth?

Synth Printer is a very very lightweight system letting you create faceplates for your DIY modular synthesizer, using simple Python code — code so simple you don't need to know any Python at all (a bit of experience with any programming language will be enough).

It's based around [CadQuery](https://github.com/CadQuery/cadquery), but provides a greatly simplified syntax focusing only on synth panels. It's meant to create panels that print right out of the box: they account for tolerances, and they provide footprints that match the kind of synth diy hardware you'll find in the wild. I've made a lot of panels using this system already. My goal is to make it so things will fit on your first attempt.

It's very much for the sort of DIY builds that use prototype boards, or PCBs mounted perpendicularly and wired to the panel. For the sort of DIY builds with sandwiched PCBs mounted in parllel, there's no guarantee the footprints will fit.

Due to its very limited audience, this system is very minimal, hacky, and rough around the edges. Still, it should be easy to learn how to get it going, and I'm happy to help if it gives you trouble. Synth Printer mostly focuses on my own needs: I build in the Kosmo format, which is bigger than Eurorack, so I tend to use bigger hardware options, such as big 6.3mm jacks.

To get started, you need a way to use CadQuery. I strongly recommend you simply use [Cq-Editor](https://github.com/CadQuery/CQ-editor) (grab a binary release).

After that, [download this repository](https://github.com/AriaSalvatrice/synth-printer/archive/refs/heads/master.zip), and load up one of the examples. Use the **▶ Render** button (F5) to run the code. Rotate the viewport, as you'll be seeing the panel from the back by default. 

You can edit code right from CQ-Editor, but if you find it limiting, you can enable autoreload in the preferences, and edit the files from an external editor. You can probably design a panel simply by modifying an example!

If stuff won't fit, you can modify the values in synthprinter.py, or use it as an inspiration to create your own functions.

_FIXME: there are no examples yet lol. just testpanel.py_

Once you're ready to export your panel, select it in the viewport, and pick "Tools -> Export as STL"


# 3D printing advice for synth panels

## Choosing the material

Common options are PLA, PETG, and ABS. 

| 🐶🎺 | PLA | PETG | ABS |
|-------|-----|------|-----|
| Cost | Cheap | Cheap | Affordable |
| Bed adhesion | Easy | Easy | Requires adhesive (ABS slurry or glue) |
| Ease of printing | Easiest | Easy | Hard, requires an enclosure |
| Toxicity | Safe | Safe | Requires proper ventilation while printing |
| Print visual quality | Good | Poor | Good, excellent after acetone vapor smoothing |
| Strength | Good | Good | Excellent |
| Heat resistance | Mediocre | Poor | Good |
| UV resistance | Mediocre | Good | Poor |

Personally, I use PLA. It looks great and is easy to print. But if I were to leave it in a hot car, my synth would be destroyed.

## Solidity

I picked the default thickness of 4mm for a reason! Even at 100% infill, it still bends a little when I unplug jacks. Still, it's solid enough.

Let's review what goes into making a solid front plate:

- Print orientation: 3D prints are weaker to shearing forces along their vertical layer lines. Not a problem for a panel printed flat, but that means the support lattice is particularly weak.
- Shell thickness: Probably even more important than infill. You might want to have 5 of them.
- Infill: Not every infill type is resistant to the same type of forces. I generally use 100% infill anyway, except for tranlucent filaments where I want to achieve a special texture when it's backlit.

## Achieving the best texture

### Printing the front as first layer (recommended)

- You need to achieve a good first layer. There's no secret, it requires a properly tuned printer, a perfectly leveled bed (a depth probe really helps with this), and a perfectly dialed in Z-offset. 
- Print on smooth glass if you can! If you have a textured glass bed, it's safe to flip it over and just print on the untextured side. This will tremendously improve the print quality. You might want to add just a touch of hair spray if heat isn't enough to hold things in place.
- You can achieve neat light reflection tricks by using an interesting bottom fill pattern. I often use the concentric one. The effect is dramatic when used with a Silk filament!
- Wanna use a beautiful but expensive specialty filament for your faceplates? Just swap filament after 3~4 layers! Do the visible layers with your fancy filament, and the rest with bargain bin stock. 
- After the first layer, it's safe to use the highest layer height your printer supports, we don't care about vertical accuracy. 

### Printing the front as last layer

- Consider enabling ironing in your slicer settings! It takes a long while, but can achieve incredibly smooth results.
- The recessed areas on the back will look visually nastier, but shouldn't require supports.
- Of course, you can't add a lattice in the back with this orientation. 
- With a poorly tuned or low quality printer, this orientation will probably yield better results.

### Printing knobs

I had good results with [Sebajom's OpenSCAD knob generators on thingiverse](https://www.thingiverse.com/sebajom/designs).

# Contributing

How much this project will be updated very much depends whether other people use it at all. If you make anything with it, be sure to show me!

You can help by: 

- Reporting your successes and failures
- Contributing footprints that worked out for you 
- Making the code less bad (but let's keep it simple)


# Todo-List

- [x] Figure out a decent "architecture" that's simple & close to natural language
  - Just going with a collection of functions, but maybe i can integrate it to CadQuery's fluent API?
  - Need to move with an architecture where you have default settings you override
  - Just have an object hold it all, having to specify the panel every time is dirty.
- [ ] Remake all my existing footprints
  - Remade a bunch already
- [ ] Make the footprints I expect to need
- [ ] More consistent nomenclature in code
- [ ] Have little previews of the expected footprint of elements (nothing fancy, just cylinders and cubes)
  - Should i use assemblies? 
- [ ] Integrate the support lattice properly. Maybe remake it? Also cache it, it takes too long to generate.
- [x] Figure out how to make fillets/chamfers for big windows not suck ass and require Blender touch-ups
- [ ] Documentation!! This is the most important part. I need to explain all it takes to get good results.
- [ ] A jupyter browser thing? Sounds daunting but people would really prefer not to have to install anything.
- [ ] Do people want to add text labels? They will be very disappointed with quality though. 
- [ ] Good documentation of the available functions, there's already docstrings so i can prolly automate it
- [ ] SVG Export, document a process to print on transparencies, mention toner transfer
- [ ] Figure out more how to make it useful for DXF / CNC processes