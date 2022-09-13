
"""x = open("horse_ebooks.txt", "r")
text = x.read()
print(text)"""

def read_file(filename):
    """Returns the text contained in file with given filename."""
    f = open(filename, "r")
    text = f.read()
    return text

def pig_latin(word):
    """ Returns the pig latin translation of a word. """
    vowels = ["a", "e", "i", "o", "u"]
    for i in range(0, len(word)):
   		if word[i] in vowels:
   			return(word[i:] + word[0:i] + "ay")

def izzle(word):
    """ Returns the izzle translation of a word. """
    pain = list(word)
    accident = ["a", "e", "i", "o", "u"]
    pain.reverse()
    for i in range(0, len(word)):
      if pain[i] in accident:
        pain[i] = "izzle"
        hurt = pain[i:]
        hurt.reverse()
        return("".join(hurt))
    return(word + "izzle")

def apply_language_game(text, language_game):
  struggle = text.split()
  answer = []
  for i in range(0, len(struggle)):
    answer.append(language_game(struggle[i]))
  return(" ".join(answer))

"""text = read_file("gettysburg.txt")
print(apply_language_game(text, izzle))"""

def count_words(text):
  """Takes a text and returns a dictionary mapping each word to its count, for example:

  count_words(["Fruits and Vegetables and Vegetables on a Budget and Vegetables at a Store and Vegetables to Clean Fruit and Vegetables"])

  would return: 
  {'and': 5, 'on': 1, 'Vegetables': 5, 'Budget': 1, 'to': 1, 'Fruit': 1, 'a': 2, 'Clean': 1, 'Fruits': 1, 'Store': 1, 'at': 1}
  """
  counted = {}
  temp = text.split()
  for i in range(0,len(temp)):
    if temp[i] in counted:
      counted[temp[i]] += 1
    else:
      counted[temp[i]] = 1
  return counted

"""text = read_file("horse_ebooks.txt")
print(count_words(text))"""

"""text = read_file("horse_ebooks.txt")
counts = count_words(text)
print(sorted(counts))"""

"""print(sorted([-5, -1, 2, 3], key = abs))"""

"""text = read_file("horse_ebooks.txt")
counts = count_words(text)
print(sorted(counts, key = counts.get))"""

"""text = read_file("horse_ebooks.txt")
counts = (count_words(text))
print(sorted(counts, key = counts.get, reverse = True))"""

def top_n_words(counts, n):
    """Returns the top n words by count. For example:

    top_n_words({'and': 5, 'on': 1, 'Vegetables': 5, 'Budget': 1, 'to': 1, 'Fruit': 1, 'a': 2, 'Clean': 1, 'Fruits': 1, 'Store': 1, 'at': 1}, 2)

    would return ["and", "Vegetables"].

    In the case of a tie, it doesn't matter which words are chosen to break the tie."""
    new = sorted(counts, key = counts.get, reverse = True)
    new = new[:n]
    return new


def print_top_n_words(counts, n):
    """Prints the top n words along with their counts. For example:

    print_top_n_words({'and': 5, 'on': 1, 'Vegetables': 5, 'Budget': 1, 'to': 1, 'Fruit': 1, 'a': 2, 'Clean': 1, 'Fruits': 1, 'Store': 1, 'at': 1}, 2)

    would print:
    and 5
    Vegetables 5"""
    temp = top_n_words(counts, n)
    print("\n".join([i + " " + str(counts[i]) for i in temp]))




























