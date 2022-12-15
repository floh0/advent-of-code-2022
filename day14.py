import numpy as np

with open("day14.input") as f:
	lines = list(map(
		lambda line: list(map(
			lambda tuple: list(map(int, tuple.split(","))), 
			line.split(" -> ")
		)), 
		f
	))

def initialize_matrix(lines):
	(minx, miny), (maxx, maxy) = (lines[0][0][0], 0), lines[0][0]
	for line in lines:
		for x, y in line:
			minx = x if x < minx else minx
			maxx = x if x > maxx else maxx
			miny = y if y < miny else miny
			maxy = y if y > maxy else maxy
	return minx, maxx, miny, maxy, np.zeros((maxy - miny + 1, maxx - minx + 1), dtype=int)

def sliding(elems, size):
	for i in range(len(elems)-size+1):
		yield elems[i:i+size]

def fill_with_rocks(lines, offset, matrix):
	for line in lines:
		for (fromx, fromy), (tox, toy) in sliding(line, 2):
			if fromx == tox:
				for i in range(min(fromy,toy),max(fromy,toy)+1):
					matrix[i,fromx-offset] = 1
			elif fromy == toy:
				for i in range(min(fromx,tox),max(fromx,tox)+1):
					matrix[fromy,i-offset] = 1

def move(x, y, minx, matrix):
	if matrix[y+1,x-minx] == 0:
		return x,y+1
	if matrix[y+1,x-1-minx] == 0:
		return x-1,y+1
	if matrix[y+1,x+1-minx] == 0:
		return x+1,y+1
	else:
		return None

def put_sand(x, y, minx, maxx, maxy, matrix):
	result = move(x, y, minx, matrix)
	while result is not None:
		x, y = result
		if y+1 > maxy or x-1 < minx or x+1 > maxx:
			return True
		result = move(x, y, minx, matrix)
	matrix[y,x-minx] = 2
	return False

minx, maxx, miny, maxy, matrix = initialize_matrix(lines)
fill_with_rocks(lines, minx, matrix)

part1 = 0
while not put_sand(500, 0, minx, maxx, maxy, matrix):
	part1 += 1
print(part1)

def add_floor(minx, maxx, maxy, matrix):
	width = maxx - minx + 1
	return maxy+2, np.vstack([matrix, np.zeros(width, dtype=int), np.ones(width, dtype=int)])

def expand(minx, miny, maxy, matrix):
	height = maxy - miny + 1
	matrix = np.hstack([np.zeros((height, 1), dtype=int), matrix, np.zeros((height, 1), dtype=int)])
	matrix[-1,0], matrix[-1,-1] = 1, 1
	return minx-1, maxx+1, matrix

maxy, matrix = add_floor(minx, maxx, maxy, matrix)
part2 = part1
while matrix[0,500-minx] != 2:
	if put_sand(500, 0, minx, maxx, maxy, matrix):
		minx, maxx, matrix = expand(minx, miny, maxy, matrix)
	else:
		part2 += 1
print(part2)
