# yagv - Yet Another Gcode Viewer, v0.5.8

A fast 3D Gcode Viewer for Reprap-style 3D printers, in Python and OpenGL/pyglet

![Screenshot](img/screenshot.png)

## Features

* Colors segments according to their type:
  * extruding (wall, infill, support if G-code comments are enabled in slicer)
  * motion of the head to the next extrusion point
  * retracting filament
  * restoring filament
* Allows displaying layers independently to examine them (scroll up & down)
* Automagically splits the Gcode into layers
* Automatic scaling to fit the window
* Zoom, panning and rotation (same mouse-button layout as OpenSCAD)
* Supported slicers:
  * [Slic3r](https://slic3r.org/) 1.2.9: works
  * [PrusaSlicer](https://www.prusa3d.com/prusaslicer/) 2.1.1: works
  * [Cura](https://ultimaker.com/software/ultimaker-cura) 4.x: works
  * [Mandoline](https://github.com/Spiritdude/mandoline-py) 0.8.x: works
  * [Slicer4RTN](https://github.com/Spiritude/Slicer4RTN) 0.4.x: works (non-planar slices)
* Day/Night mode (`--dark`)
  
## Supported Platforms
- Ubuntu Linux 20.04 LTS [confirmed]
- Expected to work in any Linux, Windows or macOS

## Installation
```
% python3 setup.py install
 - OR -
% sudo python3 setup.py install
```

## Usage

```
% yagv [file.gcode]

% yagv --help
USAGE yagv 0.5.4: [<opts>] file.gcode
   options:
      --help               display this message
      --dark               enable dark mode
      --bed-size=<w>x<h>   set bed size (e.g. 200x240)
                     
```
By default, opens `data/hana_swimsuit_fv_solid_v1.gcode` if no file specified

## Issues

* ~~Zoom & Panning don't work well together, zoom in/out changes focus center~~ resolved in 0.5.3
* Retract/restore detected but invisible (0-length segments).
* Some GCodes unsupported, in particular:
  * G20: Set Units to Inches
  * ~~G2 & G3: Arcs~~ resolved in 0.5.8
  
## Changes
* 0.5.8: support added for G2/G3 arc extrusions as used by ArcWelder, CHANGELOG added
* 0.5.4: better parsing arguments, adding `--dark` mode added
* 0.5.3: better support for Cura, Slic3r, PrusaSlicer and Mandoline distincting perimeter/wall/shell, infill and support extrusion (e.g. `;TYPE:...` Gcode comments); new mouse-button layout to match OpenSCAD
* 0.5.2: new color scheme (white bg, green extrusion, red active layer), display layer# with z [mm]
* 0.5.1: `setup.py` with proper pyglet version to match code (pre-2.0), drawing bed grid
* 0.5.0: ported to Python3, added panning, smaller font

## More Examples
### Support Structure
![Screenshot](img/screenshot-support.png)
Given `--gcode-comments` is enabled for Slic3r and PrusaSlicer.

### Non-Planar Slices
![Screenshot](img/screenshot-nonplanar.png)
Gcode from [Slicer4RTN](https://github.com/Spiritdude/Slicer4RTN), conic/tilted slicer for 4- and 5-axis FDM printers

