with open("day20.input") as f:
	numbers = list(map(int, f))

class DoublyLinkedList:
	def __init__(self, current, nodes):
		self.current = current
		self.after = None
		self.before = None
		nodes.append(self)

def create_linked_list(numbers, transform):
	nodes = []
	first = DoublyLinkedList(transform(numbers[0]), nodes)
	previous = first
	for number in numbers[1:]:
		current = DoublyLinkedList(transform(number), nodes)
		previous.after = current
		current.before = previous
		previous = current
	current.after = first
	first.before = current
	return nodes

def move_first(linkedlist, length):
	to_move = linkedlist
	should_go_left = to_move.current < 0
	how_many = abs(to_move.current) % (length-1)
	if how_many != 0:
		linkedlist.after.before = linkedlist.before
		linkedlist.before.after = linkedlist.after
		if should_go_left:
			for _ in range(how_many):
				linkedlist = linkedlist.before
			to_move.before = linkedlist.before
			to_move.after = linkedlist
		else:
			for _ in range(how_many):
				linkedlist = linkedlist.after
			to_move.after = linkedlist.after
			to_move.before = linkedlist
		to_move.before.after = to_move
		to_move.after.before = to_move

def do(numbers, transform, mix):
	nodes = create_linked_list(numbers, transform)
	for _ in range(mix):
		for node in nodes:
			move_first(node, len(numbers))
	result = 0
	zero = next(node for node in nodes if node.current == 0)
	for _ in range(3):
		for _ in range(1000):
			zero = zero.after
		result += zero.current
	return result

part1 = do(numbers, lambda x: x, 1)
print(part1)

part2 = do(numbers, lambda x: 811589153*x, 10)
print(part2)