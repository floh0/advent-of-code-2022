with open("day02.input") as f:
	inputs = list(map(lambda line: line.strip().split(" "), f.readlines()))

class Strategy1:
	def __init__(self, name):
		if name == "X" or name == "A":
			self.score = 1
			self.win = "C"
			self.lose = "B"
		elif name == "Y" or name == "B":
			self.score = 2
			self.win = "A"
			self.lose = "C"
		else:
			self.score = 3
			self.win = "B"
			self.lose = "A"

	def winning_score(self, opponent):
		return 6 if self.win == opponent \
			else 0 if self.lose == opponent \
			else 3

def compute_score(strategy):
	score = 0
	for opponent, choice in inputs:
		selected = strategy(opponent, choice)
		score += selected.winning_score(opponent)
		score += selected.score
	return score

print(compute_score(lambda _, choice: Strategy1(choice)))

class Strategy2:
	def __init__(self, name, opponent):
		if name == "X":
			self.should_win = False
			self.should_lose = True
		elif name == "Y":
			self.should_win = False
			self.should_lose = False
		else:
			self.should_win = True
			self.should_lose = False

		if self.should_win:
			self.score = Strategy1(Strategy1(opponent).lose).score
		elif self.should_lose:
			self.score = Strategy1(Strategy1(opponent).win).score		
		else:
			self.score = Strategy1(opponent).score

	def winning_score(self, opponent):
		return 6 if self.should_win \
			else 0 if self.should_lose \
			else 3

print(compute_score(lambda opponent, choice: Strategy2(choice, opponent)))
