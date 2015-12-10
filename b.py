#!/usr/bin/env python
#requires pyparsing

import xml.dom
import re
from xml.dom.minidom import parse, parseString

import css
from pathdata import svg as svgparsing
from math import ceil, floor
import os.path
import sys
import subprocess
import time

b = r"(matrix|translate|scale|rotate|skewX|skewY)" r"\(((.+?),)*(.*?)\)"
tfRe = re.compile(b,)

paths = [[[]]]
names = [[[]]]

emSize = 1024
parsed = 0

infile = "/home/nekoyasha/Desktop/nekotoba2/nicesheet.php.svg"

count = 0

def iterDOM (Node, depth = 0, transformStack = None):
    parsed = 0
    chars = 0
    if transformStack == None: transformStack = [(0.0,0.0)]
    for a in Node.childNodes:
        parsed = parsed + 1
        if a.nodeType == xml.dom.Node.ELEMENT_NODE:
            bounds = [None, None, None, None] #for hittesting
            #print " " * depth, a,
            #parse and push transform
            transform = (0.0,0.0)
            transform=mergeTransform(transform, createTransformFromNode(a))
            transform=mergeTransform(transform, createTransformFromXY(a))
            transformStack.append(mergeTransform(transformStack[-1],transform))
            #if transform != (0.0,0.0) : print "transform:", transform, transformStack[-1],
            if a.tagName == "path":
                #print a.getAttribute("d")
                steps = svgparsing.parseString(a.getAttribute("d"))
#                print steps[0][0]
#                current_point = [0, 0]
                for command, arguments in steps:  
                    #completely lazy.
                    bounds = addPointToBounds(bounds, arguments[0])
                    break
#                    if command == "M":
#                        bounds = addPointToBounds(bounds, arguments[0])
#                        for param in arguments:
#                            bounds = addPointToBounds(bounds, param)  
#                    elif command == "m":
#                        for param in arguments:
#                            bounds = addPointToBounds(bounds, param)  
#                    elif command == "C":
#                        for param in arguments:
#                            bounds = addPointToBounds(bounds, param[2])  
#                    elif command == "L":
#                        for param in arguments:
#                            bounds = addPointToBounds(bounds, param)
#                    elif command == "Z":
#                        pass
#                    else:
#                        pass
                        #print command, arguments
                #print floor(bounds[0] / emSize),floor(bounds[1] / emSize)
            elif a.tagName == "svg":
                width = int(ceil(float(a.getAttribute("width")) / emSize))
                height = int(ceil(float(a.getAttribute("height")) / emSize))
                paths[:] = [[[] for i in range(height)] for i in range(width)]
                names[:] = [[[] for i in range(height)] for i in range(width)]
                #print paths
                #print names
            elif a.tagName == "text":
                s = ""
                for subnode in a.childNodes:
                    if subnode.nodeType == xml.dom.Node.TEXT_NODE:
                        s += subnode.data
                if s != "":
                    names[int(floor(transformStack[-1][0]/emSize))][int(floor(transformStack[-1][1]/emSize))].append(s)
            elif True: #add more types here
                pass
            #print bounds
            if  paths[0] != None and bounds[0] != None:
                #pass
                try:
                    n = paths[int(floor(bounds[0]/emSize))][int(floor(bounds[1]/emSize))]
                    if len(n) == 0: chars += 1
                    n.append(a)
                    if parsed % 10 == 0:
                        #sys.stdout.write("\r[{2:8.3}] {0} strokes, {1} chars".format(parsed, chars), 0);
                        sys.stdout.write("\r[{2:8.03}] {0} strokes, {1} chars".format(parsed, chars, time.clock()));
                        sys.stdout.flush();
                    
                except IndexError:
                    pass
            #apply transform
            #pop transform
            if a.hasChildNodes:
                iterDOM(a, depth+1, transformStack)
            #pop transform
            transformStack.pop(-1)
            
def createTransformFromNode (node, attribute='transform'):
    a=(0,0)
    transform = node.getAttribute("transform")
    if transform:
        for transform, args in css.transformList.parseString(transform):
            if transform == 'translate':
                if len(args) == 1:
                    x = args[0]
                    y = 0
                else:
                    x, y = args
            a = x,y
    return a
#print b

def createTransformFromXY (node):
    x=0
    y=0

    attx=node.getAttribute("x")
    atty=node.getAttribute("y")
    
    if attx: x = float(attx)
    if atty: y = float(atty)
##    print x,y ,
    return x,y
    pass
    
def mergeTransform(left, right):
    transform = left[0]+right[0], left[1]+right[1]
   ## print "merged:",transform,
    return transform

def addPointToBounds(bounds,point):
    if bounds[0] == None or bounds[2] == None:
        bounds[0] = bounds[2] = point[0]
    else:
        bounds[0] = min(bounds[0], point [0])
        bounds[2] = max(bounds[2], point [0])
    if bounds[1] == None or bounds[3] == None:
        bounds[1] = bounds[3] = point[1]
    else:
        bounds[1] = min(bounds[1], point [1])
        bounds[3] = max(bounds[3], point [1])
    return bounds

def makeFiles():
    filepath, filename = os.path.split(infile)
    fname, ext = os.path.splitext(filename)
    for i, column in enumerate(paths):
        #print i,
        for j, cell in enumerate(column):
            if len(cell) > 0:
                
                #do stuff here
                subname = "_%d-%d" % (j,i)
                if len(names[i][j])>0:

                    subname = names[i][j][0]
                outfilename = os.path.join(filepath, subname+ext)
                sys.stdout.write("[{1:8.3}] {0}".format(outfilename, time.clock()));
                sys.stdout.write("\r");
                sys.stdout.flush();
                f = open(outfilename,"w")
                s = """<?xml version="1.0" encoding="utf-8" ?>

<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" 
  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg 
    xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
    xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
    width="{0}" height="{1}" id="{2}">
""".format (emSize, emSize, subname.replace("+", ""))
                f.write(s)
                for p in cell:
                    p.setAttribute("transform", "translate(%g, %g)" % (-i*emSize, -j*emSize))
                    f.write(p.toxml())
                f.write("</svg>")
                f.close()
                parm = ['inkscape', '--verb', 'SelectionUnion', '--verb', 'FileSave', '--verb', 'FileClose', outfilename]
                parm[1:1] = ["--select={0}".format(x.getAttribute('id')) for x in cell]
                subprocess.call(parm)
    sys.stdout.write("\n");     
parsed = parsed + 1
dom1 = parse(infile)
iterDOM(dom1)
#print names, paths
sys.stdout.write("\n");     
makeFiles()
