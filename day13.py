import itertools
import functools

with open("day13.input") as f:
	inputs = list(map(
		lambda line: list(map(eval, line.split("\n"))),
		f.read().split("\n\n")
	))

def compare(left, right):
	if isinstance(left, int) and isinstance(right, int):
		return None if left == right else left < right
	else:
		for left, right in itertools.zip_longest(
			[left] if isinstance(left, int) else left, 
			[right] if isinstance(right, int) else right
		):
			if left is None:
				return True
			elif right is None:
				return False
			else:
				result = compare(left, right)
				if result is not None:
					return result

part1 = sum(i for i, (left, right) in enumerate(inputs, 1) if compare(left, right))
print(part1)

additional = [[[2]], [[6]]]
flattened = [line for lines in inputs for line in lines] + additional
transformed_compare = functools.cmp_to_key(lambda a,b: -1 if compare(a,b) else 1)
organized = sorted(flattened, key=transformed_compare)
part2 = functools.reduce(lambda a,b: a*b, (i for i, elem in enumerate(organized, 1) if elem in additional))
print(part2)