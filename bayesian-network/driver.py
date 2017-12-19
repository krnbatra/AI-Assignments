# ID - 2014A7PS160P
# Name - Karan Deep Batra

from assign5 import *

filename = raw_input("Enter File name: ")
print("Option 1 : Markov Blanket")
print("Option 2 : GUI")
var = (int)(raw_input("Enter option number: "))

if var == 1:
	var2 = raw_input("Enter label for which you want to compute Markov Blanket: ")
	init()
	take_input(filename)
	fill_children()
	computeMarkovBlanket(var2)
else:
	init()
	take_input(filename)
	fill_children()
	gui()
	topological_sort()
	run()