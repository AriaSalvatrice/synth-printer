# Todo-List

See also the "FIXME:" and "TODO:" in the code itself.

Most of this should be addressed before I can call it version 1.

## Consistency

- Verify all the language is consistent
- Every addXXX / rect type function should default to center of footprint and have an option to center on top-left instead
  - Good progress on that

## Better code

- Improve the dirty parts of the CadQuery code. It might be a mess but it works.
  - I will never do ths lol
- Figure out a less nasty way to chamfer the display window
- Break the library into multiple files
  - It's difficult, Python's import is asjkddfs;klgjsdf;klgjc
- Reorganize the files better
- Figure out if I can make this a better neighbor - behave more like a normal Python library does, not sure what it'd even entail.
  - Look the standard operating procedure for python code is to make a 30GB venv and download junk off the internte silently and still manage to break stuff globally. This is already plenty good by Python's standards.

## Footprints

- Rotary Encoders
- More types of common buttons and switches
- DPDT version of the MTS
- Rectangular holes with rounded corners
- Previews of the rails clearance
- Place stuff at arbitrary angles, not just "horizontal" and "vertical"
- Screw sizes for displays
- Free-standing screws

## Eurorack-specific stuff

- Remove more from the side of Eurorack panels (cf. Doepfer specs)

## Engraving

- engraveLineTo() that takes toX toY
- Potentiometer ranges

## Embossing

- Embossing layer
- Text labels, but if I can't offer quality, I don't want to offer it at all, and you will NOT get quality at eurorack sizes with FDM. Maybe at Kosmo sizes, but even then it will look nasty. In general, text will turn out two extrusions wide, which is not enough.

## Supports

- Integrate the support lattice I've been using in my prints. It needs to be cached, it takes too long to generate.
- Other types of perpendicular supports

## Drill Templates

- Clean SVG Export for drill templates ready to print at 1:1 size
- Display the mounting slots on the drill template

## KiCAD Templates

- SVG Export the perfect size for KiCAD (I have good results at 0.324 scale)

## Other types of printouts

- Printing labels on stickers / transparencies
- FDM toner transfer

## CNC

- Figure out how to make the project more useful for DXF / CNC processes. Without the help of someone who uses CNC, not much I can do.

## Make it work in the browser

- Add a jupyter notebook thing. Sounds daunting to implement, but people would really prefer not to have to install anything to play with this. There's already a CQ renderer for Jupyter. And Jupyter would have autocomplete, CQ editor has none.
- Despite my stating it outright, people on ModWiggler didn't understand there's no Python dependency hell to wrangle to use Synth Printer! I need to de-empasize that it uses Python, and instead emphasize that there's "Nothing To Install".
- Have the viewport or model rotated in a way that make sense by default.

## Documentation

- Improve the documentation in general
- Move the documentation to its own website / integrated to Jupyter thing
- Provide more examples
- Have a better logical progression of examples
- Record a demo video for version 1
- Politely ask for monies why the hell not

## Guitar pedals?

- Would be a natural thing to do but not for V1
