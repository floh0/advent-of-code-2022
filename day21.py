import re

with open("day21.input") as f:
	inputs = { key: value 
		for key,value in map(lambda line: line.strip().split(": "), f)
	}

def do(instructions):
	values = {}
	while True:
		previous = len(values)
		for key, instruction in instructions:
			if key not in values:
				try:
					exec(f"{key}=int({instruction})", globals(), values)
				except NameError:
					pass
		if previous == len(values):
			break
	return values

part1 = do(inputs.items())["root"]
print(part1)

parse = re.compile(r"(\w+) (.) (\w+)")
opposite = {
	"+": "-",
	"-": "+",
	"*": "/",
	"/": "*"
}
def transform(inputs):
	for key, value in inputs.items():
		parsed = parse.match(value)
		if parsed:
			left, symbol, right = parsed.groups()
			if key == "root":
				for a in (key, left, right):
					for b in (key, left, right):
						yield a, b
			else:
				yield key, f"{left}{symbol}{right}"
				yield left, f"{key}{opposite[symbol]}{right}"
				if symbol in ("-", "/"):
					yield right, f"{left}{symbol}{key}"
				else:
					yield right, f"{key}{opposite[symbol]}{left}"
		elif key != "humn":
			yield key, value

part2 = do(list(transform(inputs)))["humn"]
print(part2)