all::	3DBenchy Voron_Design_Cube_v7 overhang3l4mm

3DBenchy::
	slic3r --gcode-comments 3DBenchy.stl -o 3DBenchy-slic3r-1.2.9.gcode
	prusa-slicer --gcode-comments -s 3DBenchy.stl -o 3DBenchy-prusa-slicer-2.1.1.gcode
	cura-slicer --machine-width=200 --machine-depth=200 3DBenchy.stl -o 3DBenchy-CuraEngine-4.4.1.gcode
	mandoline -n --no-support 3DBenchy.stl -o 3DBenchy-mandoline-0.8.5.gcode

Voron_Design_Cube_v7::
	slic3r --gcode-comments Voron_Design_Cube_v7.stl -o Voron_Design_Cube_v7-slic3r-1.2.9.gcode
	prusa-slicer --gcode-comments -s Voron_Design_Cube_v7.stl -o Voron_Design_Cube_v7-prusa-slicer-2.1.1.gcode
	cura-slicer --machine-width=200 --machine-depth=200 Voron_Design_Cube_v7.stl -o Voron_Design_Cube_v7-CuraEngine-4.4.1.gcode
	mandoline --no-support Voron_Design_Cube_v7.stl -o Voron_Design_Cube_v7-mandoline-0.8.5.gcode

overhang3l4mm::
	slic3r --support-material --support-material-angle=30 --gcode-comments overhang3l4mm.stl -o overhang3l4mm-slic3r-1.2.9.gcode
	prusa-slicer --support-material --gcode-comments -s overhang3l4mm.stl -o overhang3l4mm-prusa-slicer-2.1.1.gcode
	cura-slicer --machine-width=200 --machine-depth=200 --support_enable=true overhang3l4mm.stl -o overhang3l4mm-CuraEngine-4.4.1.gcode
	mandoline -n --support-all overhang3l4mm.stl -o overhang3l4mm-mandoline-0.8.5.gcode
	slicer4rtn --subdivide=5 overhang3l4mm.stl --output=overhang3l4mm-slicer4rtn-0.4.4.gcode

