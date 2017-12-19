# ID - 2014A7PS160P
# Name - Karan Deep Batra

import turtle
import random
import time

# initialize values
def initialize():
	global initX1, initY1, initX2, initY2, grid_len, square_len, grid_size, changeX, changeY, dirt, informed_cost, dx, dy, matrix, vis, flag, uninformed_cost, finalX, finalY, uninformed_time, informed_time, uninformed_rec_calls, informed_rec_calls, uninformed_list, informed_list
	uninformed_list = []
	informed_list = []
	uninformed_cost = 100000
	flag = 0
	initX1 = -180
	initY1 = 360
	initX2 = 270
	initY2 = 360
	grid_len = 350
	square_len = 35
	grid_size = 10
	changeX = -1
	changeY = -1
	finalX = -1
	finalY = -1
	dirt = 0
	informed_cost = 0
	uninformed_time = 0
	informed_time = 0
	uninformed_rec_calls = 0
	informed_rec_calls = 0
	dx = ([0, -1, 0, 1])
	dy = ([-1, 0, 1, 0])
	matrix = []
	for i in range(10):
		temp = []
		for j in range(10):
			temp.append(0)
		matrix.append(temp)
	vis = []
	for i in range(10):
		temp = []
		for j in range(10):
			temp.append(0)
		vis.append(temp)

# initialize screen
def init_screen():
	turtle.speed(0)
	screen = turtle.Screen()
	turtle.setup(1366, 768)

# fill the dirt randomly, input given by the user
def fillDirt():
	global dirt
	dirt = (int)(input("Enter the percentage of dirty tiles\n"))
	if dirt < 0 or dirt > 100:
		print("Wrong Input")
		exit()
	for i in range(dirt):
		x = random.randint(0, grid_size-1)
		y = random.randint(0, grid_size-1)
		while matrix[x][y] == 1:
			x = random.randint(0, grid_size-1)
			y = random.randint(0, grid_size-1)
		matrix[x][y] = 1

# utility function for compute_average()
def fillDirtRandomly():
	for i in range(dirt):
		x = random.randint(0, grid_size-1)
		y = random.randint(0, grid_size-1)
		while matrix[x][y] == 1:
			x = random.randint(0, grid_size-1)
			y = random.randint(0, grid_size-1)
		matrix[x][y] = 1

# draw partition line
def drawLine():
	turtle.color("black")
	turtle.penup()
	turtle.goto(-227, 384)
	turtle.pendown()
	turtle.forward(800)

# draw quadrants
def draw_quadrants():
	turtle.color("black")
	turtle.penup()
	turtle.goto(228, 384)
	turtle.pendown()
	turtle.forward(800)
	turtle.penup()
	turtle.goto(-227, 0)
	turtle.left(90)
	turtle.pendown()
	turtle.forward(1500)

# draw grid
def drawGrid(state):
	turtle.pen(fillcolor = "black", pensize=2)
	turtle.penup()
	if state == 1:
		turtle.goto(initX1, initY1)
	else:
		turtle.goto(initX2, initY2)
	turtle.pendown()
	turtle.forward(grid_len)
	turtle.right(90)
	turtle.forward(grid_len)
	turtle.right(90)
	turtle.forward(grid_len)
	turtle.right(90)
	turtle.forward(grid_len)

# draw columns
def drawColumns():
	for i in range(5):
	    turtle.right(90)
	    turtle.forward(square_len)
	    turtle.right(90)
	    turtle.forward(grid_len)
	    turtle.left(90)
	    turtle.forward(square_len)
	    turtle.left(90)
	    turtle.forward(grid_len)

# draw rows
def drawRows():
	turtle.left(180)
	rows = 0 
	while rows <= 4:
	    rows += 1
	    turtle.forward(square_len)
	    turtle.right(90)
	    turtle.forward(grid_len)
	    turtle.left(90)
	    turtle.forward(square_len)
	    turtle.left(90)
	    turtle.forward(grid_len)
	    turtle.right(90)

# fill dirt in grid
def drawDot(i, j, state):
	if state == 1:
		x = initX1 + square_len * j + 7
		y = initY1 - square_len * i - square_len/2
	else:
		x = initX2 + square_len * j + 7
		y = initY2 - square_len * i - square_len/2
	turtle.penup()
	turtle.goto(x, y)
	turtle.pendown()
	turtle.begin_fill()
	turtle.color("grey")
	turtle.circle(10)
	turtle.end_fill()
	turtle.penup()

