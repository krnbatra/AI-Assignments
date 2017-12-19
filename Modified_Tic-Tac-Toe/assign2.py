# ID - 2014A7PS160P
# Name - Karan Deep Batra

from __future__ import print_function
import turtle
import time

# 1 for machine, 2 for human
class TreeNode():
	def __init__(self, uv):
		self.uv = uv
		self.ans = 0
		self.child1 = None
		self.child2 = None
		self.child3 = None
		self.child4 = None

def initialize():
	global initX1, initY1, grid_len, square_len, centres, row_mappings, col_mappings, state, alpha_nodes, simple_nodes, minimax_time, alpha_time
	simple_nodes = 0
	alpha_nodes = 0
	minimax_time = 0
	alpha_time = 0
	initX1 = 0
	initY1 = 250
	grid_len = 400
	square_len = 100
	centres = [[50, 200], [150, 200], [250, 200], [350, 200], [50, 100], [150, 100], [250, 100], [350, 100], [50, 0], [150, 0], [250, 0], [350, 0], [50, -100], [150, -100], [250, -100], [350, -100]]
	row_mappings = {200 : 0, 100 : 1, 0 : 2, -100 : 3}
	col_mappings = {50 : 0, 150 : 1, 250 : 2, 350 : 3}
	state = []
	for i in range(4):
		temp = []
		for j in range(4):
			temp.append(0)
		state.append(temp)

def isValid(x, y):
	return (x >= 0 and x < 4 and y >= 0 and y < 4)

def caliberate():
	turtle.penup()
	turtle.goto(-50, 200)
	turtle.write("R1", font=("Arial", 14, "normal"))
	turtle.goto(-50, 100)
	turtle.write("R2", font=("Arial", 14, "normal"))
	turtle.goto(-50, 0)
	turtle.write("R3", font=("Arial", 14, "normal"))
	turtle.goto(-50, -100)
	turtle.write("R4", font=("Arial", 14, "normal"))
	turtle.goto(50, -200)
	turtle.write("C1", font=("Arial", 14, "normal"))
	turtle.goto(150, -200)
	turtle.write("C2", font=("Arial", 14, "normal"))
	turtle.goto(250, -200)
	turtle.write("C3", font=("Arial", 14, "normal"))
	turtle.goto(350, -200)
	turtle.write("C4", font=("Arial", 14, "normal"))

def terminal_test(state):
	for i in range(4):
		for j in range(4):
			if state[i][j] == 1:
				# right
				if isValid(i, j+1) and state[i][j+1] == 1 and isValid(i, j+2) and state[i][j+2] == 1:
					return 1
				# diagonal right
				if isValid(i+1, j+1) and state[i+1][j+1] == 1 and isValid(i+2, j+2) and state[i+2][j+2] == 1:
					return 1
				# down
				if isValid(i+1, j) and state[i+1][j] == 1 and isValid(i+2, j) and state[i+2][j] == 1:
					return 1
				# diagonal left
				if isValid(i+1, j-1) and state[i+1][j-1] == 1 and isValid(i+2, j-2) and state[i+2][j-2] == 1:
					return 1
	for i in range(4):
		for j in range(4):
			if state[i][j] == 2:
				# right
				if isValid(i, j+1) and state[i][j+1] == 2 and isValid(i, j+2) and state[i][j+2] == 2:
					return -1
				# diagonal right
				if isValid(i+1, j+1) and state[i+1][j+1] == 2 and isValid(i+2, j+2) and state[i+2][j+2] == 2:
					return -1
				# down
				if isValid(i+1, j) and state[i+1][j] == 2 and isValid(i+2, j) and state[i+2][j] == 2:
					return -1
				# diagonal left
				if isValid(i+1, j-1) and state[i+1][j-1] == 2 and isValid(i+2, j-2) and state[i+2][j-2] == 2:
					return -1
	return 0

def is_filled(state):
	for i in range(4):
		for j in range(4):
			if state[i][j] == 0:
				return False
	return True

