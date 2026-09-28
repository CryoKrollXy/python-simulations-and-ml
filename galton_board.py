from random import choice
from math import ceil

balls = 100000 # количество шаров
width = 201 # ширина доски
startPos = ceil(width / 2) # откуда кидаем шарик
variants = [-1, 1]
variants = [x / 2 for x in variants]

def main():
	field = galton(width, balls, startPos)
	
	print_graph(field)

def galton(width, balls, startPos):
	levels = width - 1
	
	field = bouncing([0 for _ in range(width)], 
									balls, levels, startPos, True)
	
	return field	

def bouncing(field, balls, levels, startPos,
						recochet = False):
	for ball in range(balls):
		#currentPos = balls - balls // len(field) * len(field)
		currentPos = startPos	
		
		lvl = 0
		while lvl < levels:
			if recochet: oldPos = currentPos
			
			currentPos += choice(variants)
			
			currentPos = min(len(field) - 1, currentPos)
			currentPos = max(0, currentPos)
			
			if recochet and currentPos == oldPos:
				if currentPos == 0:
					currentPos += 1
				else:
					currentPos -= 1
			lvl += 1
		
		field[
			round(currentPos) if 
			(currentPos + 1) % 0.1 == 5 and int(currentPos + 1) % 2 == 1
			else int(currentPos)
		] += 1
	
	return field

def print_graph(field):
	if max(field) == 0:
		print("what?")
		return None
	
	step = 62 / max(field)
	
	result = []
	for x in field:
	    coeff = round(step * x, 1)
	    formatted_coeff = f"{coeff:.{2 if len(str(int(coeff))) == 1 else 1}f}"
	    
	    line = "•" * int(coeff)
	    if len(line) > 0: result.append(f"{formatted_coeff} " + line)
	
	print("\n".join(result))

main()