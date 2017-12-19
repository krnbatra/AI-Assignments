# ID - 2014A7PS160P
# Name - Karan Deep Batra

from assign2 import *
import turtle

print("Option 1 : Display the empty board")
print("Option 2 : Play the game using Minimax algorithm")
print("Option 3 : Play the game using Alpha Beta pruning")
print("Option 4 : Show all results R1-R12")
var = (int)(input("Enter option number\n"))

if var == 1:
	initialize()
	init_screen()
	drawGrid()
	drawColumns()
	drawRows()
	turtle.exitonclick()

if var == 2:
	minimax_helper()

if var == 3:
	alpha_beta_helper()

if var == 4:
	init_screen()
	write_analysis(4)