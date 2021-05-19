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


class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
		self.zeroes = []
		self.ones = []
		self.done = []
		self.x_coord = startX
		self.y_coord = startY
		self.current = (startX+1, startY+1)
		self.flag = True
		print(f'Initial Point:{self.current}')
		self.zeroes.append(self.current)
		self.neighbours = self.__getNeighbours(self.current[0], self.current[1])

	def getAction(self, number: int) -> "Action Object":
		while self.flag:
			print(self.neighbours)
			print(f'Uncovered Number:{number}')
			if number == 0 and self.current not in self.zeroes and self.current not in self.done:
				self.zeroes.append(self.current)
			elif number == 1 and self.current not in self.ones and self.current not in self.done:
				self.ones.append(self.current)
			print(f'Zeroes List:{self.zeroes}')
			print(f'Ones List:{self.ones}')
			print(f'Done List:{self.done}')


			if len(self.done) + len(self.ones) == 24:
				return Action(AI.Action.LEAVE)
			if len(self.neighbours) >= 1:
				self.current = self.neighbours.pop(0)
				print(f'Current Point:{self.current}')
				x = self.current[0] - 1
				y = self.current[1] - 1
				action = AI.Action.UNCOVER
				return Action(action, x, y)

			u = self.zeroes.pop(0)
			if u not in self.done:
				self.done.append(u)
			if len(self.zeroes) >= 1:
				self.current = self.zeroes.pop(0)
				if self.current not in self.done:
					self.done.append(self.current)
				x = self.current[0]
				y = self.current[1]
				print(f'Finding Neighbors for:({x}, {y})')
				self.neighbours = self.__getNeighbours(x, y)
			print(f'New neighbours: {self.neighbours}')
			self.neighbours = [x for x in self.neighbours if x not in self.zeroes and x not in self.ones and x not in self.done]
			print(f'Modified neighbours: {self.neighbours}')
			print(f'CARRY OVER CURRENT: {self.current}')

		return Action(action, x, y)

	#####################################################
	#		         HELPER FUNCTIONS					#
	#####################################################
	def __getPoint(self, x: int, y: int) -> int:
		""" Return an xy representation of x and y as an integer"""
        # Convert both the numbers to strings
		num1 = str(x)
		num2 = str(y)

        # Concatenate the strings
		num1 += num2

		return int(num1)

	def __splitPoint(self, x: int) -> int:
		""" Return the x and y co-ordinates"""
		co_ords = [int(digit) for digit in str(x)]
		return co_ords

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

		valid_neighbours = [x for x in neighbours if x[0] > 0 and x[0] < 5 and x[1] > 0 and x[1] < 5]

		return valid_neighbours
