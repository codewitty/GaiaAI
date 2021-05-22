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
        self.val2 = 0 # Effective Label
        self.val3 = 8   # Number of neighbors that are covered or unmarked

class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
		self.zeroes = []
		self.ones = []
		self.done = []
		self.row = rowDimension
		self.col = colDimension
		self.x_coord = startX
		self.y_coord = startY
		self.current = (startX+1, startY+1)
		print(f'We\'re entering the init here: Current Position: {self.current[0]},{self.current[1]}')
		self.flag = True
		self.zeroes.append(self.current)
		
		# Changes I made are below
		self.__initializeboard() # NEW
		self.timestoUncover = (rowDimension * colDimension) - totalMines # NEW
		self.timesUncovered = 1 # NEW
		self.__updateboardneighbors(self.current[0], self.current[1])
		self.neighbors = self.__getCoveredNeighbors(self.current[0]-1, self.current[1]-1)


	def getAction(self, number: int) -> "Action Object":
		if (self.board[self.current[0]-1][self.current[1]-1].val1 == '*'):
			self.__updateboardneighbors(self.current[0], self.current[1])
			self.__updateboard(self.current[0], self.current[1], number) # NEW
		print(f'We\'re at the top again: Current Position: {self.current[0]},{self.current[1]}, Current Hint: {number}')
		print(f'Current Neighbors: {self.neighbors}')

		self.__printboard2() # NEW Uncomment to use (Only if running in debug mode)
		
		#self.__printboard() # NEW Uncomment to use (Only if running in debug mode)
		while self.flag:
			print(f'Trace 1')
			if self.timesUncovered == self.timestoUncover: # new unhardcoded exit condition
				return Action(AI.Action.LEAVE)

			if len(self.neighbors) >= 1:
				print(f'Inside while loop')
				self.current = self.neighbors.pop(0)
				x = self.current[0] - 1
				y = self.current[1] - 1
				action = AI.Action.UNCOVER
				self.timesUncovered += 1
				print(f'About to uncover: {x+1}, {y+1}')
				return Action(action, x, y)

			else:
				for i in range(8):	
					for j in range(8):
						#print('Hello')
						if (self.board[i][j].val1) == 0 and self.board[i][j].val3 > 0:
							#print(f'FOUND!! Position : ({i+1}, {j+1})')
							action = AI.Action.UNCOVER
							self.timesUncovered += 1
							#print(f'About to uncover: {i+1}, {j+1}')
							self.neighbors = self.__getCoveredNeighbors(i, j)
							print(f'Covered Neighbors to uncover: {i+1}, {j+1}')
							return Action(action, i, j)

				print('ZEROES DONE')
				self.ones = self.__generateOnesList()
				#print(self.ones)
				print('Gonna print board before if statament now')
				self.__printboard2()
				for one in self.ones:
					#print("searching")
					print(f'Coordinate of {one} has val1 of {self.board[one[0]-1][one[1]-1].val1} and val3 of {self.board[one[0]-1][one[1]-1].val3}')

					if int(self.board[one[0]-1][one[1]-1].val1) == int(self.board[one[0]-1][one[1]-1].val3):
						print(f'These triggered if statement: {one}')
						#self.__printboard2()
						neighbors = self.__getneighbors(one[0],one[1])
						#print(f'Coordinate is {one}, and neighbors is {neighbors}')
						for neighbor in neighbors:
							if self.board[neighbor[0]-1][neighbor[1]-1].val1 == '*' and self.board[one[0]-1][one[1]-1].val2 != 0:
								self.board[neighbor[0]-1][neighbor[1]-1].val1 = 'B'
								self.__updateboardneighbors(neighbor[0],neighbor[1])
								self.__updateEffectiveLabel(neighbor[0],neighbor[1])
				print('We are down to the second for loop')
				
				#neighbors = self.__getneighbors(i+1, j+1)
				#self.neighbors = [x for x in neighbors if self.board[x[0]-1][x[1]-1].val1 == '*']
				#print(neighbors)
				for one in self.ones:
					print(one)
					if self.board[one[0]-1][one[1]-1].val1 == '*' and self.board[one[0]-1][one[1]-1].val2 == 0:
						x = one[0] - 1
						y = one[1] - 1
						#print(f'X is {x} and Y is {y}')
						self.neighbors.append((x+1,y+1))
					
						self.timesUncovered += 1
						#self.__printboard2()
				#print('About to uncover right now')	
				print(self.neighbors)		
				action = AI.Action.UNCOVER
				self.current = self.neighbors.pop(0)
				x = self.current[0] - 1
				y = self.current[1] - 1
				self.timesUncovered += 1
				#print(f'About to uncover: {x+1}, {y+1}')
				return Action(action, x, y)
				
			return Action(AI.Action.LEAVE)





	#####################################################
	#		         HELPER FUNCTIONS					#
	#####################################################
	def __getneighbors(self, x: int, y: int) -> List:
		""" Return a list of all neighbors of the given co-ordinate"""
		neighbors = []
		neighbors.append((x, y + 1))
		neighbors.append((x, y - 1))
		neighbors.append((x + 1, y))
		neighbors.append((x - 1, y))
		neighbors.append((x + 1, y + 1))
		neighbors.append((x - 1, y + 1))
		neighbors.append((x - 1, y - 1))
		neighbors.append((x + 1, y - 1))
		valid_neighbors = [x for x in neighbors if x[0] > 0 and x[0] <= self.row and x[1] > 0 and x[1] <= self.row]
		return valid_neighbors

	def __getCoveredNeighbors(self, x: int, y: int) -> List:
		""" Return a list of all neighbors of the given co-ordinate"""
		neighbors = self.__getneighbors(x+1, y+1)
		covered_neighbors = [i for i in neighbors if self.board[i[0]-1][i[1]-1].val1 == '*']
		return covered_neighbors

	# This helper function initializes the board according to the model from Kask's discussion
	def __initializeboard(self) -> None: # NEW
		self.board = [[i for i in range(self.row)] for j in range(self.row)]
		for i in range(self.row):
			for j in range(self.row):
				tile = Tile()
				self.board[i][j] = tile
		self.board[self.x_coord][self.y_coord].val1 = 0 # You can assume first label always 0

		for i in range(self.row): 
			self.board[0][i].val3 = 5
			self.board[-1][i].val3 = 5
		for i in range(self.col):
			self.board[i][0].val3 = 5
			self.board[i][-1].val3 = 5
		self.board[0][0].val3 = 3
		self.board[self.col-1][self.row-1].val3 = 3
		self.board[0][self.row-1].val3 = 3
		self.board[self.col-1][0].val3 = 3

	# This helper function prints out how the model looks in terms of our board nested array
	# You have to look at it sideways
	# Indices are accurate for this one
	def __printboard(self) -> None: # NEW
		counter = 0
		for i in range(self.row):
			print('     ' + str(i) + '   ', end="")
		print()
		for i in range(self.row):
			print('   ' + '-----' + ' ', end="")
		print()
		flag = True
		for l in self.board:
			for tile in l:
				if flag == True:
					print(str(counter) + '|', end=" ")
					flag = False
				print(str(tile.val1) + ':' + str(tile.val2) + ':' + str(tile.val3) + '   ', end=" ")
			flag = True
			counter+= 1
			print()
	
	# This helper function prints out how the model looks on the actual board
	# It basically flips the board from __printboard sideways so you can see how it actually looks
	# Indices are inaccurate in this case so ignore those because the board was flipped sideways
	def __printboard2(self) -> None: # NEW
		counter = 0
		subtract = -1
		for i in range(self.row):
			print('     ' + str(i) + '   ', end="")
		print()
		for i in range(self.row):
			print('   ' + '-----' + ' ', end="")
		print()
		flag = True
		for i in range(self.row):
			for j in range(self.col):
				if flag == True:
					print(str(counter) + '|', end=" ")
					flag = False
				print(str(self.board[j][subtract].val1) + ':' + 
				      str(self.board[j][subtract].val2) + ':' + 
					  str(self.board[j][subtract].val3) + '   ', end=" ")
			flag = True
			counter+= 1
			subtract -= 1
			print()

	# Updates our board's labels as we uncover
	# Does not have functionality for changing anything but the label only so far
	# Coordinate of current tile to uncover must be subtracted by 1 before accessing the board
	def __updateboard(self, x: int, y: int, label: int) -> None: # NEW
		self.board[x-1][y-1].val1 = int(label)
		self.board[x-1][y-1].val2 = int(label)

	def __updateboardneighbors(self, x: int, y: int) -> None:
		neighbors = self.__getneighbors(x,y)
		for neighbor in neighbors:
			self.board[neighbor[0]-1][neighbor[1]-1].val3 -= 1

	def __generateOnesList(self) -> None:
		ones = []
		for i in range(8):
			for j in range(8):	
				if (self.board[i][j].val1) == 1:
					ones.append((i+1,j+1))
		return ones
	
	def __updateEffectiveLabel(self, x: int, y: int) -> None:
		bombneighbors = self.__getneighbors(x,y)
		for neighbor in bombneighbors:
			if self.board[neighbor[0]-1][neighbor[1]-1].val1 == '*':
				self.board[neighbor[0]-1][neighbor[1]-1].val2 = -1
			else:
				self.board[neighbor[0]-1][neighbor[1]-1].val2 -= 1


