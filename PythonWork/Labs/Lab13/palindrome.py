def palindrome(string):
  if len(string) < 2:
    return True
  elif string[0] != string[-1]:
    return False
  return palindrome(string[1:-1])
