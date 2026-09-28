from PIL import Image
from math import sin, pi, cos
import sys
import numpy as np
from decimal import Decimal, getcontext

size = (640, 640)
coords = (-1, 0)
zoom = 1/10
#zoom = 1/10
vSize = (4 * zoom, 4 * zoom * (size[1] / size[0]))
depth = 20
getcontext().prec = 30

outPath = "MandelbrotSet.png"

def main():
	canvas = getCanvas(size)
	img = draw(canvas)
	
	#print( img)
	img = Image.fromarray(img)
	img.save(outPath)

def getCanvas(size):
	xPix, yPix = size
	canvas = [[[] for x in range(xPix)] for y in range(yPix)]
	
	return canvas

def draw(canvas):
	yPix, xPix = len(canvas), len(canvas[0])
	canvas = [[color(mandel(coordCorrect([x, y]))) for x in range(xPix)] for y in range(yPix)]
	
	#print(canvas)
	return np.array(canvas).astype(np.uint8)

def mandel(c):
	z = (0.5*c[0], 0.1+c[1]*c[0])
	
	for i in range(1, depth + 1):
		z = (Decimal(z[0]) ** 2 - Decimal(z[1]) ** 2, 2 * z[0] * z[1])
		z = (Decimal(z[0]) + Decimal(c[0]), Decimal(z[1]) + Decimal(c[1]))
		
		if Decimal(z[0]) ** 2 + Decimal(z[1]) ** 2 > 4:
			#print(1)
			return i
		
	return depth

def color(x):
	if x == depth:
		return (0, 0, 0)
	
	norm = x / depth
	
	r = int(9 * (1 - norm) * (norm ** 3) * 255)
	g = int(15 * (1 - norm) ** 2 * (norm ** 2) * 255)
	b = int(8.5 * (1 - norm) ** 3 * norm * 255)
	
	#r = int(255 * norm)
#	g = int(165 * norm)
#	b = int(255 * (1 - norm))
	
	result = (r, g, b)
	return result

def coordCorrect(xy):
	x, y = xy
	for i in range(2):
		xy[i] = vSize[i] / size[i] * xy[i] - vSize[i] / 2 + coords[i]
	
	return xy

main()