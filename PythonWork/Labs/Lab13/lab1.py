print("Hello, World")

a = 5

def count_up(num):
	for i in range(1, num+1):
		print(i)

def reverse_string(string):
	x = ""
	for i in range(0, len(string)):
		x = string[i] + x
	return(x)

#ask why reverse string is inclusive for right endpoint. I think I have it figured out, since 
#python is zero indexed, the length fucntion I used already incorporates the plus 1

import turtle as t 
def fractal(level, size):
	if level == 1:
		t.forward(size)
	else:
		t.left(45)
		fractal(level-1, size)
		t.right(90)
		fractal(level-1, size)
		t.left(45)

def write(message):
	t.penup()
	t.goto(-300,200)
	t.pendown()
	t.write("Dominic Ventimiglia, Struggling College Student", font=("Arial", 30, "normal"))

def lab(checkoff):
	fractal(6, 30)
	write("message")
