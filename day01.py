with open("day01.input") as f:
	inputs = list(map(
		lambda items: list(map(lambda item: int(item), items.split("\n"))),
		f.read().split("\n\n")
	))

sums = [sum(items) for items in inputs]

part1 = max(sums)
print(part1)

part2 = sum(sorted(sums)[-3:])
print(part2)