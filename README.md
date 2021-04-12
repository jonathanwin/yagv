# yagv - Yet Another Gcode Viewer, v0.5.1

A fast 3D Gcode Viewer for Reprap-style 3D printers, in Python and OpenGL (via pyglet)

## Supported Platforms
- Ubuntu Linux 20.04 LTS
- expected to work in any Linux, Windows or OS X

![Screenshot](img/screenshot.png)

## Installation
```
% python3 setup.py install
 - OR -
% sudo python3 setup.py install
```

## Usage:

```
% yagv [file.gcode]
```
* By default, open data/hana_swimsuit_fv_solid_v1.gcode if no file specified

## Features:

* Colors segments according to their type:
  * extruding
  * flying the head to the next extrusion point
  * retracting filament
  * restoring filament
* Allows displaying layers independently to examine them.
* Automagically splits the gcode into layers.
* Automatic scaling to fit the window.
* Zoom, panning and rotation

## Issues:

* Retract/restore detected but invisible (0-length segments).
* Designed with Slic3r output in mind, may not support other slicing programs (suggestions/patches welcome).
* Some gcodes unsupported, in particular:
  * G20: Set Units to Inches (usage unknown) 
  * Arcs (G2 & G3 ?)
