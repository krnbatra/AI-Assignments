# ID - 2014A7PS160P
# Name - Karan Deep Batra

import Tkinter
from collections import deque

# initalize all variables
def init():
	global nodes_list, query_variables, conditional_variables, topo_sort, buttons_dict, index, number_buttons, labels_dict, root
	nodes_list = []
	query_variables = {}
	conditional_variables = {}
	topo_sort = []
	buttons_dict = {}
	index = 0
	number_buttons = 0
	labels_dict = {}

# onclick
def action(index):
	quo = index//4
	num1 = 4*quo
	num2 = num1+1
	num3 = num2+1
	num4 = num3+1
	buttons_dict[num1]["bg"] = "green"
	buttons_dict[num2]["bg"] = "green"
	buttons_dict[num3]["bg"] = "green"
	buttons_dict[num4]["bg"] = "green"
	buttons_dict[index]["bg"] = "orange"

# node structure
class node():
	def __init__(self, label):
		self.label = label
		self.parents = []
		self.children = []
		self.cpt = []
		self.in_degree = 0

# topologcial sort for ordering of nodes
def topological_sort():
	num_nodes = len(nodes_list)
	for node in nodes_list:
		node.in_degree = len(node.parents)
	Q = deque()
	for node in nodes_list:
		if(len(node.parents) == 0):
			Q.appendleft(node)

	while(Q):
		u = Q.pop()
		# print(u.label)
		topo_sort.append(u)
		for node in nodes_list:
			for parent in node.parents:
				# print("NODE " + node.label + " PARENT " + parent)
				if(parent == u.label):
					node.in_degree -= 1
					if(node.in_degree == 0):
						# print(node.label)
						Q.appendleft(node)

# parse input string
def parse_line(str):
	global nodes_list
	label = ""
	i = 0
	# fill label
	while i < len(str):
		if(str[i] == ' '):
			i += 1
			continue
		if(str[i] == '>'):
			break
		label += str[i]
		i += 1
	
	new_node = node(label)
	
	# fill parents
	while i < len(str):
		if(str[i] == '['):
			break
		i += 1
	
	i += 1
	parent_str = ""
	while i < len(str):
		if(str[i] == ',' or str[i] == ' '):
			if(parent_str != ""):
				new_node.parents.append(parent_str)
			parent_str = ""
		elif(str[i] == ']'):
			if(parent_str != ""):
				new_node.parents.append(parent_str)
			parent_str = ""
			break
		else:
			parent_str += str[i]
		i += 1
	# print(new_node.label, new_node.parents)

	while i < len(str):
		if(str[i] == '>' and str[i-1] == '>'):
			break
		i += 1
	# fill cpt
	i += 1
	rem = ""
	while i < len(str):
		rem += str[i]
		i += 1
	probabilities = rem.split()
	for i in probabilities:
		new_node.cpt.append(i)
	# print(new_node.cpt)
	nodes_list.append(new_node)

# read input
def take_input(filename):
	f = open(filename, "r")
	s = f.readline()
	while(1):
		if(s == "" or s[0] == "$"):
			break
		parse_line(s)
		s = f.readline()

# populate children
def fill_children():
	for node in nodes_list:
		curr_label = node.label
		for parent_label in node.parents:
			for parent in nodes_list:
				if parent.label == parent_label:
					parent.children.append(curr_label)
					break

# markov blanket calculation
def computeMarkovBlanket(node_label):
	markov_blanket = {}
	for node in nodes_list:
		if(node.label == node_label):
			markov_blanket[node.label] = 1
			for parent in node.parents:
				markov_blanket[parent] = 1
			for child in node.children:
				markov_blanket[child] = 1
				for new_node in nodes_list:
					if new_node.label == child:
						for child_parent in new_node.parents:
							markov_blanket[child_parent] = 1
	for i in markov_blanket:
		print(i)
	# return markov_blanket

# probability y given its parents
def probability_with_parents(y, conditional_dict):
	prob = 0.0
	index = 0
	for node in nodes_list:
		if node.label == y:
			i = len(node.parents)-1
			for parent in node.parents:
				if conditional_dict[parent] == 1:
					index += 2**i
				i -= 1
			prob = float(node.cpt[index])
			break
	if conditional_dict[y]==1:
		return prob
	else:
		return 1 - prob

