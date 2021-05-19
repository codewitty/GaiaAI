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
import time


class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
		self.zeroes = []
		self.ones = []
		self.done = set() 
		self.x_coord = startX
		self.y_coord = startY
		self.current = (startX+1, startY+1)
		self.flag = True
		self.zeroes.append(self.current)
		self.neighbours = self.__getNeighbours(self.current[0], self.current[1])

	def getAction(self, number: int) -> "Action Object":
		
		while self.flag:
			if number == 0 and self.current not in self.zeroes and self.current not in self.done:
				self.zeroes.append(self.current)
			elif number == 1 and self.current not in self.ones and self.current not in self.done:
				self.ones.append(self.current)


			if len(self.done) + len(self.ones) == 24:
				return Action(AI.Action.LEAVE)
			if len(self.neighbours) >= 1:
				self.current = self.neighbours.pop(0)
				x = self.current[0] - 1
				y = self.current[1] - 1
				action = AI.Action.UNCOVER
				return Action(action, x, y)

			u = self.zeroes.pop(0)
			if u not in self.done:
				self.done.add(u)
			if len(self.zeroes) >= 1:
				self.current = self.zeroes[0]
				if self.current not in self.done:
					self.done.add(self.current)
				x = self.current[0]
				y = self.current[1]
				self.neighbours = self.__getNeighbours(x, y)
			self.neighbours = [x for x in self.neighbours if x not in self.zeroes and x not in self.ones and x not in self.done]

			if len(self.zeroes) == 0:
				for coord in self.ones:
					x = coord[0]
					y = coord[1]
					neighbors = self.__getNeighbours(x,y)
					neighbors = [x for x in neighbors if x not in self.ones and x not in self.done]
					if len(neighbors) == 1:
						bomb = neighbors[0]
					else:
						continue
			
				x = bomb[0]
				y = bomb[1]
				self.neighbours = self.__getNeighbours(x, y)
				self.neighbours = [x for x in self.neighbours if x not in self.ones and x not in self.done]



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

		valid_neighbours = [x for x in neighbours if x[0] > 0 and x[0] <= 5 and x[1] > 0 and x[1] <= 5]

		return valid_neighbours
