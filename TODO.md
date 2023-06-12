# Todo-List

See also the "FIXME:" and "TODO:" in the code itself.

- [ ] Make more footprints!
  - [ ] Vertical slider
- [ ] Better support for engraving
  - [ ] Potentiometer ranges
- [ ] Support for embossing
  - For text labels, If I can't offer quality, I don't want to offer it at all, and you will NOT get quality at eurorack sizes. Maybe at Kosmo sizes, but even then it will look nasty. In general, text will turn out two extrusions wide, which is not enough. 
- [ ] Integrate the support lattice I've been using in my prints. It needs to be cached too, it takes too long to generate.
- [ ] Other types of perpendicular supports
- [ ] Provide more examples
- [ ] Figure out a less nasty way to chamfer the display window
- [ ] Improve the documentation.
- [ ] Export an API documentation. There's already detailed docstrings so i can prolly just use some off the shelf system.
- [ ] Add a jupyter browser system? Sounds daunting to implement, but people would really prefer not to have to install anything to play with this. There's already a CQ renderer for Jupyter. And Jupyter would have autocomplete, CQ editor has none.
- [ ] SVG Export for drill templates, printing labels, and FDM toner transfer.
- [ ] Figure out how to make the project more useful for DXF / CNC processes
- [ ] Implement width tolerance for panels—without messing up the user-facing coordinates. It's not really neede for Kosmo since it uses 5cm on a 5.08 grid, but it's probably required for Eurorack stuff.
- [ ] Break the library into multiple files
- [ ] Record a demo video for version 1