def enumerate_all(vars, conditional_dict):
	if len(vars) == 0:
		return 1.0
	top = vars[0]
	if top.label in conditional_dict:
		return probability_with_parents(top.label, conditional_dict) * enumerate_all(vars[1:], conditional_dict)
	else:
		conditional_dict[top.label] = 1
		ans = probability_with_parents(top.label, conditional_dict) * enumerate_all(vars[1:], conditional_dict)
		conditional_dict[top.label] = 0
		ans += probability_with_parents(top.label, conditional_dict) * enumerate_all(vars[1:], conditional_dict)
		del conditional_dict[top.label]
		return ans

# query generation
def generate_query():
	for i in range(number_buttons):
		if(buttons_dict[i]["bg"] == "orange"):
			if(i%4 == 0):
				query_variables[nodes_list[i/4].label] = 1
			if(i%4 == 1):
				query_variables[nodes_list[i/4].label] = 0
			if(i%4 == 2):
				conditional_variables[nodes_list[i/4].label] = 1
			if(i%4 == 3):
				conditional_variables[nodes_list[i/4].label] = 0
	s = "Query: P("
	for key in query_variables.keys():
		if(query_variables[key] == 0):
			s += "~" + key + ", "
		else:
			s += key + ", "
	s += "| "
	for key in conditional_variables.keys():
		if(conditional_variables[key] == 0):
			s += "~" + key + ", "
		else:
			s += key + ", "
	s += ")"
	labels_dict[1]["text"] = s
	test_dict1 = {}
	test_dict2 = {}
	for key in query_variables.keys():
		test_dict1[key] = query_variables[key]

	for key in conditional_variables.keys():
		test_dict1[key] = conditional_variables[key]

	# print(test_dict1)
	val1 = enumerate_all(topo_sort, test_dict1)
	test_dict2 = conditional_variables
	val2 = enumerate_all(topo_sort, test_dict2)
	labels_dict[2]["text"] = "Probability: " + str(val1/val2)

