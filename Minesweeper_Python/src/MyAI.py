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
import random # new

# This is the final copy of Draft AI with debugging comments

class Tile: # NEW
    def __init__(self):
        self.val1 = '*' # Covered/Marked or covered/Unmarked or Label
        self.val2 = 0 # Effective Label
        self.val3 = 8   # Number of neighbors that are covered or unmarked
        self.val4 = 0   # Probability field

class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
		self.zeroes = []
		self.f = False   # Set to False to remove all comments
		self.total = 0
		self.ones = []
		self.bombs = []
		self.done = []
		self.row = rowDimension
		self.col = colDimension
		self.x_coord = startX
		self.y_coord = startY
		self.current = (startX+1, startY+1)
		self.flag = True
		self.zeroes.append(self.current)
		#print(f'self.row is {self.row}')
		#print(f'self.col = {self.col}')
		
		# Changes I made are below
		self.__initializeboard() # NEW
		self.timestoUncover = (rowDimension * colDimension)
		self.__updateboardneighbors(self.current[0], self.current[1])
		self.neighbors = self.__getCoveredNeighbors(self.current[0]-1, self.current[1]-1)
		#self.__printboard2()


	def getAction(self, number: int) -> "Action Object":
		if self.f:
			print(f'Current val:{self.current[0], self.current[1]} Current Value: {number}')
		if (self.board[self.current[0]-1][self.current[1]-1].val1 == '*'):
			if self.f:
				print(f'Updating Neighbors of: {(self.current[0], self.current[1])}')
			self.__updateboardneighbors(self.current[0], self.current[1])
			self.__updateboard(self.current[0], self.current[1], number) # NEW
		if self.f:
			print(f'Current Neighbors: {self.neighbors}')

		if self.f:
			self.__printboard2() 
		
		#self.__printboard() # NEW Uncomment to use (Only if running in debug mode)
		while self.flag: 
			self.total = 0
			for i in range(self.col):	
				for j in range(self.row):
					if self.board[i][j].val1 != '*':
						self.total += 1
			if self.total == self.timestoUncover: # new unhardcoded exit condition
				if self.f:
					print(f'Total: {self.total}')
					print(f'To Uncover: {self.timestoUncover}')
				return Action(AI.Action.LEAVE)

			# Uncovers anyone in self.neighbors
			if len(self.neighbors) >= 1:
				if self.f:
					print(f'Inside while loop')
				self.current = self.neighbors.pop(0)
				x = self.current[0] - 1
				y = self.current[1] - 1
				action = AI.Action.UNCOVER
				if self.f:
					print(f'About to uncover: {x+1}, {y+1}')
				self.done.append(self.current)
				return Action(action, x, y)

			# If self.neighbors is empty we must use algorithms to add more to uncover
			# Below clears every 0
			else:
				for i in range(self.col):	
					for j in range(self.row):
						if self.board[i][j].val1 == 0 and self.board[i][j].val3 > 0:
							if self.f:
								print(f'FOUND A NEW ZERO!! Position : ({i+1}, {j+1})')
							action = AI.Action.UNCOVER
							self.neighbors = self.__getCoveredNeighbors(i, j)
							if len(self.neighbors) >= 1:
								new = self.neighbors.pop(0)
							if self.f:
								print(f'About to uncover: {new[0]}, {new[1]}')
								print(f'Covered Neighbors for new Zero found: {self.neighbors}')
							self.current = new
							return Action(action, new[0]-1, new[1]-1)

				# Below clears marks bombs around ones and updates
				if self.f:
					print('ZEROES DONE')
				self.ones = self.__generateOnesList()
				if self.f:
					print(f'Ones List after zeroes are done: {self.ones}')

				for one in self.ones:
					#if self.f:
						#print(f'Coordinate of {one} has {self.board[one[0]-1][one[1]-1].val1}:{self.board[one[0]-1][one[1]-1].val2}:{self.board[one[0]-1][one[1]-1].val3}')

					if int(self.board[one[0]-1][one[1]-1].val1) == int(self.board[one[0]-1][one[1]-1].val3):
						if self.f:
							print(f'These triggered if statement: {one}')
							self.__printboard2()
						neighbors = self.__getneighbors(one[0],one[1]) # Neighbors of all tiles where num of label is equal to uncovered tiles
						#print(f'Tile Coordinate is {one}, and neighbors is {neighbors}')
						#print(f'CHECKING')
						for neighbor in neighbors: # for each neighbor in those neighbors
							if self.board[neighbor[0]-1][neighbor[1]-1].val1 == '*' and self.board[neighbor[0]-1][neighbor[1]-1].val2 != 9: # if the neighbor is covered
								if self.f:
									print(f'Bomb Coordinate is {(neighbor[0],neighbor[1])}')
								self.board[neighbor[0]-1][neighbor[1]-1].val1 = 'B' # mark it as a bomb
								self.__updateboardneighbors(neighbor[0],neighbor[1])
								self.__updateEffectiveLabel(neighbor[0],neighbor[1])
				
				if self.f:
					print('Gonna print board statement now')
					self.__printboard2()

			# now that bombs around ones are marked, we want to uncover all tles with effective label 0	
			self.neighbors = self.__getCoordsofEffectiveZeroes()
			#print(f'Coords of all effective zeroes are {self.neighbors}')
			if len(self.neighbors) == 0:
				if self.f:
					print('Finding effective zero candidates')
				for i in range(self.col):
					for j in range(self.row):
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
				if maxi == 999: # This is new (means that if there are no covered tiles left, we just leave)
					return Action(AI.Action.LEAVE)
				if self.f:
					print(f'Max position: {maxi}') # Issue in probability part
					print(f'Max Probability: {self.board[maxi[0]][maxi[1]].val4}') # maxi empty
				#self.__printboard2()
				self.board[maxi[0]][maxi[1]].val1 = 'B'
				self.__updateboardneighbors(maxi[0]+1,maxi[1]+1)
				self.__updateEffectiveLabel(maxi[0]+1,maxi[1]+1)
				#print("Checking game board after probability check")
				#self.__printboard2()
				self.neighbors = self.__getCoordsofEffectiveZeroes()
				if self.f:
					print(f'New Positions to uncover: {self.neighbors}')
			if len(self.neighbors) == 0:
				#print("FINAL CHECK")
				finalcheck = self.__getCoveredTiles()
				if len(finalcheck) >= 1:
					self.neighbors.append(finalcheck.pop(0))

			if len(self.neighbors) == 0:

				#if self.f:
					#print(f'Now in final self.neighbors before exit')
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
		valid_neighbors = [x for x in neighbors if x[0] > 0 and x[0] <= self.col and x[1] > 0 and x[1] <= self.row]
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
	def __initializeboard(self) -> None: # NEW
		self.board = [[i for i in range(self.row)] for j in range(self.col)]
		for i in range(self.col):
			for j in range(self.row):
				tile = Tile()
				self.board[i][j] = tile
				#if self.f:
					#print(f'Board cordinates: I:{i}, J {j}')
		self.board[self.x_coord][self.y_coord].val1 = 0 # You can assume first label always 0

		for i in range(self.row): 
			if self.f:
				print(f'Board cordinates: I:{i}')
			self.board[0][i].val3 = 5
			self.board[-1][i].val3 = 5
		for i in range(self.col):
			if self.f:
				print(f'Board cordinates: I:{i}')
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
		counter = 1
		for i in range(self.row):
			print('     ' + str(i) + '   ', end="  ")
		print()
		for i in range(self.row):
			print('   ' + '-----' + ' ', end="  ")
		print()
		flag = True
		for i in range(self.col):
			for j in range(self.row):
				if flag == True:
					print(str(i) + '|', end="   ")
					flag = False
				print(str(self.board[i][j].val1) + ':' + str(self.board[i][j].val2) + ':' + str(self.board[i][j].val3) + '   ', end="   ")
			flag = True
			counter+= 1
			print()
	
	# This helper function prints out how the model looks on the actual board
	# It basically flips the board from __printboard sideways so you can see how it actually looks
	# Indices are inaccurate in this case so ignore those because the board was flipped sideways
	def __printboard2(self) -> None:
		counter = self.row
		subtract = -1
		for i in range(1, self.col + 1):
			if i == 1:
				print('        ' + str(i) + '  ', end="  ")
			elif i >1 and i <= 10:
				print('    ' + str(i) + '  ', end="  ")
			else:
				print('   ' + str(i) + '  ', end="  ")
		print()
		"""
		for i in range(self.row + 1):
			if i == 1:
				print('-----' + '  ', end=" ")
			elif i >1 and i <= 10:
				print(' ' + '-----' + '  ', end=" ")
			else:
				print(' ' + '-----' + '  ', end=" ")
		print()
		"""
		flag = True
		for i in range(self.row): # 0 - 15
			for j in range(self.col): # 0 - 29
				if flag == True:
					if counter < 10:
						print('0' + str(counter) + '|', end="   ")
					else:
						print(str(counter) + '|', end="   ")
					flag = False
				print(str(self.board[j][subtract].val1) + ':' + 
				      str(self.board[j][subtract].val2) + ':' + 
					  str(self.board[j][subtract].val3) + '  ', end="  ")
			flag = True
			counter -= 1
			subtract -= 1
			print()
		for i in range(1, self.col + 1):
			if i == 1:
				print('        ' + str(i) + '  ', end="  ")
			elif i >1 and i <= 10:
				print('    ' + str(i) + '  ', end="  ")
			else:
				print('   ' + str(i) + '  ', end="  ")
		print()

	# Updates our board's labels as we uncover
	# Does not have functionality for changing anything but the label only so far
	# Coordinate of current tile to uncover must be subtracted by 1 before accessing the board
	def __updateboard(self, x: int, y: int, label: int) -> None: # NEW
		self.board[x-1][y-1].val1 = int(label)
		#if self.f:
			#print(f'Printing updated val1 for {x,y}: {self.board[x-1][y-1].val1}')
		num_bombs = 0
		neighbors = self.__getneighbors(x,y)
		for neighbor in neighbors:
			if self.board[neighbor[0]-1][neighbor[1]-1].val1 == 'B': # Possible optimize in the future
				num_bombs += 1
		
		self.board[x-1][y-1].val2 = int(label) - num_bombs

	def __updateboardneighbors(self, x: int, y: int) -> None:
		neighbors = self.__getneighbors(x,y)
		#print(neighbors)
		for neighbor in neighbors:
			self.board[neighbor[0]-1][neighbor[1]-1].val3 -= 1

	def __generateOnesList(self) -> None:
		ones = []
		for i in range(self.col):
			for j in range(self.row):	
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
		for i in range(self.col):
			for j in range(self.row):
				if (self.board[i][j].val1 != 'B' and self.board[i][j].val1 != '*' and self.board[i][j].val2 == 0 and self.board[i][j].val3 != 0):
					neighbors = self.__getCoveredNeighbors(i,j)
					for neighbor in neighbors:
						if neighbor not in neighborss:
							neighborss.append(neighbor)
		return neighborss

# Calculate the probability of a position having a bomb.
	def __getProbability(self) -> tuple: # tuple coordinate is return in array coords
		neighborss = []
		maxi = [] 
		maxval = 0
		for i in range(self.col):
			for j in range(self.row):
				if (self.board[i][j].val1 == '*'): # if a tile is covered
					neighborss = self.__getUncoveredNeighbors(i,j) # get uncovered neighbors of that tile
					if not neighborss:
						continue
					for neighbor in neighborss: # for every neighbor in those neighbors
						self.board[i][j].val4 += self.board[neighbor[0]-1][neighbor[1]-1].val2/self.board[neighbor[0]-1][neighbor[1]-1].val3
					if self.f:
						print(f'Tile of coordinate ({i+1},{j+1}) has probability value = {self.board[i][j].val4}')
					if self.board[i][j].val4 > maxval:
						maxval = self.board[i][j].val4
						maxi.clear()
						maxi.append(i)
						maxi.append(j)
		#print(f'Max Value: {maxval}')
		#print(f'Max Co-ords: {maxi}')

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

	def __getCoveredTiles(self): # returns covered tile coordinate in list of tuples whcih are actual game coordinate
		covered = []
		for i in range(self.col):
			for j in range(self.row):
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
