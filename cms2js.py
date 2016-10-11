#!/usr/bin/python
##########################################################
#  cms2js  0.3                                           #
#                                                        #
#    ColorLUT converter from the Nucoda CMS format to    #
#    JavaScript multi-array for integration in HTML      #
#    applications providing 3D visualization of the      #
#    WebGL-based RGB cube representing the LUT.          #
#                                                        #
#    Copyright (C) 2014 Walter Arrighetti, Ph.D.         #
#    All Rights Reserved.                                #
##########################################################
VERSION = "0.3"

UseShaper = False
Path = {
	"LUTs":"D:\\RD\\JScubes\\",
	"web templates":"D:\\RD\\JScubes\\",
	"JS templates":"D:\\RD\\JScubes\\",
	"HTML output":"D:\\git\\",
	"JS output":"D:\\git\\"
}
Template = {
	"HTML":"template.html",
	"JS":"template.js"
}
NL = {'HTML':'\r\n','JS':'\n'}
Placeholder = {
	"HTML":["<!--###############PLACEHOLDER1###############-->"],
	"JS":["/*###############PLACEHOLDER1###############*/"]
}

print "CMS2JS %s - ColorLUT converter from Nucoda CMS to JavaScript format"%VERSION
print "Copyright (C) 2014 Walter Arrighetti, Ph.D."
print "All Rights Reserved.\n"

import fnmatch
import sys
import re
import os

args, shaper = [], False
if len(sys.argv)==2 and os.path.isfile(sys.argv[1]):	args.append(sys.argv[1])
elif len(sys.argv)==2 and os.path.isdir(sys.argv[1]):
	print "Reading directory \"%s\" for Nucoda CMS ColorLUTs..."%sys.argv[1],
	for dirpath,dirnames,filenames in os.walk(sys.argv[1]):
		print filenames
		for name in filenames:
			if fnmatch.fnmatch(name.lower(),"*.cms"):	args.append(os.path.join(dirpath,name))
	print '\n',
else:
	print "Syntax:  cms2js  [sourceLUT.cms | path-for-CMS-LUTs]"
	sys.exit(1)
if not args:
	print " * WARNING!: No Nucoda CMS ColorLUTs found to convert."
	sys.exit(5)


