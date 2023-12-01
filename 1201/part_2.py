import re

with open('input.txt') as f:
  lines = f.readlines()

number_words = {
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
  digits = re.findall(r'(?=(one|two|three|four|five|six|seven|eight|nine|\d))', line)
  if len(digits) == 1:
    first_last_digits.append((digits[0], digits[0]))
  else:
    first_last_digits.append((digits[0], digits[-1]))

arr = []
for pair in first_last_digits:
  digit1 = pair[0]
  digit2 = pair[1]

  str = number_words.get(digit1, digit1) + number_words.get(digit2, digit2)
  arr.append(int(str))

print(sum(arr))