# Build GUI
def gui():
	global frame_up, frame_down, frame_left, frame_right, index, number_buttons, root
	root = Tkinter.Tk()
	width, height = root.winfo_screenwidth(), root.winfo_screenheight()
	root.geometry('%dx%d+0+0' % (width,height))
	frame_up = Tkinter.Frame(root)
	frame_up.grid(row=0,column=0,sticky=Tkinter.N+Tkinter.S+Tkinter.W+Tkinter.E)

	frame_down = Tkinter.Frame(root)
	frame_down.grid(row=1,column=0,sticky=Tkinter.N+Tkinter.S+Tkinter.W+Tkinter.E)

	Tkinter.Grid.rowconfigure(root,0,weight=4)
	Tkinter.Grid.rowconfigure(root,1,weight=2)
	Tkinter.Grid.columnconfigure(root,0,weight=1)

	frame_left = Tkinter.Frame(frame_up,padx=100)
	frame_left.grid(row=0,column=0,sticky=Tkinter.N+Tkinter.S+Tkinter.W+Tkinter.E)

	frame_right = Tkinter.Frame(frame_up,padx=100)
	frame_right.grid(row=0,column=1,sticky=Tkinter.N+Tkinter.S+Tkinter.W+Tkinter.E)

	Tkinter.Grid.rowconfigure(frame_down,0,weight=1)
	Tkinter.Grid.columnconfigure(frame_down,0,weight=1)

	r = 1
	Tkinter.Label(frame_left,text="Query variables", bg='blue').grid(columnspan=2,sticky=Tkinter.N+Tkinter.S+Tkinter.W+Tkinter.E)
	Tkinter.Grid.rowconfigure(frame_left,0,weight=1)
	Tkinter.Label(frame_right,text="Conditional variables", bg='blue').grid(columnspan=2,sticky=Tkinter.N+Tkinter.S+Tkinter.W+Tkinter.E)
	Tkinter.Grid.rowconfigure(frame_right,0,weight=1)

	Tkinter.Grid.columnconfigure(frame_up,0,weight=1)
	Tkinter.Grid.columnconfigure(frame_up,1,weight=1)
	Tkinter.Grid.rowconfigure(frame_up,0,weight=1)

	Tkinter.Grid.columnconfigure(frame_right,0,weight=1)
	Tkinter.Grid.columnconfigure(frame_right,1,weight=1)
	Tkinter.Grid.columnconfigure(frame_left,0,weight=1)
	Tkinter.Grid.columnconfigure(frame_left,1,weight=1)

	for node in nodes_list:
		Tkinter.Grid.rowconfigure(frame_left,r,weight=1)
		Tkinter.Grid.rowconfigure(frame_right,r,weight=1)
		# button1 = Tkinter.Button(frame_left, text = node.label, borderwidth = 2, bd = 50, bg='green', activebackground='orange', padx=25).grid(row = r, column=0, sticky=Tkinter.N+Tkinter.S+Tkinter.W+Tkinter.E)
		buttons_dict[index] = Tkinter.Button(frame_left, text = node.label, borderwidth = 2, bd = 50, bg='green', activebackground='orange', padx=25)
		buttons_dict[index]["command"] = lambda x=index: action(x)
		buttons_dict[index].grid(row = r, column=0, sticky=Tkinter.N+Tkinter.S+Tkinter.W+Tkinter.E)
		
		# button2 = Tkinter.Button(frame_left, text='~' + node.label, borderwidth = 2, bd = 50, bg='green', activebackground='orange', padx=25).grid(row = r, column = 1,sticky=Tkinter.N+Tkinter.S+Tkinter.W+Tkinter.E)
		buttons_dict[index+1] = Tkinter.Button(frame_left, text='~' + node.label, borderwidth = 2, bd = 50, bg='green', activebackground='orange', padx=25)
		buttons_dict[index+1]["command"] = lambda x=index+1: action(x)
		buttons_dict[index+1].grid(row = r, column = 1,sticky=Tkinter.N+Tkinter.S+Tkinter.W+Tkinter.E)

		# button3 = Tkinter.Button(frame_right, text = node.label, borderwidth = 2, bd = 50, bg='green', activebackground='orange', padx=25).grid(row = r,column=0,sticky=Tkinter.N+Tkinter.S+Tkinter.W+Tkinter.E)
		buttons_dict[index+2] = Tkinter.Button(frame_right, text = node.label, borderwidth = 2, bd = 50, bg='green', activebackground='orange', padx=25)
		buttons_dict[index+2]["command"] = lambda x=index+2: action(x)
		buttons_dict[index+2].grid(row = r,column=0,sticky=Tkinter.N+Tkinter.S+Tkinter.W+Tkinter.E)

		# button4 = Tkinter.Button(frame_right, text='~' + node.label, borderwidth = 2, bd = 50, bg='green', activebackground='orange', padx=25).grid(row = r, column = 1,sticky=Tkinter.N+Tkinter.S+Tkinter.W+Tkinter.E)
		buttons_dict[index+3] = Tkinter.Button(frame_right, text='~' + node.label, borderwidth = 2, bd = 50, bg='green', activebackground='orange', padx=25)
		buttons_dict[index+3]["command"] = lambda x=index+3: action(x)
		buttons_dict[index+3].grid(row = r, column = 1,sticky=Tkinter.N+Tkinter.S+Tkinter.W+Tkinter.E)

		# for button 1
		r += 1
		index+=4
		number_buttons+=4
	Tkinter.Grid.rowconfigure(frame_down, 0, weight=1)
	Tkinter.Grid.rowconfigure(frame_down, 1, weight=1)
	Tkinter.Grid.columnconfigure(frame_down, 0, weight=1)
	Tkinter.Grid.columnconfigure(frame_down, 1, weight=1)
	labels_dict[1] = Tkinter.Label(frame_down,text="Query: ",anchor=Tkinter.W)
	labels_dict[1].grid(row=0,column=0,sticky=Tkinter.N+Tkinter.S+Tkinter.W+Tkinter.E)
	labels_dict[2] = Tkinter.Label(frame_down,text="Probability: ",anchor=Tkinter.W)
	labels_dict[2].grid(row=1,column=0,sticky=Tkinter.N+Tkinter.S+Tkinter.W+Tkinter.E)
	Tkinter.Button(frame_down, text='Generate Query',bg='yellow',command=generate_query,padx=5).grid(row=0, column=1, sticky=Tkinter.N+Tkinter.S+Tkinter.W+Tkinter.E)

def run():	
	root.mainloop()