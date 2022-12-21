import numpy as np
import itertools
import functools

with open("day17.input") as f:
	inputs = f.read().strip()

shapes = [
	np.matrix([[0, 0, 1, 1, 1, 1, 0]]),
	np.matrix([[0, 0, 0, 1, 0, 0, 0], [0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 1, 0, 0, 0]]),
	np.matrix([[0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0, 0], [0, 0, 1, 1, 1, 0, 0]]),
	np.matrix([[0, 0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0]]),
	np.matrix([[0, 0, 1, 1, 0, 0, 0], [0, 0, 1, 1, 0, 0, 0]]),
]

def get_generator(inputs):
	i = 0
	while True:
		yield i, inputs[i]
		i = (i+1)%len(inputs)

def push(rock, direction):
	if direction == ">" and np.sum(rock[:,-1]) == 0:
		result = np.empty_like(rock)
		result[:,0], result[:,1:] = 0, rock[:,:-1]
		return result
	elif direction == "<" and np.sum(rock[:,0]) == 0:
		result = np.empty_like(rock)
		result[:,-1], result[:,:-1] = 0, rock[:,1:]
		return result
	return rock

def push_with_obstacles(rock, direction):
	unmovable = np.where(rock == 2)
	result = push(np.where(rock == 2, 0, rock), direction)
	if np.any(result[unmovable] == 1):
		return rock
	else:
		result[unmovable] = 2
		return result

def do(rocks, instructions, floor):
	rock_index, rock = next(rocks)
	for instruction_index, instruction in itertools.islice(instructions, 4):
		rock = push(rock, instruction)
	while not (floor.size == 0 or np.any(np.add(rock[-1,:], floor[0,:]) == 3)):
		rock, floor = np.vstack([rock, floor[0,:]]), floor[1:,:]
		movable = np.where(rock == 1)
		dest = (np.add(movable[0], 1), movable[1])
		if np.any(rock[dest] == 2):
			break
		rock[movable] = 0
		rock[dest] = 1
		rock = rock if np.sum(rock[0,:]) > 0 else rock[1:,:]
		instruction_index, instruction = next(instructions)
		rock = push_with_obstacles(rock, instruction)	
	floor = np.concatenate((np.where(rock == 1, 2, rock), floor), axis=0)
	return rock_index, instruction_index, floor 

def height(iterations):
	heights = {}
	instructions = get_generator(inputs)
	rocks = get_generator(shapes)
	floor = np.matrix([], dtype=int).reshape(0, 7)

	for i in range(iterations):
		if i != 0:
			value = hash(str(floor[:20]))
			if (rock_index, instruction_index, value) not in heights:
				rows, _ = floor.shape
				heights[(rock_index, instruction_index, value)] = (rows, i)
			else:
				break
		rock_index, instruction_index, floor = do(rocks, instructions, floor)

	end_loop_height, _ = floor.shape
	start_loop_height, start_loop_i = heights[(rock_index, instruction_index, value)]
	loop_height = end_loop_height - start_loop_height
	loop_i = i - start_loop_i

	for j in range((iterations - start_loop_i) % loop_i):
		_, _, floor = do(rocks, instructions, floor)

	final_height, _ = floor.shape
	return (loop_height * (int((iterations - start_loop_i) // loop_i) - 1)) + final_height

part1 = height(2022)
print(part1)

part2 = height(1000000000000)
print(part2)
