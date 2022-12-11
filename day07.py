with open("day07.input") as f:
	lines = list(map(
		lambda result: list(map(
			lambda command: command.split(" "),
			result.strip().split("\n")
		)),
		f.read().replace("$", "\n").split("\n\n")
	))

class File:
	def __init__(self, size):
		self.size = size

class Directory:
	def __init__(self, files, parent):
		self.files = files
		self.parent = parent
		self.size = None

def populate(lines):
	base = Directory({}, None)
	for line in lines:
		command, results = line[0], line[1:]
		if command[0] == "cd":
			where = command[1]
			if where == "/":
				current = base
			elif where == "..":
				current = current.parent
			else:
				if where in current.files:
					current = current.files[where]
				else:
					current.files[where] = Directory({}, current)
					current = current.files[where]
		elif command[0] == "ls":
			for what, name in results:
				if name not in current.files:
					if what == "dir":
						current.files[name] = Directory({}, current)
					else:
						current.files[name] = File(int(what))
	return base

def compute_sizes(something):
	if isinstance(something, Directory) and something.size is None:
		computed = sum(compute_sizes(elem) for elem in something.files.values())
		something.size = computed
	return something.size

def find_interesting(something, interesting, comparison):
	if isinstance(something, Directory):
		if comparison(something.size):
			interesting.append(something.size)
		for anything in something.files.values():
			find_interesting(anything, interesting, comparison)
	return interesting

tree = populate(lines)
compute_sizes(tree)

part1 = sum(find_interesting(tree, [], lambda size: size <= 100000))
print(part1)

free_space_needed = 30000000-(70000000-tree.size)
part2 = min(find_interesting(tree, [], lambda size: size >= free_space_needed))
print(part2)



