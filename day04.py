with open("day04.input") as f:
	inputs = list(map(
		lambda l: list(map(
			lambda p: list(map(int, p.split("-"))), 
			l.strip().split(",")
		)), f
	))

def included(a, b, c, d):
	return (a >= c and b <= d) or (c >= a and d <= b)

part1 = sum(1 for (a, b), (c, d) in inputs if included(a, b, c, d))
print(part1)

def overlaps(a, b, c, d):
	return c <= a <= d or a <= c <= b

part2 = sum(1 for (a, b), (c, d) in inputs if overlaps(a, b, c, d))
print(part2)
