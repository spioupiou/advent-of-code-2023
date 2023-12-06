import re

with open('input.txt') as f:
  lines = f.readlines()

times = re.findall('\d+', lines[0])
distances = re.findall('\d+', lines[1])

race = {'time': int(''.join(times)), 'record': int(''.join(distances))}

winnings = []
wins = 0
record_distance = race['record']

for i in range(0, race['time']):
  distance = 0
  time = race['time']
  time = time - i
  distance = distance + i * time
  if distance > record_distance:
    wins += 1

winnings.append(wins)
print(winnings)

product = 1
for digit in winnings:
  product = product * digit

print(product)