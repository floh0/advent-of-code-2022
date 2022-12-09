with open("day09.input") as f:
	inputs = list(map(
		lambda e: (e[0], int(e[1])),
		map(lambda l: l.strip().split(" "), f)
	))

def move_head(direction, hx, hy):
	if direction == "R":
		hx += 1
	elif direction == "L":
		hx -= 1
	elif direction == "U":
		hy += 1
	elif direction == "D":
		hy -= 1
	return hx, hy

def move_tail(hx, hy, tx, ty):
	if hx - tx > 1 and hy - ty > 1:
		tx, ty = hx - 1, hy - 1
	elif tx - hx > 1 and hy - ty > 1:
		tx, ty = hx + 1, hy - 1
	elif hx - tx > 1 and ty - hy > 1:
		tx, ty =  hx - 1, hy + 1
	elif tx - hx > 1 and ty - hy > 1:
		tx, ty = hx + 1, hy + 1
	elif hx - tx > 1:
		tx, ty = hx - 1, hy
	elif tx - hx > 1:
		tx, ty = hx + 1, hy
	elif hy - ty > 1:
		tx, ty = hx, hy - 1
	elif ty - hy > 1:
		tx, ty = hx, hy + 1
	return tx, ty

hx, hy, tx, ty = 0, 0, 0, 0
visited = {(tx, ty)}

for (direction, number) in inputs:
	for _ in range(number):
		hx, hy = move_head(direction, hx, hy)
		tx, ty = move_tail(hx, hy, tx, ty)
		visited.add((tx, ty))

part1 = len(visited)
print(part1)

def move_rope(direction, parts):
	head = parts[0]
	head[0], head[1] = move_head(direction, head[0], head[1])
	for i in range(len(parts)-1):
		knot, following = parts[i:i+2]
		following[0], following[1] = move_tail(knot[0], knot[1], following[0], following[1])

length = 10
rope = [[0, 0] for _ in range(length)]
new_visited = {(rope[-1][0], rope[-1][1])}

for (direction, number) in inputs:
	for _ in range(number):
		move_rope(direction, rope)
		new_visited.add((rope[-1][0], rope[-1][1]))

part2 = len(new_visited)
print(part2)