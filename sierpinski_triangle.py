from PIL import Image
import numpy as np
from random import randint

side = 5000
size = (side, side)
iterations = side ** 2
APos, BPos, CPos = (side // 2, 10), (10, side - 10), (side - 10, side - 10)

outPath = 'SierpinskiTriangle.png'

def main():
	canvas = getCanvas(size)
	img = draw(canvas)
	
	img = Image.fromarray(img)
	img.save(outPath)

def getCanvas(size):
    xPix, yPix = size
    
    return np.zeros((yPix, xPix, 3), dtype=np.uint8)

def draw(canvas):
	dotPos = [APos[0], APos[1]]
	dots = [APos, BPos, CPos]
	
	for i in range(iterations):
		randomDot = dots[randint(0, 2)]
		
		dotPos = [(dotPos[i] + randomDot[i]) // 2 for i in range(2)]
		#print(dotPos)
		
		norm = dotPos[0] / size[0] * dotPos[1] / size[1]
		canvas[dotPos[1]][dotPos[0]] = (
		int(9 * (1 - norm) * (norm ** 3) * 255),
		int(15 * (1 - norm) ** 2 * (norm ** 2) * 255),
		int(8.5 * (1 - norm) ** 3 * norm * 255)
		)
	
	#print(canvas)
	return np.array(canvas).astype(np.uint8)

main()