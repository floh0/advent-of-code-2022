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
	return (covering_lines_for_row(sensors, i) for i in range(limit+1))

def covering_lines_generator(sensors, targety):
	for sensor in sensors:
		distance_from_targety = abs(sensor.y-targety)-sensor.closest
		if distance_from_targety <= 0:
			yield [sensor.x+distance_from_targety, sensor.x-distance_from_targety]

def covering_lines_for_row(sensors, targety):
	return iter(sorted(
		covering_lines_generator(sensors, targety), 
		key=lambda x: x[0]
	))

def merge(acc, value):
	xa, ya = acc[-1]
	xb, yb = value
	if xa <= xb <= ya+1:
		acc[-1][0], acc[-1][1] = xa, max(ya, yb)
	else:
		acc.append(value)
	return acc

def merge_line(line):
	return iter(functools.reduce(merge, line, [next(line)]))

def find_spots(lines):
	first = next(lines, None)
	if first and next(lines, None):
		yield first[1]+1

def find_lost(spots, sensors):
	for y, spot in enumerate(spots):
		x = next(spot, None)
		if x:
			return x, y

sensors = list(map(Sensor, lines))

y = 2000000

beacons = set((sensor.beaconx, sensor.beacony) for sensor in sensors)
line = covering_lines_for_row(sensors, y)
part1 = 0
for left, right in merge_line(line):
	part1 += abs(right-left+1)
	part1 -= sum(1 for beaconx, beacony in beacons if left <= beaconx <= right and beacony == y)
print(part1)

limit = y*2
lines = covering_lines(sensors, limit)
merged = map(merge_line, lines)

spots = map(find_spots, merged)
beaconx, beacony = find_lost(spots, sensors)

part2 = beaconx*4000000+beacony
print(part2)
