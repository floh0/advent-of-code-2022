import re
import numpy as np
import math

parse = re.compile(r"(\d+)([RL])?(.+)?")

with open("day22.input") as f:
	top, bottom = f.read().split("\n\n")

def parse_instructions(instructions):
	while instructions is not None:
		number, direction, instructions = parse.match(instructions).groups()
		yield int(number), direction

class Tile:
	def __init__(self, value, x, y, matrix):
		self.value = value
		self.x = x
		self.y = y
		self.left = None
		self.right = None
		self.top = None
		self.bottom = None
		matrix[x-1][y-1] = self
	def password(self, facing):
		return self.x*1000 + self.y*4 + facing

def build_map(plan):
	transformed = list(map(list, plan.split("\n")))
	height = len(transformed)
	width = max(len(sublist) for sublist in transformed)
	matrix = np.empty((height, width), dtype=object)
	for i in range(height):
		sublist = transformed[i]
		for j in range(len(sublist)):
			if sublist[j] != " ":
				tile = Tile(sublist[j], i+1, j+1, matrix)
	return matrix

def build_connections(tiles, length, retrieve, connect):
	for i in range(length):
		line = retrieve(tiles, i)
		first, last, previous = None, None, None
		for tile in line:
			if tile is not None and first is None:
				first = tile
			if previous is not None and tile is not None:
				connect(previous, tile)
				last = tile
			previous = tile
		connect(last, first)

def connect_left_right(left, right):
	left.right = right
	right.left = left

def connect_top_bottom(top, bottom):
	top.bottom = bottom
	bottom.top = top

numbers, directions = list(zip(*parse_instructions(bottom)))
built = build_map(top)
length, width = built.shape
build_connections(built, length, lambda m,i: m[i,:], connect_left_right)
build_connections(built, width, lambda m,i: m[:,i], connect_top_bottom)

def fix_direction(previous, current):
	if current.left == previous:
		return 0
	elif current.top == previous:
		return 1
	elif current.right == previous:
		return 2
	else:
		return 3


def go(tiles, numbers, instructions):
	tile = next(tile for tile in built[0,:] if tile)
	facing = 0

	for number in numbers:
		for _ in range(number):
			if facing == 0:
				moved = tile.right
			elif facing == 1:
				moved = tile.bottom
			elif facing == 2:
				moved = tile.left
			else:
				moved = tile.top
			if moved.value == "#":
				break
			else:
				facing = fix_direction(tile, moved)
				tile = moved
		turn = next(instructions)
		if turn:
			facing = (facing+1 if turn == "R" else facing-1) % 4
	return tile.password(facing)

part1 = go(built, numbers, iter(directions))
print(part1)

def build_cube(tiles, length, retrieve, connect):
	for i in range(length):
		line = retrieve(tiles, i)
		previous = None
		for tile in line:
			if previous is not None and tile is not None:
				connect(previous, tile)
			previous = tile

built = build_map(top)
length, width = built.shape
build_cube(built, length, lambda m,i: m[i,:], connect_left_right)
build_cube(built, width, lambda m,i: m[:,i], connect_top_bottom)

def connect(direction1, coordinates1, direction2, coordinates2):
	for first, second in zip(coordinates1, coordinates2):
		for direction in (direction1, direction2):
			if direction == "t":
				first.bottom = second
			elif direction == "b":
				first.top = second
			elif direction == "r":
				first.left = second
			elif direction == "l":
				first.right = second
			first, second = second, first

flipped = {
	"r": "l",
	"l": "r",
	"b": "t",
	"t": "b"
}