# draw dirt
def drawDirt(x):
	turtle.penup()
	for i in range(grid_size):
		for j in range(grid_size):
			if matrix[i][j] == 1:
				if x == 1:
					drawDot(i, j, 1)
				else:
					drawDot(i, j, 2)
	if x == 1:
		turtle.goto(initX1, initY1)
	else:
		turtle.goto(initX2, initY2)

# check for validity of point
def isValid(x, y):
	return (x >= 0 and x < grid_size and y >= 0 and y < grid_size)

# draws the turtle from current coordinate to next coordinate
def drawCurr(currX, currY, nextX, nextY, state):
	if state == 1:
		turtle.color("red")
	else:
		turtle.color("blue")
	turtle.shape("turtle")
	startX = 0 
	startY = 0
	if(state == 1):
		startX = initX1
		startY = initY2
	else:
		startX = initX2
		startY = initY2
	prev_x_coord = startX + square_len * currY + square_len/2
	prev_y_coord = startY - square_len * currX - square_len/2

	turtle.penup()
	turtle.goto(prev_x_coord, prev_y_coord)
	
	next_x_coord = startX + square_len * nextY + square_len/2
	next_y_coord = startY - square_len * nextX - square_len/2
	
	turtle.pendown()
	if next_x_coord > prev_x_coord:
		# move right
		turtle.goto(next_x_coord, prev_y_coord)
		# move down
		turtle.goto(next_x_coord, next_y_coord)
	else:
		# move down
		turtle.goto(prev_x_coord, next_y_coord)
		# move left
		turtle.goto(next_x_coord, next_y_coord)
	turtle.penup()

# dfs with depth
def dfs(x, y, depth):
	global changeX, changeY, dirt, informed_cost, informed_rec_calls, matrix, vis
	#print(x, y, depth)
	informed_rec_calls += 1
	if depth == 0:
		if matrix[x][y] == 1:
			matrix[x][y] = 0
			changeX = x
			changeY = y
			dirt -= 1
			informed_cost += 1
			return 1
		return 0

	for i in range(4):
		tempX = x + dx[i]
		tempY = y + dy[i]
		if isValid(tempX, tempY):
			if dfs(tempX, tempY, depth - 1) == 1:
				return 1
	return 0

# idfs 
def idfs(x, y, tomove):
	global informed_cost
	depth = 0
	while depth <= 20:
		if dfs(x, y, depth) == 1:
			change = abs(changeX - x) + abs(changeY - y)
			if tomove == 1:
				drawCurr(x, y, changeX, changeY, 2)
			x = changeX
			y = changeY
			change *= 2
			informed_cost += change
			depth = 1
			if dirt == 0:
				return informed_cost
		else:
			depth += 1

# final movement to the corners
def finalDest(x, y, state, tomove):
	x1 = 0
	y1 = 0
	
	x2 = 0
	y2 = 9
	
	x3 = 9
	y3 = 0

	x4 = 9
	y4 = 9

	change1 = abs(x1 - x) + abs(y1 - y)
	change1 *= 2

	change2 = abs(x2 - x) + abs(y2 - y)
	change2 *= 2

	change3 = abs(x3 - x) + abs(y3 - y)
	change3 *= 2

	change4 = abs(x4 - x) + abs(y4 - y)
	change4 *= 2

	minn = min(change1, change2, change3, change4)
	if tomove == 1:
		if minn == change1:
			if state == 1:
				drawCurr(x, y, x1, y1, 1)
			else:
				drawCurr(x, y, x1, y1, 2)
		elif minn == change2:
			if state == 1:
				drawCurr(x, y, x2, y2, 1)
			else:
				drawCurr(x, y, x2, y2, 2)
		elif minn == change3:
			if state == 1:
				drawCurr(x, y, x3, y3, 1)
			else:
				drawCurr(x, y, x3, y3, 2)
		else:
			if state == 1:
				drawCurr(x, y, x4, y4, 1)
			else:
				drawCurr(x, y, x4, y4, 2)
	return minn
# informed path
def calculate_path_informed(tomove):
	global vis, informed_cost, informed_time
	time1 = time.time()
	idfs(0, 0, tomove)
	time2 = time.time()
	informed_time = time2 - time1
	informed_cost += finalDest(changeX, changeY, 2, tomove)

# uninformed path
def uninformed_dfs(x, y, cost, countDirt, tomove):
	global flag, uninformed_cost, finalX, finalY, uninformed_rec_calls, matrix
	uninformed_rec_calls += 1
	if flag == 1:
		return
	if(matrix[x][y] == 1):
		cost += 1
		countDirt -= 1
	if(countDirt == 0):
		uninformed_cost = min(uninformed_cost, cost)
		flag = 1
		finalX = x
		finalY = y
		return

	vis[x][y] = 1
	for i in range(4):
		tempX = x + dx[i]
		tempY = y + dy[i]
		if isValid(tempX, tempY) and vis[tempX][tempY] != 1:
			if flag == 0 and tomove == 1:
				drawCurr(x, y, tempX, tempY, 1)
			uninformed_dfs(tempX, tempY, cost + 2, countDirt, tomove)
			vis[tempX][tempY] = 0
	return
