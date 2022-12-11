import re
import functools

parse_instruction = re.compile(r"^move (\d+) from (\d+) to (\d+)$")
parse_crate = re.compile(r"^(?:\[(\w)\]| {3}) ?(.*)$")

def extract_row(lines):
	for line in lines:
		m = parse_crate.match(line)
		if m:
			yield m.group(1), m.group(2)

def parse_inputs(crates):
	lines = crates.split("\n")
	while all(len(line) for line in lines):
		row, lines = zip(*extract_row(lines))
		yield list(filter(lambda x: x, row))

with open("day05.input") as f:
	top, bottom = f.read().split("\n\n")
	crates = list(parse_inputs(top)) 
	instructions = list(map(
		lambda line: list(map(int, parse_instruction.match(line).groups())), 
		bottom.split("\n")
	))

def do_instruction(moving, crates, instruction):
	how_many, where_from, where_to = instruction
	crates[where_from-1], to_move = crates[where_from-1][how_many:], crates[where_from-1][:how_many]
	crates[where_to-1] = moving(to_move) + crates[where_to-1]

def tops(moving, crates):
	for instruction in instructions:
		do_instruction(moving, crates, instruction)
	return "".join(row[0] for row in crates)

part1 = tops(lambda c: list(reversed(c)), crates.copy())
print(part1)

part2 = tops(lambda c: c, crates.copy())
print(part2)
