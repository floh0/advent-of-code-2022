import numpy as np

with open("day08.input") as f:
	trees = np.matrix(
		[list(map(int, [tree for tree in line.strip()])) for line in f]
	)

def visible_from_left(matrix, i, j):
	line = matrix[i:i+1,:j+1]
	tree = line[:,-1]
	others = line[:,:-1]
	return (tree > others).all()

rot1 = np.rot90(trees, k=1)
rot2 = np.rot90(trees, k=2)
rot3 = np.rot90(trees, k=3)

length, width = trees.shape

part1 = 0
for i in range(length):
	for j in range(width):
		if visible_from_left(trees, i, j) or \
			visible_from_left(rot1, width-1-j, i) or \
			visible_from_left(rot2, length-1-i, width-1-j) or \
			visible_from_left(rot3, j, length-1-i):
			part1 += 1

def tree_generator(direction, height):
	blocked = False
	for tree in direction:
		if not blocked:
			if tree < height:
				yield 1
			else:
				blocked = True
				yield 1

def scenic_score(matrix, i, j):
	left = np.flip(matrix[i:i+1,:j]).tolist()[0]
	right = matrix[i:i+1,j+1:].tolist()[0]
	up = np.rot90(matrix[:i,j:j+1], k=-1).tolist()[0]
	down = np.rot90(matrix[i+1:,j:j+1], k=1).tolist()[0]

	height = matrix[i,j]

	score = 1
	for direction in [left, right, up, down]:
		score *= sum(tree_generator(direction, height))
	return score

part2 = max(scenic_score(trees, i, j) for i in range(length) for j in range(width))		
print(part2)