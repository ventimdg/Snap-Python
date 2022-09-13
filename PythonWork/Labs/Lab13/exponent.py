def exponent(num, power):
  result = 1
  while power > 0:
    result = result * num
    power = power - 1
  return result