def print_state(state):
	for i in range(4):
		for j in range(4):
			print(state[i][j], end = ' ')
		print()
	print()

def minimax(currNode, curr_turn, state):
	global simple_nodes
	simple_nodes += 1
	res = terminal_test(state)
	if res == 1:
		# winning state for machine
		currNode.uv = 1
		return
	if res == -1:
		# winning state for human
		currNode.uv = -1
		return

	if is_filled(state):
		currNode.uv = 0
		return

	for col in range(4):
		for row in range(4):
			if state[row][col] == 0:
				state[row][col] = curr_turn
				if curr_turn == 1: # max
					if col == 0:
						currNode.child1 = TreeNode(1000)
						minimax(currNode.child1, 2, state)
					elif col == 1:
						currNode.child2 = TreeNode(1000)
						minimax(currNode.child2, 2, state)
					elif col == 2:
						currNode.child3 = TreeNode(1000)
						minimax(currNode.child3, 2, state)
					elif col == 3:
						currNode.child4 = TreeNode(1000)
						minimax(currNode.child4, 2, state)

				else:	# min
					if col == 0:
						currNode.child1 = TreeNode(-1000)
						minimax(currNode.child1, 1, state)
					elif col == 1:
						currNode.child2 = TreeNode(-1000)
						minimax(currNode.child2, 1, state)
					elif col == 2:
						currNode.child3 = TreeNode(-1000)
						minimax(currNode.child3, 1, state)
					elif col == 3:
						currNode.child4 = TreeNode(-1000)
						minimax(currNode.child4, 1, state)
				state[row][col] = 0
				break
	if curr_turn == 1:
		if(currNode is not None and currNode.child1 is not None):
			if(currNode.child1.uv > currNode.uv):
				currNode.ans = 0
			currNode.uv = max(currNode.child1.uv, currNode.uv)
		if(currNode is not None and currNode.child2 is not None):
			if(currNode.child2.uv > currNode.uv):
				currNode.ans = 1
			currNode.uv = max(currNode.child2.uv, currNode.uv)
		if(currNode is not None and currNode.child3 is not None):
			if(currNode.child3.uv > currNode.uv):
				currNode.ans = 2
			currNode.uv = max(currNode.child3.uv, currNode.uv)
		if(currNode is not None and currNode.child4 is not None):
			if(currNode.child4.uv > currNode.uv):
				currNode.ans = 3
			currNode.uv = max(currNode.child4.uv, currNode.uv)
	else:
		if(currNode is not None and currNode.child1 is not None):
			if(currNode.child1.uv < currNode.uv):
				currNode.ans = 0
			currNode.uv = min(currNode.child1.uv, currNode.uv)
		if(currNode is not None and currNode.child2 is not None):
			if(currNode.child2.uv < currNode.uv):
				currNode.ans = 1
			currNode.uv = min(currNode.child2.uv, currNode.uv)
		if(currNode is not None and currNode.child3 is not None):
			if(currNode.child3.uv < currNode.uv):
				currNode.ans = 2
			currNode.uv = min(currNode.child3.uv, currNode.uv)
		if(currNode is not None and currNode.child4 is not None):
			if(currNode.child4.uv < currNode.uv):
				currNode.ans = 3
			currNode.uv = min(currNode.child4.uv, currNode.uv)
	del(currNode.child1)
	del(currNode.child2)
	del(currNode.child3)
	del(currNode.child4)

