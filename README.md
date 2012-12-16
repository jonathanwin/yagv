# yagv - Yet Another Gcode Viewer, v0.3

A fast 3D Gcode Viewer for Reprap-style 3D printers, in Python and OpenGL (via pyglet)

Designed in Ubuntu Linux; Expected to work in any Linux, Windows or OS X

## Requires:

* python 2.x (2.7.3 tested)
  http://python.org/
* pyglet 1.1+ (1.1.4 tested)
  http://www.pyglet.org

## Usage:

yagv file.gcode

## Features:

* Colors segments according to their type:
  * extruding
  * flying the head to the next extrusion point
  * retracting filament
  * restoring filament
* Allows displaying layers independently to examine them.
* Automagically splits the gcode into layers.
* Automatic scaling to fit the window.
* Zoom and rotation (Panning planned).

## Issues:

* Panning for close inspection not yet supported.
* Retract/restore detected but invisible (0-length segments).
* Designed with Slic3r output in mind, may not support other slicing programs (suggestions/patches welcome).
* Some gcodes unsupported:
  * G91: Set to Relative Positioning (used by some slicers)
  * G20: Set Units to Inches (usage unknown) 
  * Arcs (G2 & G3 ?)
