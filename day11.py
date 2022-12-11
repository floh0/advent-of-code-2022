import re
import functools

with open("day11.input") as f:
	inputs = f.read().split("\n\n")

parse = re.compile(r"^Monkey (\d):\n  Starting items: ([^\n]+)\n  Operation: ([^\n]+)\n  Test: divisible by (\d+)\n    If true: throw to monkey (\d+)\n    If false: throw to monkey (\d+)$")

class Monkey:
	def __init__(self, values):
		self.num = int(values[0])
		self.items = list(map(int, values[1].split(",")))
		self.worrio = values[2]
		self.divisible = int(values[3])
		self.true = int(values[4])
		self.false = int(values[5])
		self.inspected = 0

monkeys= list(map(
	lambda monkey: Monkey(parse.match(monkey).groups()), 
	inputs
))

def play_round(monkeys, manage):
	for monkey in monkeys:
		while len(monkey.items) > 0:
			item = monkey.items[0]
			monkey.inspected += 1
			_locals = {"old": item}
			exec(monkey.worrio, globals(), _locals)
			new = _locals["new"]
			new = manage(new)
			sendto = monkey.false if new % monkey.divisible else monkey.true
			monkeys[sendto].items.append(new)
			monkey.items.pop(0)

def business(monkeys):
	top2 = sorted(monkeys, key=lambda monkey: monkey.inspected, reverse=True)[:2]
	return top2[0].inspected * top2[1].inspected

def play_rounds(rounds, monkeys, manage):
	for _ in range(rounds):
		play_round(monkeys, manage)
	return business(monkeys)

part1 = play_rounds(20, monkeys.copy(), lambda worry: int(worry / 3))
print(part1)

ppcm = functools.reduce(lambda a,b: a*b, map(lambda monkey: monkey.divisible, monkeys))
part2 = play_rounds(10000, monkeys.copy(), lambda worry: worry % ppcm)
print(part2)
