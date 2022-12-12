import heapq

with open("day12.input") as f:
	heightmap = f.read()

matrix = list(map(lambda elem: list(elem.strip()), heightmap.split("\n")))
width = len(matrix[0])
length = len(matrix)

def find_index(of, matrix):
	return next((i, line.index(of)) for i, line in enumerate(matrix) if of in line)

start = a,b = find_index("S", matrix)
end = c,d = find_index("E", matrix)

matrix[a][b] = "a"
matrix[c][d] = "z"

def find_shortest(start, end, matrix):
	current = start
	visited = set()
	to_visit = [(0, start)]

	while current != end:
		try:
			distance, current = _, (x,y) = heapq.heappop(to_visit)
		except IndexError:
			return None
		if current not in visited:
			visited.add(current)
			for (i,j) in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
				if 0 <= i < length and 0 <= j < width and ord(matrix[i][j]) - ord(matrix[x][y]) <= 1:
					heapq.heappush(to_visit, (distance+1, (i,j)))

	return distance

part1 = find_shortest(start, end, matrix)
print(part1)

all_paths = (find_shortest((i,j), end, matrix) for i, line in enumerate(matrix) for j, height in enumerate(line) if height in "a")
part2 = min(filter(lambda x: x, all_paths))
print(part2)
