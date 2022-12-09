with open("day03.input") as f:
	sacks = list(map(lambda l: l.strip(), f))

def find_duplicate(sack):
	size = int(len(sack) / 2)
	return next(iter(set(sack[:size]).intersection(set(sack[size:]))))

def priority(item):
	value = ord(item)
	return value - 96 if value >= 97 else value - 38

part1 = 0
for sack in sacks:
	part1 += priority(find_duplicate(sack))
print(part1)

def batch(l, size):
	for i in range(0, len(l), size):
		yield l[i:i+size]

def find_common(a, b, c):
	return next(iter(set(a).intersection(set(b)).intersection(set(c))))

part2 = 0
for a, b, c in batch(sacks, 3):
	part2 += priority(find_common(a, b, c))
print(part2)