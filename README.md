# Synth Printer


Hey kid, wanna extrude a synth?

Synth Printer is a very very lightweight system letting you create faceplates for your DIY modular synthesizer, using simple Python code — code so simple you don't need to know any Python at all (a bit of experience with any programming language will be enough). You don't need to install a complex Python environment either.

Try it out! In just a few minutes, you'll get a STL file ready to print, and your components will fit just right, without having to bust out the calipers. With live visualization as you edit the code, and realistic previews of the size of the elements, it's much less fiddly than using CAD software, and much easier to get clearances right.

![](https://fedi.aria.dog/media/c4884ecad3a1700363192ba8b7769008bfdbd071679a2cdc40e2fe0c17a83720.jpg)

**This is alpha quality software! Expect the API to change and break existing projects. You can get great results from this system, but only use it for one-offs you don't mind never being able to edit with future versions of Synth Printer.**

It's based on [CadQuery](https://github.com/CadQuery/cadquery), but provides a greatly simplified syntax focusing only on synth panels. It's meant to create panels that print right out of the box: they account for tolerances, and they provide footprints that match the kind of synth diy hardware you'll find in the wild. I've made a lot of panels using this system already. My goal is to make it so things will fit on your first attempt.

It's very much for the sort of DIY builds that use prototype boards, or PCBs mounted perpendicularly and wired to the panel. For the sort of DIY builds with sandwiched PCBs mounted in parallel, there's no guarantee the footprints will fit.

Due to its very limited audience, this system is very minimal, hacky, and rough around the edges. Still, it should be easy to learn how to get it going, and I'm happy to help if it gives you trouble. Synth Printer mostly focuses on my own needs: I build in the Kosmo format, which is bigger than Eurorack, so I tend to use bigger hardware options, such as big 6.3mm jacks.

To get started, you need a way to use CadQuery. I strongly recommend you simply use a [Cq-Editor binary release](https://github.com/CadQuery/CQ-editor/releases). It bundles all you need, there's nothing else to install.

After that, [download this repository](https://github.com/AriaSalvatrice/synth-printer/archive/refs/heads/master.zip), and load up one of the examples in that editor. Use the **▶ Render** button (F5) to run the code. Rotate the viewport, as you'll be seeing the panel from the back by default. You can toggle the preview layer in the outliner to see the panel better.

You can edit code right from CQ-Editor, but if you find it limiting, you can enable autoreload in the preferences, and edit the files from an external editor. You can  design a panel simply by modifying an example, but take a look at synthprinter.py: the functions are full of useful comments, telling you which hardware they fit, and why some values were chosen.

My goal is to provide default settings that fit in mosts cases. But if stuff won't fit, you can override any default setting in the constructor, the examples will show you how.

Once you're ready to export your panel, select it in the viewport, and pick "Tools➔Export as STL". Make sure not to also export the preview layer!


# 3D printing advice for synth panels

## Choosing the material

Common options are PLA, PETG, and ABS. 

| 🐶🎺 | PLA | PETG | ABS |
|-------|-----|------|-----|
| **Cost** | Cheap | Cheap | Affordable |
| **Bed adhesion** | Easy | Easy | Requires adhesive (ABS slurry or glue) |
| **Ease of printing** | Easiest | Easy | Hard, requires an enclosure |
| **Toxicity** | Safe | Safe | Requires proper ventilation while printing |
| **Print visual quality** | Good | Poor | Good, excellent after acetone vapor smoothing |
| **Strength** | Good | Good | Excellent |
| **Heat resistance** | Mediocre | Poor | Good |
| **UV resistance** | Mediocre | Good | Poor |

Personally, I use PLA. It looks great and is easy to print. But if I were to leave it in a hot car, my synth would be destroyed.

## Solidity

I picked the default thickness of 4mm for a reason! Even at 100% infill, it still bends a little when I unplug jacks. Still, it's solid enough.

Let's review what goes into making a solid front plate:

- Print orientation: 3D prints are weaker to shearing forces along their vertical layer lines. Not a problem for a panel printed flat, but that means any vertical supports added in the back will be particularly weak.
- Shell thickness: Probably even more important than infill. You might want to have 5 of them.
- Infill: Not every infill type is resistant to the same type of forces. I generally use 100% infill anyway, except for translucent filaments where I want to achieve a special texture when it's backlit.

## Choosing the best orientation

### Printing the front as first layer, upside-down

- This is my preferred way of printing panels.
- By printing in this orientation, you can add supports for the PCB on the back. I often use a support lattice to which I secure the PCBs with self-locking ties. Note that Synth Printer has no built-in support for them yet, but it's planned. You can just add a support mesh in your slicer, for now.
- You need to achieve a good first layer. There's no secret, it requires a properly tuned printer, a perfectly leveled bed (a depth probe really helps with this), and a perfectly dialed in Z-offset. 
- Print on smooth glass if you can! If you have a textured glass bed, it's safe to flip it over and just print on the untextured side. This will tremendously improve the print quality. You might want to add just a touch of hair spray if heat isn't enough to hold things in place.
- You can achieve neat light reflection tricks by using an interesting bottom fill pattern. I often use the concentric one. The effect is dramatic when used with a Silk filament!
- Wanna use a beautiful but expensive specialty filament for your faceplates? Just swap filament after 5~6 layers! Do the visible layers with your fancy filament, and the rest with bargain bin stock. 
- After the first layer, it's safe to use the highest layer height your printer supports, we don't care about vertical accuracy. 
- After the first few layers, it's also safe to bump up your printing speed, up to the maximum you know your rig can handle. 

### Printing the front as last layer

- With a poorly tuned or low quality printer, this orientation will yield better results.
- Consider enabling ironing in your slicer settings! It takes a long while, but can achieve an incredibly smooth surface. It's particularly good if you want to decorate your panel with acrylic paint (POSCA markers are a favorite for this).
- You can add decorations in relief, and change filaments to have labels! But note that at Eurorack sizes, it's almost impossible to have text labels that look any decent. Synth Printer has no support for embossings yet, so you'll have to edit the STL with other software.
- The recessed areas on the back will look visually nastier, and be less deep, but shouldn't require supports.
- Of course, you can't add supports in the back with this orientation. 

## Printing knobs

I had good results with [Sebajom's OpenSCAD knob generators on thingiverse](https://www.thingiverse.com/sebajom/designs).

# Gallery

![](https://fedi.aria.dog/media/48111bbf4051e198cf090cd38726a9b97886c05f6974ec72be4ca06e06b9a480.jpg) ![](https://fedi.aria.dog/media/958b5eb5111a63c637f5c32a8a06463c2148161ee46ddcce65a444be3fb37278.jpg)

# Contributing

How much this project will be updated very much depends whether other people use it at all. 

You can help by: 

- Reporting your successes and failures
- Contributing footprints that worked out for you 
- Making the code less bad (but let's keep it simple)

# Contact

I insist to see whatever you make with this system! You can send me pics of your contraptions and dog gifs at [woof@aria.dog](mailto:woof@aria.dog). I'm also on the Fediverse (Mastodon-compatible): [@woof@aria.dog](https://fedi.aria.dog/woof).

toodles, 

![Aria Salvatrice](https://github.com/AriaSalvatrice/synth-protoboard/blob/master/Images/signature.png?raw=true)