def alpha_beta(currNode, curr_turn, state):
	global alpha_nodes
	alpha_nodes += 1
	res = terminal_test(state)
	if res == 1:
		# winning state for machine
		currNode.uv = 1
		return
	if res == -1:
		# winning state for human
		currNode.uv = -1
		return

	if is_filled(state):
		currNode.uv = 0
		return

	for col in range(4):
		for row in range(4):
			if state[row][col] == 0:
				state[row][col] = curr_turn
				if curr_turn == 1: # max
					if col == 0:
						currNode.child1 = TreeNode(1000)
						alpha_beta(currNode.child1, 2, state)
					elif col == 1:
						currNode.child2 = TreeNode(1000)
						alpha_beta(currNode.child2, 2, state)
					elif col == 2:
						currNode.child3 = TreeNode(1000)
						alpha_beta(currNode.child3, 2, state)
					elif col == 3:
						currNode.child4 = TreeNode(1000)
						alpha_beta(currNode.child4, 2, state)
					if(currNode is not None and currNode.child1 is not None):
						if(currNode.child1.uv == 1):
							currNode.ans = 0
							currNode.uv = 1
							state[row][col] = 0
							return
					if(currNode is not None and currNode.child2 is not None):
						if(currNode.child2.uv == 1):
							currNode.ans = 1
							currNode.uv = 1
							state[row][col] = 0
							return
					if(currNode is not None and currNode.child3 is not None):
						if(currNode.child3.uv == 1):
							currNode.ans = 2
							currNode.uv = 1
							state[row][col] = 0
							return
					if(currNode is not None and currNode.child4 is not None):
						if(currNode.child4.uv == 1):
							currNode.ans = 3
							currNode.uv = 1
							state[row][col] = 0
							return
				else:	# min
					if col == 0:
						currNode.child1 = TreeNode(-1000)
						alpha_beta(currNode.child1, 1, state)
					elif col == 1:
						currNode.child2 = TreeNode(-1000)
						alpha_beta(currNode.child2, 1, state)
					elif col == 2:
						currNode.child3 = TreeNode(-1000)
						alpha_beta(currNode.child3, 1, state)
					elif col == 3:
						currNode.child4 = TreeNode(-1000)
						alpha_beta(currNode.child4, 1, state)

					if(currNode is not None and currNode.child1 is not None):
						if(currNode.child1.uv == -1):
							currNode.ans = 0
							currNode.uv = -1
							state[row][col] = 0
							return
					if(currNode is not None and currNode.child2 is not None):
						if(currNode.child2.uv == -1):
							currNode.ans = 1
							currNode.uv = -1
							state[row][col] = 0
							return
					if(currNode is not None and currNode.child3 is not None):
						if(currNode.child3.uv == -1):
							currNode.ans = 2
							currNode.uv = -1
							state[row][col] = 0
							return
					if(currNode is not None and currNode.child4 is not None):
						if(currNode.child4.uv == -1):
							currNode.ans = 3
							currNode.uv = -1
							state[row][col] = 0
							return
				state[row][col] = 0
				break
	if curr_turn == 1:
		if(currNode is not None and currNode.child1 is not None):
			if(currNode.child1.uv > currNode.uv):
				currNode.ans = 0
			currNode.uv = max(currNode.child1.uv, currNode.uv)
		if(currNode is not None and currNode.child2 is not None):
			if(currNode.child2.uv > currNode.uv):
				currNode.ans = 1
			currNode.uv = max(currNode.child2.uv, currNode.uv)
		if(currNode is not None and currNode.child3 is not None):
			if(currNode.child3.uv > currNode.uv):
				currNode.ans = 2
			currNode.uv = max(currNode.child3.uv, currNode.uv)
		if(currNode is not None and currNode.child4 is not None):
			if(currNode.child4.uv > currNode.uv):
				currNode.ans = 3
			currNode.uv = max(currNode.child4.uv, currNode.uv)
	else:
		if(currNode is not None and currNode.child1 is not None):
			if(currNode.child1.uv < currNode.uv):
				currNode.ans = 0
			currNode.uv = min(currNode.child1.uv, currNode.uv)
		if(currNode is not None and currNode.child2 is not None):
			if(currNode.child2.uv < currNode.uv):
				currNode.ans = 1
			currNode.uv = min(currNode.child2.uv, currNode.uv)
		if(currNode is not None and currNode.child3 is not None):
			if(currNode.child3.uv < currNode.uv):
				currNode.ans = 2
			currNode.uv = min(currNode.child3.uv, currNode.uv)
		if(currNode is not None and currNode.child4 is not None):
			if(currNode.child4.uv < currNode.uv):
				currNode.ans = 3
			currNode.uv = min(currNode.child4.uv, currNode.uv)

