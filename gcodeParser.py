#!/usr/bin/env python

import math

class GcodeParser:
	
	def __init__(self):
		self.model = GcodeModel(self)
		
	def parseFile(self, path):
		# read the gcode file
		with open(path, 'r') as f:
			# init line counter
			self.lineNb = 0
			# for all lines
			for line in f:
				# inc line counter
				self.lineNb += 1
				# remove trailing linefeed
				self.line = line.rstrip()
				# parse a line
				self.parseLine()
			
		self.model.postProcess()
		return self.model
		
	def parseLine(self):
		# strip comments:
		bits = self.line.split(';',1)
		if (len(bits) > 1):
			comment = bits[1]
		
		# extract & clean command
		command = bits[0].strip()
		
		# TODO strip logical line number & checksum
		
		# code is fist word, then args
		comm = command.split(None, 1)
		code = comm[0] if (len(comm)>0) else None
		args = comm[1] if (len(comm)>1) else None
		
		if code:
			if hasattr(self, "parse_"+code):
				getattr(self, "parse_"+code)(args)
			else:
				self.warn("Unknown code '%s'"%code)
		
	def parseArgs(self, args):
		dic = {}
		if args:
			bits = args.split()
			for bit in bits:
				letter = bit[0]
				coord = float(bit[1:])
				dic[letter] = coord
		return dic

	def parse_G0(self, args):
		# G0: Rapid move
		# same as a controlled move for us (& reprap FW)
		self.G1(args, "G0")
		
	def parse_G1(self, args, type="G1"):
		# G1: Controlled move
		self.model.do_G1(self.parseArgs(args), type)
		
	def parse_G20(self, args):
		# G20: Set Units to Inches
		self.error("Unsupported & incompatible: G20: Set Units to Inches")
		
	def parse_G21(self, args):
		# G21: Set Units to Millimeters
		# Default, nothing to do
		pass
		
	def parse_G28(self, args):
		# G28: Move to Origin
		self.model.do_G28(self.parseArgs(args))
		
	def parse_G90(self, args):
		# G90: Set to Absolute Positioning
		self.model.setRelative(False)
		
	def parse_G91(self, args):
		# G91: Set to Relative Positioning
		self.model.setRelative(True)
		
	def parse_G92(self, args):
		# G92: Set Position
		self.model.do_G92(self.parseArgs(args))
		
	def warn(self, msg):
		print "[WARN] Line %d: %s (Text:'%s')" % (self.lineNb, msg, self.line)
		
	def error(self, msg):
		print "[ERROR] Line %d: %s (Text:'%s')" % (self.lineNb, msg, self.line)
		raise Exception("[ERROR] Line %d: %s (Text:'%s')" % (self.lineNb, msg, self.line))

class BBox(object):
	
	def __init__(self, coords):
		self.xmin = self.xmax = coords["X"]
		self.ymin = self.ymax = coords["Y"]
		self.zmin = self.zmax = coords["Z"]
		
	def dx(self):
		return self.xmax - self.xmin
	
	def dy(self):
		return self.ymax - self.ymin
	
	def dz(self):
		return self.zmax - self.zmin
		
	def cx(self):
		return (self.xmax + self.xmin)/2
	
	def cy(self):
		return (self.ymax + self.ymin)/2
	
	def cz(self):
		return (self.zmax + self.zmin)/2
	
	def extend(self, coords):
		self.xmin = min(self.xmin, coords["X"])
		self.xmax = max(self.xmax, coords["X"])
		self.ymin = min(self.ymin, coords["Y"])
		self.ymax = max(self.ymax, coords["Y"])
		self.zmin = min(self.zmin, coords["Z"])
		self.zmax = max(self.zmax, coords["Z"])
		
