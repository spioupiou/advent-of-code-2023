import re

with open('test_input.txt') as f:
  lines = f.readlines()

number_words = {
    'zero': '0',
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

first_last_digits = []
for i, line in enumerate(lines):
  line = line.strip('\n')
  digits = re.findall(r'zero|one|two|three|four|five|six|seven|eight|nine|\d', line)
  
  if len(digits) == 1:
    first_last_digits.extend([digits[0], digits[0]])
    print(i+1, digits[0], digits[0])
  else:
    first_last_digits.extend([digits[0], digits[-1]])
    print(i+1, digits[0], digits[-1])

# print(first_last_digits)

arr = []
for i in range(0, len(first_last_digits), 2):
  if i == len(first_last_digits) - 1:
    break
  digit1 = number_words.get(first_last_digits[i], first_last_digits[i])
  digit2 = number_words.get(first_last_digits[i+1], first_last_digits[i+1])
  str = digit1+digit2
  arr.append(int(str))

print(sum(arr))