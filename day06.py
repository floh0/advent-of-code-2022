with open("day06.input") as f:
	buffer = f.read()

def sliding(l, n):
	for i in range(n, len(l)):
		yield (i, l[i-n:i])

def first(size):
	return next(i for i, elem in sliding(buffer, size) if len(set(elem)) == size)

part1 = first(4)
print(part1)

part2 = first(14)
print(part2)