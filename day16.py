import re
import heapq

parse = re.compile(r"^Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ([\w\s,]+)$")

class Valve:
	def __init__(self, line):
		self.name = line[0]
		self.rate = int(line[1])
		self.tunnels = line[2].strip().split(", ")
	def __repr__(self):
		return f"name={self.name}, rate={self.rate}, tunnels={self.tunnels}"

with open("day16.input") as f:
	valves = list(map(
		lambda line: Valve(parse.match(line).groups()),
		f
	))

dictionary = { valve.name: valve for valve in valves }

def heuristic(minutes, opened, current):
	return sum(max(0,minutes-distances[current][valve.name])*valve.rate for valve in dictionary.values() if valve.name not in opened)

def heapify(value):
	return -value

def get_distances(node, distances, distance):
	if node not in distances or distances[node] > distance:
		distances[node] = distance
		for neighbour in dictionary[node].tunnels:
			distances = get_distances(neighbour, distances, distance+1)
	return distances

distances = {key: get_distances(key, {}, 0) for key in dictionary.keys()}

heap = [(heapify(heuristic(30, set(), "AA")), (30,0,"AA",set()))]

visited = set()

while True:
	value, (minutes, pressure, current, opened) = heapq.heappop(heap)
	if (value, minutes, pressure, current) in visited:
		continue
	visited.add((value, minutes, pressure, current))
	if minutes == 0:
		break
	minutes -= 1
	valve = dictionary[current]
	if current not in opened and valve.rate > 0:
		newopened = opened | {current}
		newpressure = pressure + minutes*valve.rate
		heapq.heappush(heap, (
			heapify(newpressure+heuristic(minutes, newopened, current)), 
			(minutes, newpressure, current, newopened)
		))
	for neighbour in valve.tunnels:
		heuristicvalue = heapify(pressure+heuristic(minutes, opened, neighbour))
		heapq.heappush(heap, (
			heuristicvalue, 
			(minutes, pressure, neighbour, opened)
		))

part1 = pressure
print(part1)

def better_heuristic(minutes, opened, human, elephant):
	return sum(max(0,minutes-min(distances[human][valve.name], distances[elephant][valve.name]))*valve.rate for valve in dictionary.values() if valve.name not in opened)

heap = [(heapify(better_heuristic(26, set(), "AA", "AA")), (26,0,"AA","AA",True,set()))]

visited = set()

while True:
	value, (minutes, pressure, human, elephant, turn, opened) = heapq.heappop(heap)
	if hash((value, minutes, pressure, human, elephant)) in visited or hash((value, minutes, pressure, elephant, human)) in visited:
		continue
	visited.add(hash((value, minutes, pressure, human, elephant)))
	if minutes == 0:
		break
	if turn:
		minutes -= 1
	current = human if turn else elephant
	newturn = not turn
	valve = dictionary[current]
	if current not in opened and valve.rate > 0:
		newhuman, newelephant = current if turn else human, elephant if turn else current
		newopened = opened | {current}
		newpressure = pressure + minutes*valve.rate
		heapq.heappush(heap, (
			heapify(newpressure+better_heuristic(minutes, newopened, newhuman, newelephant)), 
			(minutes, newpressure, newhuman, newelephant, newturn, newopened)
		))
	for neighbour in valve.tunnels:
		newhuman, newelephant = neighbour if turn else human, elephant if turn else neighbour
		heuristicvalue = heapify(pressure+better_heuristic(minutes, opened, newhuman, newelephant))
		heapq.heappush(heap, (
			heuristicvalue, 
			(minutes, pressure, newhuman, newelephant, newturn, opened)
		))

part2 = pressure
print(part2)


