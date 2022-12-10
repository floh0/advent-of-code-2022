import re

noop = re.compile(r"^noop$")
addx = re.compile(r"^addx (-?\d+)$")

def parse_line(line):
	if noop.match(line):
		return None
	else:
		m = addx.match(line)
		return int(m.group(1))

with open("day10.input") as f:
	instructions = [parse_line(line) for line in f]

checkpoints = [20, 60, 100, 140, 180, 220]

def incr_cycle(cycle, x, strength):
	cycle += 1
	return cycle, strength + cycle * x if cycle in checkpoints else strength

def execute_program(cycle, x, value, func):
	for instruction in instructions:
		cycle, value = func(cycle, x, value)
		if instruction is not None:
			cycle, value = func(cycle, x, value)
			x += instruction
	return value

part1 = execute_program(cycle=0, x=1, value=0, func=incr_cycle)
print(part1)

def move_sprite(pixel, x, sprite):
	sprite += "🤠" if x-1 <= pixel <= x+1 else "🔲"
	if pixel >= 39:
		pixel = 0
		sprite += "\n"
	else:
		pixel += 1
	return pixel, sprite

part2 = execute_program(cycle=0, x=1, value="", func=move_sprite)
print(part2)