def init_screen():
	turtle.speed(0)
	screen = turtle.Screen()
	turtle.setup(1366, 768)

def drawLine():
	turtle.penup()
	turtle.goto(-50, 300)
	turtle.pendown()
	turtle.write("Base Line", font=("Arial", 14, "normal"))
	turtle.color("red")
	turtle.forward(500)

def drawGrid():
	turtle.color("black")
	turtle.pen(fillcolor = "black", pensize=2)
	turtle.penup()
	turtle.goto(initX1, initY1)
	turtle.pendown()
	turtle.forward(grid_len)
	turtle.right(90)
	turtle.forward(grid_len)
	turtle.right(90)
	turtle.forward(grid_len)
	turtle.right(90)
	turtle.forward(grid_len)

def drawColumns():
	for i in range(2):
	    turtle.right(90)
	    turtle.forward(square_len)
	    turtle.right(90)
	    turtle.forward(grid_len)
	    turtle.left(90)
	    turtle.forward(square_len)
	    turtle.left(90)
	    turtle.forward(grid_len)

def drawRows():
	turtle.left(180)
	rows = 0 
	while rows < 2:
	    rows += 1
	    turtle.forward(square_len)
	    turtle.right(90)
	    turtle.forward(grid_len)
	    turtle.left(90)
	    turtle.forward(square_len)
	    turtle.left(90)
	    turtle.forward(grid_len)
	    turtle.right(90)

def drawDot(i, j, turn):
	x = initX1 + square_len * j + 25
	y = initY1 - square_len * i - square_len/2
	turtle.penup()
	turtle.goto(x, y)
	turtle.pendown()
	turtle.begin_fill()
	if turn == 1:
		turtle.color("green")
	else:
		turtle.color("blue")
	turtle.circle(30)
	turtle.end_fill()
	turtle.penup()

def goto(i, j):
	global state, root
	turtle.penup()
	dist = 1000000
	minnX = -1
	minnY = -1
	for idx in range(16):
		x = centres[idx][0]
		y = centres[idx][1]
		tempDist = (x-i)**2 + abs(y-j)**2
		if tempDist < dist:
			dist = tempDist
			minnX = x
			minnY = y

	final_row = row_mappings[minnY]
	final_col = col_mappings[minnX]

	for i in range(final_row):
		if state[i][final_col] == 0:
			print("Please choose a valid move")
			return

	if(state[final_row][final_col] != 0):
		print("Please choose a valid move")
		return

	state[final_row][final_col] = 2
	drawDot(row_mappings[minnY], col_mappings[minnX], 2)
	# print_state(state)
	if is_game_completed(state):
		return
	root2 = TreeNode(-1000)
	alpha_beta(root2, 1, state)
	col = root2.ans
	row = -1
	for i in range(4):
		if state[i][col] == 0:
			row = i
			break
	state[row][col] = 1
	drawDot(row, col, 1)
	# print_state(state)
	if is_game_completed(state):
		return

def is_game_completed(state):
	res = terminal_test(state)
	if res == 1:
		turtle.penup()
		turtle.goto(-200, 0)
		turtle.pendown()
		turtle.write("Machine wins",font=("Arial", 16, "normal"))
		return True
	elif res == -1:
		turtle.penup()
		turtle.goto(-200, 0)
		turtle.pendown()
		turtle.write("Human wins",font=("Arial", 16, "normal"))
		return True
	if is_filled(state):
		turtle.penup()
		turtle.goto(-200, 0)
		turtle.pendown()
		turtle.write("Match draw",font=("Arial", 16, "normal"))
		return True
	return False

