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
import random 


class Tile: 
    def __init__(self):
        self.val1 = '*' # Covered/Marked or covered/Unmarked or Label
        self.val2 = 0   # Effective Label
        self.val3 = 8   # Number of neighbors that are covered or unmarked
        self.val4 = 0   # Probability field

class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
		self.zeroes = []
		self.total = 0
		self.ones = []
		self.bombs = []
		self.row = rowDimension
		self.col = colDimension
		print(self.row, self.col)
		self.x_coord = startX
		self.y_coord = startY
		self.current = (startX+1, startY+1)
		self.flag = True
		self.zeroes.append(self.current)
		self.__initializeboard() 
		self.timestoUncover = (rowDimension * colDimension)
		self.__updateboardneighbors(self.current[0], self.current[1])
		self.neighbors = self.__getCoveredNeighbors(self.current[0]-1, self.current[1]-1)


	def getAction(self, number: int) -> "Action Object":
		if (self.board[self.current[0]-1][self.current[1]-1].val1 == '*'):
			self.__updateboardneighbors(self.current[0], self.current[1])
			self.__updateboard(self.current[0], self.current[1], number) 
		
		#self.__printboard()  Uncomment to use (Only if running in debug mode)
		#self.__printboard2()  Uncomment to use (Only if running in debug mode)
		while self.flag: 
			self.total = 0
			for i in range(self.row):	
				for j in range(self.col):
					if self.board[i][j].val1 != '*':
						self.total += 1
			if self.total == self.timestoUncover:
				return Action(AI.Action.LEAVE)

			# Uncovers anyone in self.neighbors
			if len(self.neighbors) >= 1:
				self.current = self.neighbors.pop(0)
				x = self.current[0] - 1
				y = self.current[1] - 1
				action = AI.Action.UNCOVER
				return Action(action, x, y)

			# If self.neighbors is empty we must use algorithms to add more to uncover
			# Below clears every 0
			else:
				for i in range(self.row):	
					for j in range(self.col):
						if self.board[i][j].val1 == 0 and self.board[i][j].val3 > 0:
							action = AI.Action.UNCOVER
							self.neighbors = self.__getCoveredNeighbors(i, j)
							if len(self.neighbors) >= 1:
								new = self.neighbors.pop(0)
							self.current = new
							return Action(action, new[0]-1, new[1]-1)

				# Below clears marks bombs around ones and updates
				self.ones = self.__generateOnesList()

				for one in self.ones:
					if int(self.board[one[0]-1][one[1]-1].val1) == int(self.board[one[0]-1][one[1]-1].val3):
						neighbors = self.__getneighbors(one[0],one[1]) # Neighbors of all tiles where num of label is equal to uncovered tiles
						#print(f'Tile Coordinate is {one}, and neighbors is {neighbors}')
						#print(f'CHECKING')
						for neighbor in neighbors: # for each neighbor in those neighbors
							if self.board[neighbor[0]-1][neighbor[1]-1].val1 == '*' and self.board[neighbor[0]-1][neighbor[1]-1].val2 != 9: # if the neighbor is covered
								self.board[neighbor[0]-1][neighbor[1]-1].val1 = 'B' # mark it as a bomb
								self.bombs.append((neighbor[0],neighbor[1])) # add coordinate of bomb to bomb list
				
				# now all bombs have been appended to bomb list
				for bomb in self.bombs:	 # now update neighbors of each bomb coordinate
					self.__updateboardneighbors(bomb[0],bomb[1])
					self.__updateEffectiveLabel(bomb[0],bomb[1])

			# now that bombs around ones are marked, we want to uncover all tles with effective label 0	
			self.neighbors = self.__getCoordsofEffectiveZeroes()
			#print(f'Coords of all effective zeroes are {self.neighbors}')
			if len(self.neighbors) == 0:
				for i in range(self.row):
					for j in range(self.col):
						if self.board[i][j].val2 == self.board[i][j].val3: # if effective label of any tile is equal to uncovered neighbors
							n = self.__getneighbors(i+1,j+1)
							for neighbor in n: # for neighbor in neighbors of any tile that has effective label equal to uncovered neighbors
								if self.board[neighbor[0]-1][neighbor[1]-1].val1 == '*': # if the neighbor is covered it is a bomb
									self.board[neighbor[0]-1][neighbor[1]-1].val1 = 'B'
									self.__updateboardneighbors(neighbor[0],neighbor[1]) # so we update the labels of everyone around that bomb
									self.__updateEffectiveLabel(neighbor[0],neighbor[1])
									self.neighbors = self.__getCoordsofEffectiveZeroes() # after updating, we now get more effective zeroes
									#self.__printboard2()

			
			# probability check 
			self.bombs = []
			if len(self.neighbors) == 0:
				#print("Checking game board before probability")
				#self.__printboard2()
				maxi = self.__getProbability()
				if maxi == 999:     # This means that if there are no covered tiles left, we just leave)
					return Action(AI.Action.LEAVE)
				#self.__printboard2()
				self.board[maxi[0]][maxi[1]].val1 = 'B'
				self.__updateboardneighbors(maxi[0]+1,maxi[1]+1)
				self.__updateEffectiveLabel(maxi[0]+1,maxi[1]+1)
				#print("Checking game board after probability check")
				#self.__printboard2()
				self.neighbors = self.__getCoordsofEffectiveZeroes()
			if len(self.neighbors) == 0:
				#print("FINAL CHECK")
				finalcheck = self.__getCoveredTiles()
				if len(finalcheck) >= 1:
					self.neighbors.append(finalcheck.pop(0))

			if len(self.neighbors) == 0:
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
		valid_neighbors = [x for x in neighbors if x[0] > 0 and x[0] <= self.row and x[1] > 0 and x[1] <= self.col]
		return valid_neighbors

	def __getCoveredNeighbors(self, x: int, y: int) -> List:
		""" Return a list of all neighbors of the given co-ordinate"""
		neighbors = self.__getneighbors(x+1, y+1)
		covered_neighbors = [i for i in neighbors if self.board[i[0]-1][i[1]-1].val1 == '*']
		return covered_neighbors

	def __getUncoveredNeighbors(self, x: int, y: int) -> List: # Uncovered neighbor means no * or B (doesnt include bombs)
		""" Return a list of all neighbors of the given co-ordinate"""
		neighbors = self.__getneighbors(x+1, y+1)
		uncovered_neighbors = [i for i in neighbors if self.board[i[0]-1][i[1]-1].val1 != '*' and self.board[i[0]-1][i[1]-1].val1 != 'B']
		return uncovered_neighbors

	# This helper function initializes the board according to the model from Kask's discussion
	def __initializeboard(self) -> None: 
		self.board = [[i for i in range(self.row)] for j in range(self.col)]
		for i in range(self.col):
			for j in range(self.row):
				print(i,j)
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
	def __printboard(self) -> None: 
		counter = 0
		for i in range(self.row):
			print('     ' + str(i) + '   ', end="")
		print()
		for i in range(self.col):
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
	def __printboard2(self) -> None: 
		counter = 0
		subtract = -1
		for i in range(self.row):
			print('     ' + str(i) + '   ', end="")
		print()
		for i in range(self.col):
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
	def __updateboard(self, x: int, y: int, label: int) -> None: 
		self.board[x-1][y-1].val1 = int(label)
		num_bombs = 0
		neighbors = self.__getneighbors(x,y)
		for neighbor in neighbors:
			if self.board[neighbor[0]-1][neighbor[1]-1].val1 == 'B': # Possible optimize in the future
				num_bombs += 1
		
		self.board[x-1][y-1].val2 = int(label) - num_bombs

	def __updateboardneighbors(self, x: int, y: int) -> None:
		neighbors = self.__getneighbors(x,y)
		for neighbor in neighbors:
			self.board[neighbor[0]-1][neighbor[1]-1].val3 -= 1

	def __generateOnesList(self) -> None:
		ones = []
		for i in range(self.row):
			for j in range(self.col):	
				if (self.board[i][j].val1) == 1:
					ones.append((i+1,j+1))
		return ones
	
	def __updateEffectiveLabel(self, x: int, y: int) -> None:
		bombneighbors = self.__getneighbors(x,y)
		for neighbor in bombneighbors:
			if self.board[neighbor[0]-1][neighbor[1]-1].val1 == '*' or self.board[neighbor[0]-1][neighbor[1]-1].val1 == 'B': # if a bomb's neighbor is uncovered, set to 9
				self.board[neighbor[0]-1][neighbor[1]-1].val2 = 9
			else:
				self.board[neighbor[0]-1][neighbor[1]-1].val2 -= 1 # otherwise, decrement effective label of neighbor

	def __getCoordsofEffectiveZeroes(self) -> None:
		neighborss = []
		for i in range(self.row):
			for j in range(self.col):
				if (self.board[i][j].val1 != 'B' and self.board[i][j].val1 != '*' and self.board[i][j].val2 == 0):
					neighbors = self.__getCoveredNeighbors(i,j)
					#print(f'Tile of coordinate {(i+1,j+1)} has neighbors of {neighbors}')
					for neighbor in neighbors:
						if neighbor not in neighborss:
							neighborss.append(neighbor)
		return neighborss

	def __getProbability(self) -> tuple: # tuple coordinate is return in array coords
		neighborss = []
		maxi = [] 
		maxval = 0
		for i in range(self.row):
			for j in range(self.col):
				if (self.board[i][j].val1 == '*'): # if a tile is covered
					neighborss = self.__getUncoveredNeighbors(i,j) # get uncovered neighbors of that tile
					#print(f'Tile of coordinate {(i+1,j+1)} is covered and we\'re checking for probability')
					#print(f'Uncovered Neighbors: {neighborss}')
					for neighbor in neighborss: # for every neighbor in those neighbors
						self.board[i][j].val4 += self.board[neighbor[0]-1][neighbor[1]-1].val2/self.board[neighbor[0]-1][neighbor[1]-1].val3
					#print(f'Tile of coordinate ({i+1},{j+1}) has probability value = {self.board[i][j].val4}')
					if self.board[i][j].val4 > maxval:
						maxval = self.board[i][j].val4
						maxi.clear()
						maxi.append(i)
						maxi.append(j)

		if len(maxi) == 0: # if wall of bombs surround covered tiles,we must do random
			allCovered = self.__getCoveredTiles()
			if len(allCovered) == 0: # No covered tiles left
				return 999
			#print(f'Covered tiles are {allCovered} from probability')
			else:
				randomval = random.randint(0,len(allCovered)-1)
				maxi.append(allCovered[0][0]-1)
				maxi.append(allCovered[0][1]-1)
			
		return maxi

	def __getCoveredTiles(self): # returns covered tile coordinate in list of tuples which are actual game coordinate
		covered = []
		for i in range(self.row):
			for j in range(self.col):
				if self.board[i][j].val1 == '*': # if a tile is covered
					covered.append((i+1,j+1)) # May have to fix this if row and column dimensions different
		return covered


# An Optimization PROBLEM if we ever wanna optimize this in the future
# self.__geteffectiveZeroes
# The issue is that this function gets the coordinates of every tile in the board
# that has an effective label of 0 and is not uncovered or a bomb
# this means that it picks up on tiles that have been done for a very long time also
# fo these tiles it calls self.__getCoveredNeighbors but for most of these tiles, since they have been done
# for a very long time, the obviously dont have any covered neighbors for it goes through pointless iterations
# which could be making our code take longer