for arg in args:
	inputLUT = arg
	RefName = os.path.splitext(os.path.split(inputLUT)[1])[0]
	HTMLplaceholder = os.path.join(Path["web templates"],Template["HTML"])
	JSplaceholder = os.path.join(Path["JS templates"],Template["JS"])
	if not os.path.isfile(JSplaceholder):
		print " * ERROR!: Unable to find in \"%s\" the main JavaScript template \"%s\" !"%os.path.split(JSplaceholder)
	if not os.path.isfile(HTMLplaceholder):
		print " * ERROR!: Unable to find in \"%s\" the main HTML template \"%s\" !"%os.path.split(HTMLplaceholder)
	if not os.path.isfile(inputLUT):
		inputLUT = os.path.join(Path["LUTs"],os.path.split(sys.argv[1])[1])
		if not os.path.isfile(inputLUT):
			print " * ERROR!: ColorLUT \"%s\" not found!"%inputLUT
	try:
		inLUT = open(inputLUT,"r")
		lines = inLUT.readlines()
		inLUT.close()
	except:
		print " * ERROR!: Unable to read ColorLUT \"%s\" !"%inputLUT


	for n in range(len(lines)):
		line = lines[n].strip()
		if line.startswith("LUT_1D_SIZE"):
			size = int(re.match("LUT_1D_SIZE\s+(?P<size>\d+)",line).group("size"))
			if size:	shaper = True
		if line.startswith("LUT_3D_SIZE"):
			side = int(re.match("LUT_3D_SIZE\s+(?P<size>\d+)",line).group("size"))
			startLUT = n+2
			break
	if not side:
		print " * ERROR!: Invalid CMS LUT header for \"%s\""%inputLUT
		sys.exit(2)

	if shaper:
		print "Parsing shaper LUT from \"%s\"....."%os.path.split(inputLUT)[1],
		shaperLUT = []
		for n in range(startLUT,len(lines)):
			if lines[n]=="":
				startLUT = n+1
				break
			line = re.match("(?P<red>\d+\.\d{4,7})\s+(?P<green>\d+\.\d{4,7})\s+(?P<blue>\d+\.\d{4,7})",lines[n].strip())
			if not line or len(line.groups())!=3:	continue
			shaperLUT.append(tuple(map(float,line.groups())))
			if len(shaperLUT) >= size:
				startLUT = n+1
				break
		print '\n',
	if len(shaperLUT) != size:
		print " * ERROR!: Invalid size for the shaper LUT!"
		sys.exit(3)

	LUT = []
	for n in range(startLUT,len(lines)):
		line = re.match("(?P<red>\d+\.\d{4,7})\s+(?P<green>\d+\.\d{4,7})\s+(?P<blue>\d+\.\d{4,7})",lines[n].strip())
		if line:
			startLUT = n
			break

	print "Parsing RGB cube from \"%s\"....."%os.path.split(inputLUT)[1],
	for i in range(side):
		LUT.append([])
		for j in range(side):
			LUT[i].append([])
			for k in range(side):
				LUT[i][j].append([])
				line = lines[startLUT + (side**2)*i + side*j + k].strip()
				LUTpoint = re.match("(?P<red>\d+\.\d{4,7})\s+(?P<green>\d+\.\d{4,7})\s+(?P<blue>\d+\.\d{4,7})",line)
				LUT[i][j][k] = tuple(map(float,LUTpoint.groups()))
	print '\n',

	LUTjs = "\tvar LUT=[";		shaperjs = "\tvar shaper=["
	print "Converting ColorLUT \"%s\" into JavaScript....."%RefName,
	for i in range(side):
		LUTjs += "[";		shaperjs += "["
		for j in range(side):
			LUTjs += "[";		shaperjs += "["
			for k in range(side):
				shaperjs += "[%.6f,%.6f,%.6f],"%(float(i)/side,float(j)/side,float(k)/side)
				LUTjs += "[%.6f,%.6f,%.6f],"%LUT[i][j][k]
			LUTjs += "],";		shaperjs += "],"
		LUTjs += "],";		shaperjs += "],"
	LUTjs += "];";		shaperjs += "];"
	print '\n',

	outputLUT = os.path.join(Path["JS output"],RefName+".html")
	outputJS = os.path.join(Path["JS output"],RefName+"_RGBcube.js")
	HTMLoutput = os.path.join(Path["HTML output"],)
	JSoutput = os.path.join(Path["JS output"],"")
	try:	PHhtml = open(HTMLplaceholder,"r")
	except:	print " * ERROR!: Unable to read HTML placeholder \"%s\" !"%HTMLplaceholder
	try:	PHjs = open(JSplaceholder,"r")
	except:	print " * ERROR!: Unable to read JS placeholder \"%s\" !"%JSplaceholder
	try:
		outJS = open(outputJS,"wb")
		outLUT = open(outputLUT,"wb")
	except:
		print " * ERROR!: Unable to write final HTML+JavaScrt files."
		sys.exit(4)

	for line in PHhtml:
		if Placeholder["HTML"][0] in line:
			start = line.find(Placeholder["HTML"][0])
			stop = start + len(Placeholder["HTML"][0])
			outLUT.write( line[:start] + os.path.relpath(outputJS,Path["HTML output"]) + line[stop:].strip("\n\r") + NL['HTML'] )
		else:	outLUT.write(line.strip("\n\r")+NL['HTML'])
	PHhtml.close()
	outLUT.close()
	print "Writing JavaScript LUT \"%s\"....."%os.path.split(outputJS)[1],
	for line in PHjs:
		if Placeholder["JS"][0] in line:
			start = line.find(Placeholder["JS"][0])
			stop = start + len(Placeholder["JS"][0])
			outJS.write( line[:start]+NL['JS'] )
			if UseShaper:	outJS.write( shaperjs + NL['JS'] )
			outJS.write( LUTjs + NL['JS'] )
			outJS.write( line[stop:].strip("\n\r") + NL['JS'] )
		else:	outJS.write(line.strip("\n\r")+NL['JS'])
	print '\n',
	PHjs.close()
	outJS.close()
