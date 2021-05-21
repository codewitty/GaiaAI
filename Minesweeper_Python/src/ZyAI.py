# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action
from typing import List

# CHANGES MADE #
################
# Tile class added so that we can add tile objects into our board model
# Board model created and initialized
# Board model kind of updated as we uncover
# Board model can be printed out in two different formats (printboard() or printboard2())
# Exit condition made to be unhardcoded

class Tile: # NEW
    def __init__(self):
        self.val1 = '*' # Covered/Marked or covered/Unmarked or Label
        self.val2 = ' ' # Effective Label
        self.val3 = 8   # Number of neighbors that are covered or unmarked

class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
		self.zeroes = []
		keys = [0,1,2,3,5,6,7,8]
		self.boardTracker = {key: [] for key in keys}
		self.ones = []
		self.uncovered = []
		self.done = []      # No uncovered neighbors remaining
		self.mines = []      # Positions with mines
		self.row = rowDimension
		self.col = colDimension
		self.x_coord = startX
		self.y_coord = startY
		self.current = (startX+1, startY+1)
		self.flag = True
		self.zeroes.append(self.current)
		self.boardTracker[0].append(self.current)
		self.neighbours = self.__getNeighbours(self.current[0], self.current[1])
		self.all = self.__generateAll(rowDimension, colDimension)
		self.total = (rowDimension * colDimension)
		self.totalMines = totalMines
		self.all.remove(self.current)

	def getAction(self, number: int) -> "Action Object":
		print(self.all)
		print(self.boardTracker)

		while self.flag:
			if self.totalMines + len(self.uncovered) == self.total:
				return Action(AI.Action.LEAVE)

			if number == 0 and self.current not in self.zeroes and self.current not in self.uncovered:
				self.zeroes.append(self.current)
				try:
					self.all.remove(self.current)
				except ValueError:
					pass  # do nothing!
			elif number == 1 and self.current not in self.ones and self.current not in self.uncovered:
				self.ones.append(self.current)
				try:
					self.all.remove(self.current)
				except ValueError:
					pass  # do nothing!
			
			if len(self.neighbours) >= 1:
				self.current = self.neighbours.pop(0)
				x = self.current[0] - 1
				y = self.current[1] - 1
				action = AI.Action.UNCOVER
				return Action(action, x, y)

			u = self.zeroes.pop(0)
			if u not in self.uncovered:
				self.uncovered.append(u)
				self.all.remove(self.current)
			if len(self.zeroes) >= 1:
				self.current = self.zeroes[0]
				if self.current not in self.uncovered:
					self.uncovered.append(self.current)
				x = self.current[0]
				y = self.current[1]
				self.neighbours = self.__getNeighbours(x, y)
			self.neighbours = [x for x in self.neighbours if x not in self.zeroes and x not in self.ones and x not in self.uncovered]


			if len(self.zeroes) == 0:
				for position in self.uncovered:
					self.uncovered.append(self.current)


	#####################################################
	#		         HELPER FUNCTIONS					#
	#####################################################
	def __getNeighbours(self, x: int, y: int) -> List:
		""" Return a list of all neighbours of the given co-ordinate"""
		neighbours = []
		neighbours.append((x, y + 1))
		neighbours.append((x, y - 1))
		neighbours.append((x + 1, y))
		neighbours.append((x - 1, y))
		neighbours.append((x + 1, y + 1))
		neighbours.append((x - 1, y + 1))
		neighbours.append((x - 1, y - 1))
		neighbours.append((x + 1, y - 1))
		valid_neighbours = [x for x in neighbours if x[0] > 0 and x[0] <= self.row and x[1] > 0 and x[1] <= self.row]
		return valid_neighbours

	def __generateAll(self, x: int, y: int) -> List:
		""" Return a list of all possible board positions"""
		positions = []
		for i in range(1, x+1):
			for j in range(1, y+1):
				positions.append((i, j))
		return positions

	def __getCoveredNeighbors(self, x: int, y: int) -> List:
		""" Return a list of all uncovered neighbors"""
		covered_neigh = self.__getNeighbors(x, y)
		valid_neighbours = [x for x in uncovered_neigh if x not in self.uncovered] 
		return covered_neigh
