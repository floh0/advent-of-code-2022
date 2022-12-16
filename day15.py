import re
import functools

parse = re.compile(r"^Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)$")

with open("day15.input") as f:
	lines = list(map(
		lambda line: list(map(int, parse.match(line).groups())),
		f
	))

def manhattan(fromx, fromy, tox, toy):
	return abs(fromx-tox)+abs(fromy-toy)

class Sensor:
	def __init__(self, data):
		self.x = data[0]
		self.y = data[1]
		self.beaconx = data[2]
		self.beacony = data[3]
		self.closest = manhattan(*data)

def covering_lines(sensors, limit):
	return [sorted(
		covering_lines_for_row(sensors, i), 
		key=lambda x: x[0]
	) for i in range(limit+1)]

def covering_lines_for_row(sensors, targety):
	for sensor in sensors:
		distance_from_targety = abs(sensor.y-targety)-sensor.closest
		if distance_from_targety <= 0:
			yield [sensor.x+distance_from_targety, sensor.x-distance_from_targety]

def merge_lines(acc, value):
	xa, ya = acc[-1]
	xb, yb = value
	if xa <= xb <= ya+1:
		return acc[:-1] + [[xa, max(ya, yb)]]
	else:
		return acc[:-1] + [[xa, ya], [xb, yb]]

def sliding(elems, size):
	for i in range(len(elems)-size+1):
		yield elems[i:i+size]

def find_spots(lines):
	for ((xa, ya), (xb, yb)) in sliding(lines, 2):
		if not xa <= xb <= ya+1:
			yield ya+1

def find_lost(spots, sensors):
	for y, spot in enumerate(spots):
		x = next(spot, None)
		if x:
			return x, y

sensors = list(map(Sensor, lines))

y = 2000000

limit = y*2
lines = covering_lines(sensors, limit)
merged = list(map(lambda line: functools.reduce(merge_lines, line, [line[0]]), lines))

part1 = 0
beacons = set((sensor.beaconx, sensor.beacony) for sensor in sensors)
for left, right in merged[y]:
	part1 += abs(right-left+1)
	part1 -= sum(1 for beaconx, beacony in beacons if left <= beaconx <= right and beacony == y)
print(part1)

spots = map(find_spots, merged)
beaconx, beacony = find_lost(spots, sensors)

part2 = beaconx*4000000+beacony
print(part2)