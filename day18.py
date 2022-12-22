import numpy as np

with open("day18.input") as f:
	inputs = list(map(
		lambda coordinates: list(map(
			int, coordinates.split(",")
		)), f
	))

identity = np.identity(3, dtype=int)
possibilities = np.vstack([identity, -1*identity])

part1 = sum(
	1 for x, y, z in inputs for dx, dy, dz in possibilities 
	if [x+dx, y+dy, z+dz] not in inputs
)
print(part1)

def min_max(inputs):
	minx, miny, minz = inputs[0] 
	maxx, maxy, maxz = inputs[0]
	for x, y, z in inputs:
		minx, miny, minz = min(minx, x), min(miny, y), min(minz, z)
		maxx, maxy, maxz = max(maxx, x), max(maxy, y), max(maxz, z)
	return minx, miny, minz, maxx, maxy, maxz

minx, miny, minz, maxx, maxy, maxz = min_max(inputs)
air = [
	[x, y, z] for x in range(minx+1, maxx) for y in range(miny+1, maxy) for z in range(minz+1, maxz)
	if [x, y, z] not in inputs
]

def water(air):
	watered = [
		[x, y, z] for x, y, z in air 
		if all([x+dx, y+dy, z+dz] in inputs or [x+dx, y+dy, z+dz] in air for dx, dy, dz in possibilities)
	]
	return air if len(watered) == len(air) else water(watered)

watered = water(air)
part2 = sum(
	1 for x, y, z in inputs for dx, dy, dz in possibilities 
	if [x+dx, y+dy, z+dz] not in inputs and [x+dx, y+dy, z+dz] not in snuggled
)
print(part2)