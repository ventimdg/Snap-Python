# Exercise 1
#def push_first_odd_back(lst):
	#test = lst[:]
	#i = 0
	#while lst == test and i < len(lst):
		#if lst[i]%2 == 1:
			#lst.append(lst[i])
			#lst.pop(i)
		#else:
			#i += 1

#why does this break with [0, 0, 1]

def push_first_odd_back(lst):
	test = lst[:]
	for i in range(0, len(lst)):
		if test == lst and lst[i]%2 == 1:
			lst.append(lst[i])
			lst.pop(i)


# Exercise 2
def flatten(lst):
	x = []
	for i in range(0, len(lst)):
		x += lst[i]
	lst = x
	return lst

# Exercise 3.1
def squares_of_evens(lst):
	return [x * x for x in lst if (x % 2 == 0)]

# Exercise 3.2
def nth_power_of_evens(lst, n):
    return [x ** n for x in lst if (x % 2 == 0)]

# Exercise 4
def substitute_base(string, old, new):
	answer = [letter for letter in string]
	for i in range(0, len(string)):
		if answer[i] == old:
			answer[i] = new
	return "".join(answer)

# Exercise 5
def combine(lst):
	if str(lst[0]).isdigit() == True:
		x = 0
		for i in range(0, len(lst)):
			x += lst[i]
	else:
		x = "".join(lst)
	return x

# Exercise 6
def base_freq(string):
	data = [letter for letter in string]
	DNA = {}
	for i in range(0, len(string)):
		if data[i] in DNA:
			DNA[data[i]] += 1
		else:
			DNA[data[i]] = 1
	return DNA

# Exercise 7.1
def substitute_chars(string, replacements):
	jumble = [letter for letter in string]
	for i in range(0, len(string)):
		if jumble[i] in replacements:
			jumble[i] = replacements[jumble[i]]
	return "".join(jumble)

# Exercise 7.2
def invert_dict(original):
	x = list(original.keys())
	invert = {}
	for i in range(0, len(original)):
		invert[original[x[i]]] = x[i]
	return invert 