class GcodeModel:
	
	def __init__(self, parser):
		# save parser for messages
		self.parser = parser
		# latest coordinates & extrusion relative to offset, feedrate
		self.relative = {
			"X":0.0,
			"Y":0.0,
			"Z":0.0,
			"F":0.0,
			"E":0.0}
		# offsets for relative coordinates and position reset (G92)
		self.offset = {
			"X":0.0,
			"Y":0.0,
			"Z":0.0,
			"E":0.0}
		# if true, args for move (G1) are given relatively (default: absolute)
		self.isRelative = False
		# the segments
		self.segments = []
		self.layers = None
		self.distance = None
		self.extrudate = None
		self.bbox = None
	
	def do_G1(self, args, type):
		# G0/G1: Rapid/Controlled move
		# clone previous coords
		coords = dict(self.relative)
		# update changed coords
		for axis in args.keys():
			if coords.has_key(axis):
				if self.isRelative:
					coords[axis] += args[axis]
				else:
					coords[axis] = args[axis]
			else:
				self.warn("Unknown axis '%s'"%axis)
		# build segment
		absolute = {
			"X": self.offset["X"] + coords["X"],
			"Y": self.offset["Y"] + coords["Y"],
			"Z": self.offset["Z"] + coords["Z"],
			"F": coords["F"],	# no feedrate offset
			"E": self.offset["E"] + coords["E"]
		}
		seg = Segment(
			type,
			absolute,
			self.parser.lineNb,
			self.parser.line)
		self.addSegment(seg)
		# update model coords
		self.relative = coords
		
	def do_G28(self, args):
		# G28: Move to Origin
		self.warn("G28 unimplemented")
		
	def do_G92(self, args):
		# G92: Set Position
		# this changes the current coords, without moving, so do not generate a segment
		
		# no axes mentioned == all axes to 0
		if not len(args.keys()):
			args = {"X":0.0, "Y":0.0, "Z":0.0, "E":0.0}
		# update specified axes
		for axis in args.keys():
			if self.offset.has_key(axis):
				# transfer value from relative to offset
				self.offset[axis] += self.relative[axis] - args[axis]
				self.relative[axis] = args[axis]
			else:
				self.warn("Unknown axis '%s'"%axis)

	def setRelative(self, isRelative):
		self.isRelative = isRelative
		
	def addSegment(self, segment):
		self.segments.append(segment)
		#print segment
		
	def warn(self, msg):
		self.parser.warn(msg)
		
	def error(self, msg):
		self.parser.error(msg)
		
		
	def classifySegments(self):
		# apply intelligence, to classify segments
		
		# start model at 0
		coords = {
			"X":0.0,
			"Y":0.0,
			"Z":0.0,
			"F":0.0,
			"E":0.0}
			
		# first layer at Z=0
		currentLayerIdx = 0
		currentLayerZ = 0
		
		for seg in self.segments:
			# default style is fly (move, no extrusion)
			style = "fly"
			
			# no horizontal movement, but extruder movement: retraction/refill
			if (
				(seg.coords["X"] == coords["X"]) and
				(seg.coords["Y"] == coords["Y"]) and
				(seg.coords["E"] != coords["E"]) ):
					style = "retract" if (seg.coords["E"] < coords["E"]) else "restore"
			
			# some horizontal movement, and positive extruder movement: extrusion
			if (
				( (seg.coords["X"] != coords["X"]) or (seg.coords["Y"] != coords["Y"]) ) and
				(seg.coords["E"] > coords["E"]) ):
				style = "extrude"
			
			# positive extruder movement in a different Z signals a layer change for this segment
			if (
				(seg.coords["E"] > coords["E"]) and
				(seg.coords["Z"] != currentLayerZ) ):
				currentLayerZ = seg.coords["Z"]
				currentLayerIdx += 1
			
			# set style and layer in segment
			seg.style = style
			seg.layerIdx = currentLayerIdx
			
			
			#print coords
			#print seg.coords
			#print "%s (%s  | %s)"%(style, str(seg.coords), seg.line)
			#print
			
			# execute segment
			coords = seg.coords
			
			
	def splitLayers(self):
		# split segments into previously detected layers
		
		# start model at 0
		coords = {
			"X":0.0,
			"Y":0.0,
			"Z":0.0,
			"F":0.0,
			"E":0.0}
			
		# init layer store
		self.layers = []
		
		currentLayerIdx = -1
		
		# for all segments
		for seg in self.segments:
			# next layer
			if currentLayerIdx != seg.layerIdx:
				layer = Layer(coords["Z"])
				layer.start = coords
				self.layers.append(layer)
				currentLayerIdx = seg.layerIdx
			
			layer.segments.append(seg)
			
			# execute segment
			coords = seg.coords
		
		self.topLayer = len(self.layers)-1
		
	def calcMetrics(self):
		# init distances and extrudate
		self.distance = 0
		self.extrudate = 0
		
		# init model bbox
		self.bbox = None
		
		# extender helper
		def extend(bbox, coords):
			if bbox is None:
				return BBox(coords)
			else:
				bbox.extend(coords)
				return bbox
		
		# for all layers
		for layer in self.layers:
			# start at layer start
			coords = layer.start
			
			# init distances and extrudate
			layer.distance = 0
			layer.extrudate = 0
			
			# include start point
			self.bbox = extend(self.bbox, coords)
			
			# for all segments
			for seg in layer.segments:
				# calc XYZ distance
				d  = (seg.coords["X"]-coords["X"])**2
				d += (seg.coords["Y"]-coords["Y"])**2
				d += (seg.coords["Z"]-coords["Z"])**2
				seg.distance = math.sqrt(d)
				
				# calc extrudate
				seg.extrudate = (seg.coords["E"]-coords["E"])
				
				# accumulate layer metrics
				layer.distance += seg.distance
				layer.extrudate += seg.extrudate
				
				# execute segment
				coords = seg.coords
				
				# include end point
				extend(self.bbox, coords)
			
			# accumulate total metrics
			self.distance += layer.distance
			self.extrudate += layer.extrudate
		
	def postProcess(self):
		self.classifySegments()
		self.splitLayers()
		self.calcMetrics()

	def __str__(self):
		return "<GcodeModel: len(segments)=%d, len(layers)=%d, distance=%f, extrudate=%f, bbox=%s>"%(len(self.segments), len(self.layers), self.distance, self.extrudate, self.bbox)
	
class Segment:
	def __init__(self, type, coords, lineNb, line):
		self.type = type
		self.coords = coords
		self.lineNb = lineNb
		self.line = line
		self.style = None
		self.layerIdx = None
		self.distance = None
		self.extrudate = None
	def __str__(self):
		return "<Segment: type=%s, lineNb=%d, style=%s, layerIdx=%d, distance=%f, extrudate=%f>"%(self.type, self.lineNb, self.style, self.layerIdx, self.distance, self.extrudate)
		
class Layer:
	def __init__(self, Z):
		self.Z = Z
		self.segments = []
		self.distance = None
		self.extrudate = None
		
	def __str__(self):
		return "<Layer: Z=%f, len(segments)=%d, distance=%f, extrudate=%f>"%(self.Z, len(self.segments), self.distance, self.extrudate)
		
		
if __name__ == '__main__':
	path = "test.gcode"

	parser = GcodeParser()
	model = parser.parseFile(path)

	print model
