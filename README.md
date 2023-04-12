# Synth Printer: WIP Experiment with CadQuery

**This is not ready for general use yet!**

I don't really know python btw, I just did enough hacks with it to have kinda picked it up by accident. 

-----------------

Hey kid, wanna extrude a synth?

Synth Printer is a very very lightweight system letting you create faceplates for your DIY modular synthesizer, using simple Python code — code so simple you don't need to know any Python at all (a bit of experience with any programming language will be enough).

It's based around [CadQuery](https://github.com/CadQuery/cadquery), but provides a greatly simplified syntax focusing only on synth panels. It's meant to create panels that print right out of the box: they account for tolerances, and they provide footprints that match the kind of synth diy hardware you'll find in the wild. I've made a lot of panels using this system already. My goal is to make it so things will fit on your first attempt.

It's very much for the sort of DIY builds that use prototype boards, or PCBs mounted perpendicularly and wired to the panel. It's not really meant for the sort of DIY builds with sandwiched PCBs mounted in parllel. 

Due to its very limited audience, this system is very minimal, hacky, and rough around the edges. Still, it should be easy to learn how to get it going, and I'm happy to help if it gives you trouble. Synth Printer mostly focuses on my own needs: I build in the Kosmo format, which is bigger than Eurorack, so I tend to use bigger hardware options, such as big 6.3mm jacks. How much this project will be updated very much depends whether other people use it at all.

To get started, you need a way to use CadQuery. I strongly recommend you simply use [Cq-Editor](https://github.com/CadQuery/CQ-editor) (grab a binary release).

After that, [download this repository](https://github.com/AriaSalvatrice/synth-printer/archive/refs/heads/master.zip), and load up one of the examples. Use the **▶ Render** button (F5) to run the code. Rotate the viewport, as you'll be seeing the panel from the back by default. 

You can edit code right from CQ-Editor, but if you find it limiting, you can enable autoreload in the preferences, and edit the files from an external editor. You can probably design a panel simply by modifying an example!

If stuff won't fit, you can modify the values in synthprinter.py, or use it as an inspiration to create your own functions.

_FIXME: there are no examples yet lol. just testpanel.py_

Once you're ready to export your panel, select it in the viewport, and pick "Tools -> Export as STL"


# How to print [TODO]
- Print as exported, exposed face down
- Well tuned printer is important
- Use a non-textured bed, if it's glass flip it over
- Using infills to achieve special effects (concentric + silk)
- PLA vs PETG vs ABS (PLA is solid enough but can melt)
- [Making knobs](https://www.thingiverse.com/sebajom/designs)


# Todo-List

- [ ] Figure out a decent "architecture" that's simple & close to natural language
  - Just going with a collection of functions, but maybe i can integrate it to CadQuery's fluent API?
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