height, width = built.shape
cube_side = math.gcd(height, width)
for i in range(0, height, cube_side):
	for j in range(0, width, cube_side):
		if built[i,j] is None:
			sides = list(filter(lambda x: x[1] is not None, [
				("t", built[i-1,j:j+cube_side] if (
					i > 0 and all(built[i-1,j:j+cube_side])
				) else None),
				("b", built[i+cube_side,j:j+cube_side] if (
					i+cube_side < height and all(built[i+cube_side,j:j+cube_side])
				) else None),
				("l", built[i:i+cube_side,j-1] if (
					j > 0 and all(built[i:i+cube_side,j-1])
				) else None),
				("r", built[i:i+cube_side,j+cube_side] if (
					j+cube_side < width and all(built[i:i+cube_side,j+cube_side])
				) else None)
			]))
			if len(sides) == 2:
				# 2233
				# 2233
				# 11
				# 11
				(direction1, coordinates1), (direction2, coordinates2) = sides
				if (direction1, direction2) in (("t", "r"), ("b", "l")):
					coordinates1 = coordinates1[::-1]
				connect(direction1, coordinates1, direction2, coordinates2)
			elif len(sides) == 1:
				# 223344
				# 223344
				# 11
				# 11
				(direction1, coordinates1), = sides
				additional_sides = list(filter(lambda x: x[1] is not None and not direction1 in x[0], [
					("rrt", built[i,j+2*cube_side:j+3*cube_side] if (
						j+3*cube_side <= width and all(built[i,j+2*cube_side:j+3*cube_side])
					) else None),
					("rrb", built[i+cube_side-1,j+2*cube_side:j+3*cube_side] if (
						j+3*cube_side <= width and all(built[i,j+2*cube_side:j+3*cube_side])
					) else None),
					("ttr", built[i-2*cube_side:i-cube_side,j+cube_side-1] if (
						i-2*cube_side >= 0 and all(built[i-2*cube_side:i-cube_side,j+cube_side-1])
					) else None),
					("ttl", built[i-2*cube_side:i-cube_side,j] if (
						i-2*cube_side >= 0 and all(built[i-2*cube_side:i-cube_side,j])
					) else None),
					("llt", built[i,j-2*cube_side:j-cube_side] if (
						j-2*cube_side >= 0 and all(built[i,j-2*cube_side:j-cube_side])
					) else None),
					("llb", built[i+cube_side-1,j-2*cube_side:j-cube_side] if (
						j-2*cube_side >= 0 and all(built[i+cube_side-1,j-2*cube_side:j-cube_side])
					) else None),
					("bbr", built[i+2*cube_side:i+3*cube_side,j+cube_side-1] if (
						i+3*cube_side <= height and all(built[i+2*cube_side:i+3*cube_side,j+cube_side-1])
					) else None),
					("bbl", built[i+2*cube_side:i+3*cube_side,j] if (
						i+3*cube_side <= height and all(built[i+2*cube_side:i+3*cube_side,j])
					) else None)
				]))

				if len(additional_sides) == 1:
					(direction2, coordinates2), = additional_sides
					coordinates2 = coordinates2[::-1]
					direction2 = flipped[direction2[-1]] 
					connect(direction1, coordinates1, direction2, coordinates2)

			far_sides = list(filter(lambda x: x[1] is not None, [
				("ttt", built[i-3*cube_side,j:j+cube_side] if (
					i-3*cube_side >= 0 and all(built[i-3*cube_side,j:j+cube_side])
				) else None),
				("bbb", built[i+4*cube_side-1,j:j+cube_side] if (
					i+4*cube_side-1 < height and all(built[i+4*cube_side-1,j:j+cube_side])
				) else None),
				("lll", built[i:i+cube_side,j-3*cube_side] if (
					j-3*cube_side >= 0 and all(built[i:i+cube_side,j-3*cube_side])
				) else None),
				("rrr", built[i:i+cube_side,j+4*cube_side-1] if (
					j+4*cube_side-1 < width and all(built[i:i+cube_side,j+4*cube_side-1])
				) else None)
			]))
			if len(far_sides) == 1:
				(direction1, coordinates1), = far_sides
				close_sides = list(filter(lambda x: x[1] is not None, [
					("tt", built[i-cube_side,j:j+cube_side] if (
						i-cube_side >= 0 and all(built[i-cube_side,j:j+cube_side])
					) else None),
					("bb", built[i+2*cube_side-1,j:j+cube_side] if (
						i+2*cube_side-1 < height and all(built[i+2*cube_side-1,j:j+cube_side])
					) else None),
					("ll", built[i:i+cube_side,j-cube_side] if (
						j-cube_side >= 0 and all(built[i:i+cube_side,j-cube_side])
					) else None),
					("rr", built[i:i+cube_side,j+2*cube_side-1] if (
						j+2*cube_side-1 < width and all(built[i:i+cube_side,j+2*cube_side-1])
					) else None)
				]))
				if len(close_sides) == 2:
					# 1122
					# 1122
					#   334455
					#   334455
					(direction2, coordinates2), = list(filter(lambda x: x[0][-1] != direction1[-1], close_sides))
					direction1, direction2 = flipped[direction1[-1]], flipped[direction2[-1]]
					connect(direction1, coordinates1, direction2, coordinates2)
				elif len(close_sides) == 0:
					# 1122
					# 1122
					#   334455
					#   334455
					#       66
					#       66
					mid_sides = list(filter(lambda x: x[1] is not None and len(set(x[0]) & set(direction1)) == 0, [
						("rrt", built[i,j+2*cube_side:j+3*cube_side] if (
							j+3*cube_side <= width and all(built[i,j+2*cube_side:j+3*cube_side])
						) else None),
						("rrb", built[i+cube_side-1,j+2*cube_side:j+3*cube_side] if (
							j+3*cube_side <= width and all(built[i,j+2*cube_side:j+3*cube_side])
						) else None),
						("ttr", built[i-2*cube_side:i-cube_side,j+cube_side-1] if (
							i-2*cube_side >= 0 and all(built[i-2*cube_side:i-cube_side,j+cube_side-1])
						) else None),
						("ttl", built[i-2*cube_side:i-cube_side,j] if (
							i-2*cube_side >= 0 and all(built[i-2*cube_side:i-cube_side,j])
						) else None),
						("llt", built[i,j-2*cube_side:j-cube_side] if (
							j-2*cube_side >= 0 and all(built[i,j-2*cube_side:j-cube_side])
						) else None),
						("llb", built[i+cube_side-1,j-2*cube_side:j-cube_side] if (
							j-2*cube_side >= 0 and all(built[i+cube_side-1,j-2*cube_side:j-cube_side])
						) else None),
						("bbr", built[i+2*cube_side:i+3*cube_side,j+cube_side-1] if (
							i+3*cube_side <= height and all(built[i+2*cube_side:i+3*cube_side,j+cube_side-1])
						) else None),
						("bbl", built[i+2*cube_side:i+3*cube_side,j] if (
							i+3*cube_side <= height and all(built[i+2*cube_side:i+3*cube_side,j])
						) else None)
					]))
					if len(mid_sides) == 1:
						(direction2, coordinates2), = mid_sides
						direction1, direction2 = flipped[direction1[-1]], flipped[direction2[-1]]
						connect(direction1, coordinates1, direction2, coordinates2)

part2 = go(built, numbers, iter(directions))
print(part2)