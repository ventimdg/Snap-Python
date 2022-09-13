class Book:
	language = 'English'
	worn_down = False
	varieties = {}
	
	def __init__(self, genre, title, author, publication_year):
		self.genre = genre
		self.title = title
		self.author = author
		self.publication_year = publication_year

		 
	def calculate_age(self):
		#Calculates the age of the book by subtracting its publication year from the current year.
		return 2020 - self.publication_year

	def outdated(self, old_age):
		#Determines if the book is outdated. Takes in an old_age and sets worn_down to True.
		if 2020 - self.publication_year <= old_age:
			return True
		else:
			return False

	def add_genre(self):
		if self.genre not in Book.varieties:
			Book.varieties[self.genre] = [self.title, self.author]

class Textbook(Book):
	publisher = 'Houghton Mifflin Harcourt'

	def random_function(self):
		return 'Do something'

class UCBMFET:
	members = 173532
	topic = "memes"
	posts = {}

	def __init__(self, name):
		self.name = name
		self.activity = 0
		self.posts = 0
		self.member = True
		UCBMFET.members += 1

	def tag_ur_friend_in_meme(self, friend):
		if isinstance(friend, UCBMFET) == True:
			self.activity += 1
			print('@' + friend.name + " is in CS10!")
		else:
			print('You cannot tag someone in a meme if they are not a member of UCBMFET.')

	def post_in_UCBMFET(self, title_of_post):
		if title_of_post in UCBMFET.posts:
			print('You have been banned for reposting a meme.')
		else:
			UCBMFET.posts[title_of_post] = 0
			self.activity += 1
			self.posts += 1
			print('Your total activity on UCMBFET is now ' + str(self.activity) + " and your total posts to UCBMFET is now " + str(self.posts))

	def like_a_post_in_UCBMFET(self, title_of_post):
		self.activity += 1
		UCBMFET.posts[title_of_post] += 1
		print('Your total activity on UCMBFET is now ' + str(self.activity) + ", and the total number of likes on the post " + title_of_post + " is " + str(UCBMFET.posts[title_of_post]))
		
