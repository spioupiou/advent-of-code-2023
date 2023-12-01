import re

with open('test_input.txt') as f:
  lines = f.readlines()

first_last_digits = []
for line in lines:
  line = line.strip('\n')
  digits = re.findall('\d', line)
  print(digits)
  if len(digits) == 1:
    first_last_digits.extend([digits[0], digits[0]])
  else:
    first_last_digits.extend([digits[0], digits[-1]])

print(first_last_digits)

arr = []

for i in range(0, len(first_last_digits), 2):
  if i == len(first_last_digits) - 1:
    break
  str = first_last_digits[i]+first_last_digits[i+1]
  arr.append(int(str))

print(sum(arr))