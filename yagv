#!/usr/bin/env python

YAGV_VERSION = "0.5.8"        # -- check Makefile and setup.py too

import pyglet
import math

# Disable error checking for increased performance
pyglet.options['debug_gl'] = False

from pyglet import clock
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse

from gcodeParser import *
import os.path
import time

colorMap = {
	# Misc:
	"background": [ 1,1,1, 1. ],
	"grid": [ .2,.2,.2, 1. ],
	"text": [ 0,0,0, 1. ],

   # Gcode:
	"extrude": [ 0.,.8,0. ],
	"extrude_active": [ .8,0.,0. ],
	"extrude_wall": [ .2,.9,0. ],
	"extrude_wall_active": [ .8,.5,0. ],
	"extrude_support": [ .8,.8,0. ],
	"extrude_support_active": [ 1,.9,0. ],
	"retract": [ .8,.8,0. ],
	"unretract": [ .8,0.,.8 ],
	"motion": [ 0.,0.,1. ]
}

def preg_match(rex,s,m,opts={}):
	_m = re.search(rex,s)
	m.clear()
	if _m:
		m.append(s)
		m.extend(_m.groups())
		return True
	return False
                              
class App:
	def __init__(self):
		self.RX = 0.0
		self.RZ = 0.0
		self.PX = 0.0
		self.PY = 0.0
		self.zoom = 1.0
		self.conf = { }
		self.conf['bed_size'] = [ 200, 200 ]
	
	def main(self):
		
		#### MAIN CODE ####
		import sys

		path = ''

		i = 1
		while(i<len(sys.argv)):
			m = [ ]
			if preg_match('^--([\w\-]+)=(.*)$',sys.argv[i],m):
				m[1] = m[1].replace('-','_')
				self.conf[m[1]] = m[2]
			elif preg_match('^--([\w\-]+)$',sys.argv[i],m):
				m[1] = m[1].replace('-','_')
				self.conf[m[1]] = 1
			else:
		 		path = sys.argv[i]
			i += 1

		if 'help' in self.conf and self.conf['help']:
			print("""USAGE yagv %s: [<opts>] file.gcode
   options:
      --help               display this message
      --dark               enable dark mode
      --bed-size=<w>x<h>   set bed size (e.g. 200x240)
""" % YAGV_VERSION)
			sys.exit(0)
		if 'dark' in self.conf and self.conf['dark']:
			colorMap['background'] = [ 0,0,0, 1 ]
			colorMap['grid'] = [ 1,1,1, 0.1 ]
			colorMap['text'] = [ 1,1,1, 0.7 ]

		if type(self.conf['bed_size'])==str:
			self.conf['bed_size'] = list(map(lambda x: int(x),self.conf['bed_size'].split('x')))
			print(self.conf['bed_size'])

		if len(path)==0:
			script_path = os.path.realpath(__file__)
			script_dir = os.path.dirname(script_path)
			path = os.path.join(script_dir, "data/hana_swimsuit_fv_solid_v1.gcode")
			# WTF setuptools: no easy way to access EGG internal data file, we installed it in /usr/local/share/yagv/ instead :-(
			path = "/usr/local/share/yagv/data/hana_swimsuit_fv_solid_v1.gcode"

		print("Yet Another GCode Viewer v%s"%YAGV_VERSION)

		self.path = "loading ..."

		# -- create window soon, before loading ...
		self.window = MyWindow(self, caption="Yet Another GCode Viewer v%s: %s" % (YAGV_VERSION,os.path.basename(path)), resizable=True, width=1024, height=768)
		pyglet.gl.glClearColor(colorMap['background'][0],colorMap['background'][1],colorMap['background'][2],1)

		# debug: log all events
		# self.window.push_handlers(pyglet.window.event.WindowEventLogger())

		self.load(path)

		# default to the middle layer
		self.layerIdx = len(self.model.layers)//2
		self.window.hud()

		#img = pyglet.resource.image("icon.png")
		#img = pyglet.image.load("/usr/local/share/yagv/icon.png")
		#self.window.set_icon(img)

		pyglet.app.run()

	def reload(self):
		self.load(self.path)
			
	def load(self, path):
		
		print("loading file %s ..." % repr(path))
		t1 = time.time()
		
		print("Parsing '%s'..." % path)
		
		self.path = path

		parser = GcodeParser()
		self.model = parser.parseFile(path)

		print("Done! %s" % self.model)
		
		# render the model
		print("rendering vertices...")
		self.renderVertices()
		print("rendering indexed colors...")
		self.renderIndexedColors()
		print("rendering true colors...")
		self.renderColors()
		print("generating graphics...")
		self.generateGraphics()
		print("Done")
		
		t2 = time.time()
		print("loaded file in %0.3f ms" % ((t2-t1)*1000.0 ))
	
	def renderVertices(self):
		t1 = time.time()
		
		self.vertices = []

		for layer in self.model.layers:
			
			layer_vertices = []
			
			x = layer.start["X"]
			y = layer.start["Y"]
			z = layer.start["Z"]
			for seg in layer.segments:
				layer_vertices.append(x)
				layer_vertices.append(y)
				layer_vertices.append(z)
				x = seg.coords["X"]
				y = seg.coords["Y"]
				z = seg.coords["Z"]
				layer_vertices.append(x)
				layer_vertices.append(y)
				layer_vertices.append(z)

			self.vertices.append(layer_vertices)
			#layer.end['X'] = layer_vertices[:3]
			#layer.end['Y'] = layer_vertices[:2]
			#layer.end['Z'] = layer_vertices[:1]
			
		t2 = time.time()
		print("end renderColors in %0.3f ms" % ((t2-t1)*1000.0, ))
	
	def renderIndexedColors(self):
		t1 = time.time()
		# pre-render segments to colors in the index
		styleToColoridx = {
			"extrude" : 0,
			"fly" : 1,
			"retract" : 2,
			"restore" : 3,
	  		"extrude.wall": 4,
			"extrude.support": 5
			}
		
		# all the styles for all layers
		self.vertex_indexed_colors = []
		
		# for all layers
		for layer in self.model.layers:
			
			# index for this layer
			layer_vertex_indexed_colors = []
			for seg in layer.segments:
				# get color index for this segment
				if seg.style == 'extrude' and (seg.type == 'G1:wall' or seg.type == 'G1:shell' or seg.type == 'G1:perimeter' or seg.type.find('shell') or seg.type.find('shell')):
					styleCol = styleToColoridx['extrude.wall']
				elif seg.style == 'extrude' and seg.type == 'G1:support':
					styleCol = styleToColoridx['extrude.support']
				else:
					styleCol = styleToColoridx[seg.style]
				# append color twice (once per end)
				layer_vertex_indexed_colors.extend((styleCol, styleCol))
			
			# append layer to all layers
			self.vertex_indexed_colors.append(layer_vertex_indexed_colors)
		t2 = time.time()
		print("end renderIndexedColors in %0.3f ms" % ((t2-t1)*1000.0, ))
	
	def renderColors(self):
		t1 = time.time()
		
		self.vertex_colors = [[],[],[]]
		
		# render color index to real colors
		cm = [ 
			# 0: old layer
			[ colorMap['extrude'].copy(),        colorMap['motion'].copy(), colorMap['retract'].copy(), colorMap['unretract'].copy(), colorMap['extrude_wall'].copy(), colorMap['extrude_support'].copy() ],
			# 1: current layer
			[ colorMap['extrude_active'].copy(), colorMap['motion'].copy(), colorMap['retract'].copy(), colorMap['unretract'].copy(), colorMap['extrude_wall_active'].copy(), colorMap['extrude_support_active'].copy() ],
			# 2: limbo layer
			[ colorMap['extrude'].copy(),        colorMap['motion'].copy(), colorMap['retract'].copy(), colorMap['unretract'].copy(), colorMap['extrude_wall'].copy(), colorMap['extrude_support'].copy() ]
		]
		for i in range(6):         # -- add per type the alpha
			cm[0][i].append(.2 if i==1 or i==5 else .7)    # -- old
			cm[1][i].append(.2 if i==1 else 1.)    # -- current
			cm[2][i].append(.1)    # -- limbo
		
		# for all 3 types
		for display_type in range(3):
			
			#type_color_map = cm[display_type]

			# -- cumbersome float -> int color
			type_color_map = []
			n = 0
			for c in cm[display_type]:
				type_color_map.append([])
				for i in range(4):
					type_color_map[n].append(int(c[i]*255))
				n += 1

			# for all preindexed layer colors
			for indexes in self.vertex_indexed_colors:
				
				# render color indexes to colors
				colors = list(map(lambda e: type_color_map[e], indexes))
				# flatten color values
				fcolors = []
				list(map(fcolors.extend, colors))
				
				# push colors to vertex list
				self.vertex_colors[display_type].append(fcolors)
				
		t2 = time.time()
		print("end renderColors in %0.3f ms" % ((t2-t1)*1000.0, ))
	
	def generateGraphics(self):
		t1 = time.time()
		
		self.graphics_old = []
		self.graphics_current = []
		self.graphics_limbo = []
		
		for layer_idx in range(len(self.vertices)):
			nb_layer_vertices = len(self.vertices[layer_idx])//3
			vertex_list = pyglet.graphics.vertex_list(nb_layer_vertices,
				('v3f/static', self.vertices[layer_idx]),
				('c4B/static', self.vertex_colors[0][layer_idx])
			)
			self.graphics_old.append(vertex_list)
			
			vertex_list = pyglet.graphics.vertex_list(nb_layer_vertices,
				('v3f/static', self.vertices[layer_idx]),
				('c4B/static', self.vertex_colors[1][layer_idx])
			)
			self.graphics_current.append(vertex_list)
			
			vertex_list = pyglet.graphics.vertex_list(nb_layer_vertices,
				('v3f/static', self.vertices[layer_idx]),
				('c4B/static', self.vertex_colors[2][layer_idx])
			)
			self.graphics_limbo.append(vertex_list)
		#	print(nb_layer_vertices, len(self.vertices[layer_idx]), len(self.colors[0][layer_idx]))
		
		t2 = time.time()
		print("end generateGraphics in %0.3f ms" % ((t2-t1)*1000.0, ))
		
	# -- rotate		
	def rotate_drag_start(self, x, y, button, modifiers):
		self.rotateDragStartRX = self.RX
		self.rotateDragStartRZ = self.RZ
		self.rotateDragStartX = x
		self.rotateDragStartY = y

	def rotate_drag_do(self, x, y, dx, dy, buttons, modifiers):
		# deltas
		deltaX = x - self.rotateDragStartX
		deltaY = y - self.rotateDragStartY
		# rotate!
		self.RZ = self.rotateDragStartRZ + deltaX/5.0 # mouse X bound to model Z
		self.RX = self.rotateDragStartRX + deltaY/5.0 # mouse Y bound to model X

	def rotate_drag_end(self, x, y, button, modifiers):
		self.rotateDragStartRX = None
		self.rotateDragStartRZ = None
		self.rotateDragStartX = None
		self.rotateDragStartY = None

	def layer_drag_start(self, x, y, button, modifiers):
		self.layerDragStartLayer = self.layerIdx
		self.layerDragStartX = x
		self.layerDragStartY = y

	def layer_drag_do(self, x, y, dx, dy, buttons, modifiers):
		# sum x & y
		delta = x - self.layerDragStartX + y - self.layerDragStartY
		# new theoretical layer
		self.layerIdx = int(self.layerDragStartLayer + delta//5)
		# clamp layer to 0-max
		self.layerIdx = max(min(self.layerIdx, self.model.topLayer), 0)
		self.layer_update()
		
	#	# clamp layer to 0-max, with origin slip
	#	if (self.layerIdx < 0):
	#		self.layerIdx = 0
	#		self.layerDragStartLayer = 0
	#		self.layerDragStartX = x
	#		self.layerDragStartY = y
	#	if (self.layerIdx > len(self.model.layers)-1):
	#		self.layerIdx = len(self.model.layers)-1
	#		self.layerDragStartLayer = len(self.model.layers)-1
	#		self.layerDragStartX = x
	#		self.layerDragStartY = y

	# -- layer select		
	def layer_update(self):
		#self.window.layerLabel.text = "layer %d (z=%.2f)" % (self.layerIdx,self.model.layers[self.layerIdx].start['Z'])
		if self.model.layers[self.layerIdx].bbox.zmin != self.model.layers[self.layerIdx].bbox.zmax:
			self.window.layerLabel.text = "layer %d (z=%.2f..%.2f)" % (self.layerIdx,self.model.layers[self.layerIdx].bbox.zmin,self.model.layers[self.layerIdx].bbox.zmax)
		else:
			self.window.layerLabel.text = "layer %d (z=%.2f)" % (self.layerIdx,self.model.layers[self.layerIdx].start['Z'])
		#print(self.model.layers[self.layerIdx].bbox.zmin)

	def layer_up(self):
		self.layerIdx = max(min(self.layerIdx+1, self.model.topLayer), 0)
		self.layer_update()

	def layer_down(self):
		self.layerIdx = max(min(self.layerIdx-1, self.model.topLayer), 0)
		self.layer_update()

	def layer_bottom(self):
		self.layerIdx = min(1, self.model.topLayer)
		self.layer_update()

	def layer_top(self):
		self.layerIdx = self.model.topLayer
		self.layer_update()

	def layer_drag_end(self, x, y, button, modifiers):
		self.layerDragStartLayer = None
		self.layerDragStartX = None
		self.layerDragStartY = None

	# -- panning
	def panning_start(self, x, y, button, modifiers):
		self.panningStartPX = self.PX
		self.panningStartPY = self.PY
		self.panningStartX = x
		self.panningStartY = y

	def panning_do(self, x, y, dx, dy, buttons, modifiers):
		# deltas
		#deltaX = x - self.panningStartX
		#deltaY = y - self.panningStartY
		# -- panning done with proper rotation
		deltaX = math.cos(-self.RZ/180*math.pi) * (x - self.panningStartX) + math.sin(self.RZ/180*math.pi) * (y - self.panningStartY)
		deltaY = math.sin(-self.RZ/180*math.pi) * (x - self.panningStartX) + math.cos(self.RZ/180*math.pi) * (y - self.panningStartY)
		# pan!
		f = 5
		self.PX = self.panningStartPX + deltaX/f # mouse X bound to model X
		self.PY = self.panningStartPY + deltaY/f # mouse Y bound to model Y

	def panning_end(self, x, y, button, modifiers):
		self.panningStartX = None
		self.panningStartY = None


def glLine(p1,p2,c):
	glBegin(GL_LINES)
	glColor4f(c[0],c[1],c[2],c[3])
	glVertex3f(p1[0],p1[1],p1[2])
	glVertex3f(p2[0],p2[1],p2[2])
	glEnd()
	
class MyWindow(pyglet.window.Window):

	# constructor
	def __init__(self, app, **kwargs):
		pyglet.window.Window.__init__(self, **kwargs)
		self.app = app
		#self.hud()
	
	# hud info
	def hud(self):
		
		# HUD labels
		self.blLabels = []
		self.brLabels = []
		self.tlLabels = []
		self.trLabels = []

		c_texti = list(map(lambda x: int(x*255), colorMap['text']))
		#self.brLabels.append(pyglet.text.Label("yagv "+YAGV_VERSION,font_size=10,color=c_texti,anchor_x='right', anchor_y='bottom'))
      
		# help
		self.helpText = [
						"Left-mouse: rotate | Middle: change layer, Scroll: zoom | Right: panning   Ctrl-R: reload"]
		for txt in self.helpText:
			self.blLabels.append(
				pyglet.text.Label(	txt,
									font_size=10,color=c_texti) )

		# statistics
		## model stats
		self.statsLabel = pyglet.text.Label(	"",
										font_size=10,color=c_texti,
										anchor_y='top')
		filename = os.path.basename(self.app.path)
		self.statsLabel.text = "%s: %d layers (%d segments), %.1fm filament" % (filename, len(self.app.model.layers), len(self.app.model.segments), self.app.model.extrudate/1000.0)
		
		## fps counter
		self.fpsLabel = pyglet.text.Label(	"",
										font_size=10,color=c_texti,
										anchor_y='top')
		self.tlLabels.append(self.statsLabel)
		#self.tlLabels.append(self.fpsLabel)

		# status
		## current Layer
		self.layerLabel = pyglet.text.Label(	"layer %d (z=%.2f)" % (
			self.app.layerIdx,
			self.app.model.layers[self.app.layerIdx].start['Z'],
			#self.app.model.layers[self.app.layerIdx].end['Z']
			#self.app.model.layers[self.app.layerIdx].bbox.zmin,
			#self.app.model.layers[self.app.layerIdx].bbox.zmax
			), font_size=10,color=c_texti,anchor_x='right', anchor_y='top')
		self.trLabels.append(self.layerLabel)

		# layout the labels in the window's corners
		self.placeLabels(self.width, self.height)
	
	
	# events
	def on_resize(self, width, height):
		glViewport(0, 0, width, height)
		self.placeLabels(width, height)
		#self.render(width, height)
		
		return pyglet.event.EVENT_HANDLED

	def on_mouse_press(self, x, y, button, modifiers):
		#print("on_mouse_press(x=%d, y=%d, button=%s, modifiers=%s)"%(x, y, button, modifiers))
		if button & mouse.LEFT:
			self.app.rotate_drag_start(x, y, button, modifiers)
			
		if button & mouse.MIDDLE:
			self.app.layer_drag_start(x, y, button, modifiers)

		if button & mouse.RIGHT:
			self.app.panning_start(x, y, button, modifiers)


	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		#print("on_mouse_drag(x=%d, y=%d, dx=%d, dy=%d, buttons=%s, modifiers=%s)"%(x, y, dx, dy, buttons, modifiers))
		if buttons & mouse.LEFT:
			self.app.rotate_drag_do(x, y, dx, dy, buttons, modifiers)
			
		if buttons & mouse.MIDDLE:
			self.app.layer_drag_do(x, y, dx, dy, buttons, modifiers)

		if buttons & mouse.RIGHT:
			self.app.panning_do(x, y, dx, dy, buttons, modifiers)


	def on_mouse_release(self, x, y, button, modifiers):
		#print("on_mouse_release(x=%d, y=%d, button=%s, modifiers=%s)"%(x, y, button, modifiers))
		if button & mouse.LEFT:
			self.app.rotate_drag_end(x, y, button, modifiers)
			
		if button & mouse.MIDDLE:
			self.app.layer_drag_end(x, y, button, modifiers)

		if button & mouse.RIGHT:
			self.app.panning_end(x, y, button, modifiers)

	def on_key_release(self, symbol, modifiers):
		print("pressed key: %s, mod: %s"%(symbol, modifiers))
		#print("pressed key: %s, mod: %s"%(pyglet.window.key.R, pyglet.window.key.MOD_CTRL))

		if symbol==pyglet.window.key.R and modifiers & pyglet.window.key.MOD_CTRL:
			self.app.reload()
		elif symbol==pyglet.window.key.UP:
			self.app.layer_up()
		elif symbol==pyglet.window.key.DOWN:
			self.app.layer_down()
		elif symbol==pyglet.window.key.HOME:
			self.app.layer_bottom()
		elif symbol==pyglet.window.key.END:
			self.app.layer_top()
		else:
			print("pressed key: %s, mod: %s"%(symbol, modifiers))
		
	def placeLabels(self, width, height):
		x = 5
		y = 5
		for label in self.blLabels:
			label.x = x
			label.y = y
			y += 20
			
		x = width - 5
		y = 5
		for label in self.brLabels:
			label.x = x
			label.y = y
			y += 20
			
		x = 5
		y = height - 5
		for label in self.tlLabels:
			label.x = x
			label.y = y
			y -= 20
			
		x = width - 5
		y = height - 5
		for label in self.trLabels:
			label.x = x
			label.y = y
			y -= 20


	def on_mouse_scroll(self, x, y, dx, dy):
		# zoom on mouse scroll
		delta = dx + dy
		if delta == 0:
			return
		z = 1.2 if delta>0 else 1/1.2
		self.app.zoom = max(1.0, self.app.zoom * z)
		#print('mouse scroll:', `x, y, dx, dy`, `z, self.app.zoom`)

	def on_draw(self):
		#print("draw")
		
		# Clear buffers
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		
		# setup projection
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(65, self.width / float(self.height), 0.1, 1000)
		
		# setup camera
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		gluLookAt(0,1.5,2,0,0,0,0,1,0)
		
		# enable alpha blending
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		
		# rotate axes to match reprap style
		glRotated(-90, 1,0,0)

		# user rotate model
		glRotated(-self.app.RX, 1,0,0)
		glRotated(self.app.RZ, 0,0,1)
		
		# Todo check this
		glTranslated(0,0,-0.5)
		
		# fit & user zoom model
		max_width = max(
			self.app.model.bbox.dx(),
			self.app.model.bbox.dy(),
			self.app.model.bbox.dz()
		)
		scale = self.app.zoom / max_width
		glScaled(scale, scale, scale)
		
		# user pan model
		glTranslated(self.app.PX,self.app.PY,0)

		glTranslated(-self.app.model.bbox.cx(), -self.app.model.bbox.cy(), -self.app.model.bbox.cz())
		
		# draw axes
		glBegin(GL_LINES)
		glColor3f(1,0,0)
		glVertex3f(0,0,0); glVertex3f(1,0,0); glVertex3f(1,0,0); glVertex3f(1,0.1,0)
		glVertex3f(1,0,0); glVertex3f(self.app.model.bbox.xmax,0,0)
		glColor3f(0,1,0)
		glVertex3f(0,0,0); glVertex3f(0,1,0); glVertex3f(0,1,0); glVertex3f(0,1,0.1)
		glVertex3f(0,1,0); glVertex3f(0,self.app.model.bbox.ymax,0)
		glColor3f(0,0,1)
		glVertex3f(0,0,0); glVertex3f(0,0,1); glVertex3f(0,0,1); glVertex3f(0.1,0,1)
		glVertex3f(0,0,1); glVertex3f(0,0,self.app.model.bbox.zmax)
		glEnd()
		
		# draw bed grid
		for y in range(0,self.app.conf['bed_size'][1]+1):
			glLine([0,y,0],[self.app.conf['bed_size'][0],y,0],[colorMap['grid'][0],colorMap['grid'][1],colorMap['grid'][2],0.3 if y%10 == 0 else 0.1])
		for x in range(0,self.app.conf['bed_size'][0]+1):
			glLine([x,0,0],[x,self.app.conf['bed_size'][1],0],[colorMap['grid'][0],colorMap['grid'][1],colorMap['grid'][2],0.3 if x%10 == 0 else 0.1])

		# -- draw the model layers
		#    lower layers
		glLineWidth(1)
		for graphic in self.app.graphics_old[0:self.app.layerIdx]:
			graphic.draw(GL_LINES)
		
		#    highlighted layer
		glLineWidth(2)
		graphic = self.app.graphics_current[self.app.layerIdx]
		graphic.draw(GL_LINES)
		
		#    limbo layers
		glLineWidth(1)
		for graphic in self.app.graphics_limbo[self.app.layerIdx+1:]:
			graphic.draw(GL_LINES)
		
		# disable depth for HUD
		glDisable(GL_DEPTH_TEST)
		glDepthMask(0)
		
		# Set your camera up for 2d, draw 2d scene
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity();
		glOrtho(0, self.width, 0, self.height, -1, 1)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		
		self.fpsLabel.text = "%d fps"%int(round(pyglet.clock.get_fps()))
		
		for label in self.blLabels:
			label.draw()
		for label in self.brLabels:
			label.draw()
		for label in self.tlLabels:
			label.draw()
		for label in self.trLabels:
			label.draw()
		
		# reenable depth for next model display
		glEnable(GL_DEPTH_TEST)
		glDepthMask(1)

App().main()
