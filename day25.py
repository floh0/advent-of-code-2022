with open("day25.input") as f:
	lines = list(map(lambda line: line.strip(), f))

snapy_to_decimal = {
	"2": 2,
	"1": 1,
	"0": 0,
	"-": -1,
	"=": -2
}

decimal_to_snapy = {
	0: ("0", lambda x: x),
	1: ("1", lambda x: x),
	2: ("2", lambda x: x),
	3: ("=", lambda x: x+2),
	4: ("-", lambda x: x+1)
}

def to_decimal(number):
	result = 0
	for i, value in enumerate(reversed(number)):
		result += snapy_to_decimal[value] * 5**i
	return result

def to_snafu(number):
	digit, transformation = decimal_to_snapy[number % 5]
	remainder = transformation(number) // 5
	return digit if remainder == 0 else to_snafu(remainder)+digit

part1 = to_snafu(sum(to_decimal(line) for line in lines))
print(part1)