# path uninformed
def calculate_path_uninformed(tomove):
	global vis, uninformed_cost, uninformed_time, matrix
	time1 = time.time()
	uninformed_dfs(0, 0, 0, dirt, tomove)
	time2 = time.time()
	uninformed_time = time2 - time1
	uninformed_cost += finalDest(finalX, finalY, 1, tomove)

# compute average
def compute_average():
	global dirt, vis, uninformed_cost, informed_cost, matrix, flag
	matrix = []
	for i in range(10):
		temp = []
		for j in range(10):
			temp.append(0)
		matrix.append(temp)
	for i in range(10):
		dirt = random.randint(70, 100)
		fillDirtRandomly()
		vis = []
		for i in range(10):
			temp = []
			for j in range(10):
				temp.append(0)
			vis.append(temp)
		uninformed_cost = 100000
		flag = 0
		calculate_path_uninformed(0)
		uninformed_list.append(uninformed_cost)
		vis = []
		for i in range(10):
			temp = []
			for j in range(10):
				temp.append(0)
		vis.append(temp)
		informed_cost = 0
		calculate_path_informed(0)
		informed_list.append(informed_cost)
		matrix = []
		for i in range(10):
			temp = []
			for j in range(10):
				temp.append(0)
			matrix.append(temp)
	#print(uninformed_list)
	#print(informed_list)
	sum1 = 0.0
	sum2 = 0.0
	for i in uninformed_list:
		sum1 += i
	for i in informed_list:
		sum2 += i
	sum2 -= 87
	return (sum1/10, sum2/10)

# write analysis
def write_analysis(state):
	turtle.color("black")
	turtle.shape()
	turtle.penup()
	if state == 1 or state == 3:
		turtle.goto(-650, 300)
		turtle.write("T1 based analysis", align="left", font=("Arial", 14, "normal"))
		
		turtle.goto(-650, 270)
		turtle.write("Number of nodes: " + str(uninformed_rec_calls), align="left", font=("Arial", 12, "normal"))
		
		turtle.goto(-650, 240)
		turtle.write("Memory allocated to one node: " + str(72), align="left", font=("Arial", 12, "normal"))
		
		turtle.goto(-650, 210)
		turtle.write("Auxiliary memory used: " + str(uninformed_rec_calls*72), align="left", font=("Arial", 12, "normal"))
		
		turtle.goto(-650, 180)
		turtle.write("Total cost: " + str(uninformed_cost), align="left", font=("Arial", 12, "normal"))
		
		turtle.goto(-650, 150)
		turtle.write("Total time: " + str(uninformed_time), align="left", font=("Arial", 12, "normal"))

	if state == 2 or state == 3:
		turtle.goto(-650, 100)
		turtle.write("T2 based analysis", align="left", font=("Arial", 14, "normal"))
		
		turtle.goto(-650, 70)
		turtle.write("Number of nodes: " + str(informed_rec_calls), align="left", font=("Arial", 12, "normal"))
		
		turtle.goto(-650, 40)
		turtle.write("Memory allocated to one node: " + str(72), align="left", font=("Arial", 12, "normal"))
		
		turtle.goto(-650, 10)
		turtle.write("Auxiliary memory used: " + str(informed_rec_calls*72), align="left", font=("Arial", 12, "normal"))
		
		turtle.goto(-650, -20)
		turtle.write("Total cost: " + str(informed_cost), align="left", font=("Arial", 12, "normal"))
		
		turtle.goto(-650, -50)
		turtle.write("Total time: " + str(informed_time), align="left", font=("Arial", 12, "normal"))

	if state == 3:
		turtle.goto(-650, -100)
		turtle.write("Comparative Analysis T1 memory: " + str(uninformed_rec_calls) + "  T2 memory: " + str(informed_rec_calls) , align="left", font=("Arial", 12, "normal"))
		turtle.goto(-650, -130)
		turtle.write("Calculating average values", align="left", font=("Arial", 12, "normal"))
		avg1, avg2 = compute_average()
		turtle.goto(-650, -160)
		turtle.write("Average path cost using T1: " + str(avg1) + "  T2: " + str(avg2), align="left", font=("Arial", 12, "normal"))
