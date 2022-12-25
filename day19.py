import re
import heapq
import functools

parse = re.compile(r"^Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.$")

class Blueprint:
	def __init__(self, line):
		self.num = int(line[0])
		self.ore_ore_cost = int(line[1])
		self.clay_ore_cost = int(line[2])
		self.obsidian_ore_cost = int(line[3])
		self.obsidian_clay_cost = int(line[4])
		self.geode_ore_cost = int(line[5])
		self.geode_obsidian_cost = int(line[6])

with open("day19.input") as f:
	blueprints = list(map(
		lambda line: Blueprint(parse.match(line).groups()),
		f
	))

def max_geode(minutes, 
	ore_robots, clay_robots, obsidian_robots, geode_robots, 
	ore, clay, obsidian, geode):
	return int(geode + geode_robots * minutes + (minutes)*(minutes-1)/2)

def heap_push(heap, minutes, 
	ore_robots, clay_robots, obsidian_robots, geode_robots, 
	ore, clay, obsidian, geode):
	heapq.heappush(heap, (
		-max_geode(minutes, ore_robots, clay_robots, obsidian_robots, geode_robots, ore, clay, obsidian, geode), 
		(minutes, ore_robots, clay_robots, obsidian_robots, geode_robots, ore, clay, obsidian, geode)
	))

def do(blueprint, minutes, 
	ore_robots, clay_robots, obsidian_robots, geode_robots, 
	ore, clay, obsidian, geode):
	heap = []
	visited = set() 

	heap_push(heap, minutes, ore_robots, clay_robots, obsidian_robots, geode_robots, ore, clay, obsidian, geode)

	while heap:
		_, value = heapq.heappop(heap)
		if value in visited:
			continue
		else:
			visited.add(value)
		(minutes, ore_robots, clay_robots, obsidian_robots, geode_robots, ore, clay, obsidian, geode) = value

		if minutes == 0:
			return geode
		minutes_left = minutes-1

		new_ore = ore + ore_robots
		new_clay = clay + clay_robots
		new_obsidian = obsidian + obsidian_robots
		new_geode = geode + geode_robots

		heap_push(heap, minutes_left,
			ore_robots, clay_robots, obsidian_robots, geode_robots,
			new_ore, new_clay, new_obsidian, new_geode
		)
		if ore >= blueprint.ore_ore_cost:
			heap_push(heap, minutes_left,
				ore_robots+1, clay_robots, obsidian_robots, geode_robots,
				new_ore-blueprint.ore_ore_cost, new_clay, new_obsidian, new_geode
			)
		if ore >= blueprint.clay_ore_cost:
			heap_push(heap, minutes_left,
				ore_robots, clay_robots+1, obsidian_robots, geode_robots,
				new_ore-blueprint.clay_ore_cost, new_clay, new_obsidian, new_geode
			)
		if ore >= blueprint.obsidian_ore_cost and clay >= blueprint.obsidian_clay_cost:
			heap_push(heap, minutes_left,
				ore_robots, clay_robots, obsidian_robots+1, geode_robots,
				new_ore-blueprint.obsidian_ore_cost, new_clay-blueprint.obsidian_clay_cost, new_obsidian, new_geode
			)
		if ore >= blueprint.geode_ore_cost and obsidian >= blueprint.geode_obsidian_cost:
			heap_push(heap, minutes_left,
				ore_robots, clay_robots, obsidian_robots, geode_robots+1,
				new_ore-blueprint.geode_ore_cost, new_clay, new_obsidian-blueprint.geode_obsidian_cost, new_geode
			)

part1 = sum(
	blueprint.num * do(blueprint, 24, 1, 0, 0, 0, 0, 0, 0, 0) 
	for blueprint in blueprints
)
print(part1)

part2 = functools.reduce(
	lambda a, b: a*b,
	(
		do(blueprint, 32, 1, 0, 0, 0, 0, 0, 0, 0) 
		for blueprint in blueprints[:3]
	)
)
print(part2)
