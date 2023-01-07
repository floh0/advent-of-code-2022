import numpy as np
import heapq

def transform_input(matrix):
	height, width = matrix.shape
	transformed = np.zeros((height, width, 4), dtype=int)
	for i in range(height):
		for j in range(width):
			if matrix[i,j] == ">":
				transformed[i,j,0] = 1
			elif matrix[i,j] == "<":
				transformed[i,j,1] = 1
			elif matrix[i,j] == "^":
				transformed[i,j,2] = 1
			elif matrix[i,j] == "v":
				transformed[i,j,3] = 1
	return transformed

with open("day24.input") as f:
	matrix = transform_input(
		np.matrix(list(map(list, map(
			lambda line: line.strip()[1:-1], 
			f.readlines()[1:-1]
		))), dtype=str)
	)

def move(matrix):
	height, width, depth = matrix.shape
	moved = np.zeros((height, width, depth), dtype=list)
	for i in range(height):
		for j in range(width):
			if matrix[i,j,0] == 1:
				moved[i,(j+1)%width,0] = 1
			if matrix[i,j,1] == 1:
				moved[i,(j-1)%width,1] = 1
			if matrix[i,j,2] == 1:
				moved[(i-1)%height,j,2] = 1
			if matrix[i,j,3] == 1:
				moved[(i+1)%height,j,3] = 1
	return moved

def manhattan(fromx, fromy, tox, toy):
	return abs(fromx-tox)+abs(fromy-toy)

class Elem:
	def __init__(self, weight, value):
		self.value = value
		self.weight = weight
	def __lt__(self, other):
		return self.weight < other.weight

def do(matrix, fromx, fromy, tox, toy):
	height, width, _ = matrix.shape
	heuristic = lambda x,y: manhattan(x,y,tox,toy)
	x,y = fromx,fromy
	heap = [Elem(heuristic(x,y),(x,y,matrix,0))]

	identity = np.identity(2, dtype=int)
	possibilities = np.vstack([identity, -1*identity, np.zeros((1,2), dtype=int)])

	visited = set()

	while True:
		elem = heapq.heappop(heap)
		x, y, current, minutes = elem.value
		if (x, y, minutes) in visited:
			continue
		else:
			visited.add((x, y, minutes))
		if (x,y) == (tox, toy):
			break
		moved = move(current)
		for i,j in possibilities:
			if (x+i, y+j) == (fromx, fromy) or (
				0 <= x+i <= height-1 and 0 <= y+j <= width-1 and np.sum(moved[x+i,y+j,:]) == 0
			):
				heapq.heappush(heap, Elem(minutes+1+heuristic(x+i, y+j), (x+i, y+j, moved, minutes+1)))

	return move(current), minutes+1

height, width, _ = matrix.shape

trip1, part1 = do(matrix, -1, 0, height-1, width-1)
print(part1)

trip2, back = do(trip1, height, width-1, 0, 0)
_, forth = do(trip2, -1, 0, height-1, width-1)
part2 = part1 + back + forth
print(part2)