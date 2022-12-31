with open("day23.input") as f:
	lines = list(map(lambda line: list(line.strip()), f))			

def get_elves(lines):
	return [ (i,j)
		for i in range(len(lines))
		for j in range(len(lines[i]))
		if lines[i][j] == "#"
	]
	
def consider(elves, x, y):
	for i in range(-1, 2):
		for j in range(-1, 2):
			if (i, j) != (0, 0) and (x+i,y+j) in elves:
				return True
	return False

def propose(x, y, elves, directions):
	for direction, choice in directions:
		if choice(x, y, elves):
			if direction == "n":
				return (x-1, y)
			elif direction == "s":
				return (x+1, y) 
			elif direction == "w":
				return (x, y-1)
			elif direction == "e":
				return (x, y+1)

def propose_all(proposed, elves, directions):
	choices = {}
	for i in range(len(elves)):
		if consider(elves, *elves[i]):
			proposed[i] = propose(*elves[i], elves, directions)
			if proposed[i]:
				if proposed[i] in choices:
					choices[proposed[i]] += 1
				else:
					choices[proposed[i]] = 1
	return proposed, choices

def remove_conflicts(proposed, choices):
	for i in range(len(proposed)):
		if proposed[i] in choices and choices[proposed[i]] > 1:
			proposed[i] = None
	return proposed

def move_all(removed, elves):
	for i in range(len(elves)):
		if removed[i]:
			elves[i] = removed[i]
	return elves

def go(lines, stop):
	directions = [
		("n", lambda x,y,elves: all((x-1,y+i) not in elves for i in range(-1, 2))),
		("s", lambda x,y,elves: all((x+1,y+i) not in elves for i in range(-1, 2))),
		("w", lambda x,y,elves: all((x+i,y-1) not in elves for i in range(-1, 2))),
		("e", lambda x,y,elves: all((x+i,y+1) not in elves for i in range(-1, 2)))
	]
	elves = get_elves(lines)
	proposed = [None for _ in elves]
	i = 0
	previous = None
	current = hash(str(elves))
	while not stop(previous, current, i):
		proposed, choices = propose_all(proposed, elves, directions)
		removed = remove_conflicts(proposed, choices)
		elves = move_all(removed, elves)
		directions = directions[1:] + directions[:1]
		previous = current
		current = hash(str(elves))
		i += 1
	return elves, i

def ground(elves):
	keys = iter(elves)
	first = next(keys)
	(minx, miny), (maxx, maxy) = first, first
	for (x, y) in keys:
		minx, miny, maxx, maxy = min(minx, x), min(miny, y), max(maxx, x), max(maxy, y)
	area = (1+maxx-minx)*(1+maxy-miny)
	return area - len(elves)

elves, _ = go(lines, lambda previous, current, i: i == 10)
part1 = ground(elves)
print(part1)

_, part2 = go(lines, lambda previous, current, i: previous == current)
print(part2)