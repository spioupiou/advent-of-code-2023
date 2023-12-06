import re

with open('input.txt') as f:
  lines = f.readlines()

arr = []
times = re.findall('\d+', lines[0])
distances = re.findall('\d+', lines[1])

for i, _ in enumerate(times):
  race = {'time': int(times[i]), 'record': int(distances[i])}
  arr.append(race)

winnings = []
for race in arr:
  wins = 0
  record_distance = race['record']
  # for each unit of time, distance increases by 1
  # 
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