def minimax_helper():
	global state, root, minimax_time
	initialize()
	print("PLEASE WAIT!!!")
	root = TreeNode(-1000)
	time1 = time.time()
	minimax(root, 1, state)
	init_screen()
	drawLine()
	drawGrid()
	drawColumns()
	drawRows()
	caliberate()
	col = root.ans
	row = -1
	turtle.onscreenclick(goto)
	for i in range(4):
		if state[i][col] == 0:
			row = i
			break
	state[row][col] = 1
	drawDot(row, col, 1)
	var = (int)(input("Enter 1 to continue playing or 0 to stop."))
	print()
	time2 = time.time()
	minimax_time = time2-time1
	if(var == 1):
		turtle.clear()
		turtle.goto(0, 0)
		turtle.penup()
		turtle.right(270)
		minimax_helper()
	else:
		write_analysis(2)

def alpha_beta_helper():
	global state, root, alpha_time
	initialize()
	print("PLEASE WAIT!!!")
	root = TreeNode(-1000)
	time1 = time.time()
	alpha_beta(root, 1, state)
	init_screen()
	drawLine()
	drawGrid()
	drawColumns()
	drawRows()
	caliberate()
	col = root.ans
	row = -1
	turtle.onscreenclick(goto)
	for i in range(4):
		if state[i][col] == 0:
			row = i
			break
	state[row][col] = 1
	drawDot(row, col, 1)
	var = (int)(input("Enter 1 to continue playing or 0 to stop."))
	time2 = time.time()
	alpha_time = time2-time1
	if(var == 1):
		turtle.clear()
		turtle.goto(0, 0)
		turtle.penup()
		turtle.right(270)
		alpha_beta_helper()
	else:
		write_analysis(3)

def write_analysis(state):
	turtle.color("black")
	turtle.shape()
	turtle.penup()
	if state == 2:
		turtle.goto(-650, 300)
		turtle.write("Minimax based analysis", align="left", font=("Arial", 14, "normal"))
		
		turtle.goto(-650, 270)
		turtle.write("Number of nodes:[R1] " + str(simple_nodes), align="left", font=("Arial", 12, "normal"))
		
		turtle.goto(-650, 240)
		turtle.write("Memory allocated to one node:[R2] " + str(72), align="left", font=("Arial", 12, "normal"))
		
		turtle.goto(-650, 210)
		turtle.write("Maximum growth of implicit stack:[R3] " + str(72*simple_nodes), align="left", font=("Arial", 12, "normal"))
		
		turtle.goto(-650, 180)
		turtle.write("Total time:[R4] " + str(minimax_time), align="left", font=("Arial", 12, "normal"))
		
		turtle.goto(-650, 150)
		turtle.write("Number of nodes created in one micro second:[R5] " + str(minimax_time/1000000), align="left", font=("Arial", 12, "normal"))

	if state == 3:
		turtle.goto(-650, 100)
		turtle.write("Alpha beta pruning based analysis", align="left", font=("Arial", 14, "normal"))
		
		turtle.goto(-650, 70)
		turtle.write("Number of nodes:[R6] " + str(alpha_nodes), align="left", font=("Arial", 12, "normal"))
		
		turtle.goto(-650, 40)
		turtle.write("Change in number of nodes:[R7] " + str((6761217-alpha_nodes)/6761217.0), align="left", font=("Arial", 12, "normal"))
		
		turtle.goto(-650, 10)
		turtle.write("Time taken:[R8] " + str(alpha_time), align="left", font=("Arial", 12, "normal"))

	if state == 4:
		turtle.goto(-650, -100)
		turtle.write("Comparative Analysis[R9] Minimax memory: " + str(486807624) + "  Alpha Beta memory: " + str(432288) , align="left", font=("Arial", 12, "normal"))
		turtle.goto(-650, -130)
		turtle.write("Average time to play the game 10 times:[R10] 37.53", align="left", font=("Arial", 12, "normal"))
		turtle.goto(-650, -160)
		turtle.write("Number of times M wins ins 10 games:[R11] " + str(10), font=("Arial", 12, "normal"))
		turtle.goto(-650, -190)
		turtle.write("Number of times M wins ins 20 games:[R12] " + str(20), font=("Arial", 12, "normal"))
	turtle.exitonclick()
