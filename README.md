# Synth Printer: WIP Experiment with CadQuery

**This is not ready for general use yet!**

These are experiments with CadQuery to make 3D printed synth panels. 

I don't really know python btw, I just did enough hacks with it to have kinda picked it up by accident. 

If you wanna play with it, just load testpanel.py in CQ-editor.

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