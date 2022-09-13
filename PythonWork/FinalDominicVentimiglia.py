### 2020Fa CS10 With-Computer Final Exam: Python

def max_hops(i, L):
	""" Return the maximum number of hops to exit the maze from the current position;
	I is the index encoding the current position
	L is the maze

	>>> max_hops(0, [3, 9, 9, 0])
	1
	>>> max_hops(0, [3, 4, 5, 2, 11, 0])
	3	
	"""
	# Your solution below
	answer = 0
	while i != (len(L) - 1):
		if i - L[i] >= 0:
			if (i - L[i]) - (L[i - L[i]]) >= 0 or (i - L[i]) + (L[i - L[i]]) < len(L):
				i = i - L[i]
				answer += 1
			else:
				i = i + L[i]
				answer += 1
		else:
			i = i + L[i]
			answer += 1
	return answer

	"""answer = 0 
	while i != (len(L) - 1):
		if i - L[i] >= 0:
			i = i - L[i]
			answer += 1
		else:
			i = i + L[i]
			answer += 1
	return answer"""

"""I did not know whether we had to create a check that checked if a move caused the player to get stuck. For example, if the board is [3,11,5,2,11,0], the players first move would be to the
two but has two options for a second move. Obviously, moving left would cause the player to get stuck because there aren't 11 blocks to move to so it would cause an error and the player would
have to move to the right. The first code on top accounts for that type of check because I did not know if we needed to check for something like that. The code below (the second one) works on the examples given but
does not check if a move would result in an impossible spot that would cause an error"""