from colorama import init
init()
from colorama import Fore, Back, Style

"""Fore: BLACK, GREEN, RED, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET
Back: BLACK, GREEN, RED, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET
Style: DIM, NORMAL, BRIGHT, RESET"""

"""Question 1: Write a function that prints given text into a given color"""

def change_text_color(text, color):
	color = color.upper()
	if color == "BLACK":
		return(Fore.BLACK + str(text) + Fore.RESET)
	if color == "GREEN":
		return(Fore.GREEN + str(text) + Fore.RESET)
	if color == "RED":
		return(Fore.RED + str(text) + Fore.RESET)
	if color == "YELLOW":
		return(Fore.YELLOW + str(text) + Fore.RESET)
	if color == "BLUE":
		return(Fore.BLUE + str(text) + Fore.RESET)
	if color == "MAGENTA":
		return(Fore.MAGENTA + str(text) + Fore.RESET)
	if color == "CYAN":
		return(Fore.CYAN + str(text) + Fore.RESET)
	if color == "WHITE":
		return(Fore.WHITE + str(text) + Fore.RESET)
		

	"""Question 2: Write a function that prints given text onto a given background color"""

def change_background_color(text, color):
	color = color.upper()
	if color == "BLACK":
		return(Back.BLACK + str(text) + Back.RESET)
	if color == "GREEN":
		return(Back.GREEN + str(text) + Back.RESET)
	if color == "RED":
		return(Back.RED + str(text) + Back.RESET)
	if color == "YELLOW":
		return(Back.YELLOW + str(text) + Back.RESET)
	if color == "BLUE":
		return(Back.BLUE + str(text) + Back.RESET)
	if color == "MAGENTA":
		return(Back.MAGENTA + str(text) + Back.RESET)
	if color == "CYAN":
		return(Back.CYAN + str(text) + Back.RESET)
	if color == "WHITE":
		return(Back.WHITE + str(text) + Back.RESET)
	

def change_brightness(text, level):
	"""Question 2: Write a function that prints given text in a given brightness level"""
	level = level.upper()
	if level == "DIM":
		return(Style.DIM + str(text) + Style.NORMAL)
	if level == "NORMAL":
		return(Style.NORMAL + str(text) + Style.NORMAL)
	if level == "BRIGHT":
		return(Style.BRIGHT + str(text) + Style.NORMAL)

####### Text Processing with Colorama ########

def read_file(filename):
	"""Returns the text contained in file with given filename."""
	f = open(filename, "r")
	text = f.read()
	return text

def parse_text(text):
	"""Prints the given text with changed formatting according to different conditions"""
	new = text.split()
	answer = []
	helper = ""
	for i in range(0, len(new)):
		temp = new[i]
		helper = str(new[i])
		if len(new[i]) >= 6:
			helper = change_text_color(helper, "BLUE")
		if "t" in temp:
			helper = change_background_color(helper, "YELLOW")
		if temp[-1] == "e":
			helper = change_background_color(helper, "GREEN")
		if temp == temp[::-1]:
			helper = change_brightness(helper, "BRIGHT")
		answer.append(str(helper))
	answer = " ".join(answer)
	print(answer)



text = read_file('tetris.txt')
print(parse_text(text))




















