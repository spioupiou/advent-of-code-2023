import re

def parse(file):
  cards = []
  with open(file) as f:
    lines = f.readlines()
    for line in lines:
      str = re.sub(r'Card\s+\d+:', '', line.strip("\n")).split(" | ")
      for card in str:
        nums = re.findall("\d+", card)
        cards.append([int(i) for i in nums])
    return [cards[i:i+2] for i in range(0, len(cards), 2)]
  
def solve_part_1(cards):
  points = []
  total = 0
  for i in range(0, len(cards)):
    for num in cards[i][1]:
      if total == 0 and num in cards[i][0]:
        total += 1
      elif total != 0 and num in cards[i][0]:
        total *= 2
    points.append(total)
    total = 0
  
  return sum(points)

def solve_part_2(cards):
  # Track number of cards for each index, set default to 1
  number_of_cards = {}
  points = {}
  for i in range(0, len(cards)):
    number_of_cards[i] = 1
    total = 0
    for num in cards[i][1]:
      if num in cards[i][0]:
        total += 1
    points[i] = total

  for i in points.keys():
    point = points[i]
    for j in range(1, point+1):
      number_of_cards[i+j] += number_of_cards[i]
      
  return sum(number_of_cards.values())

  
cards = parse("input.txt")
print(solve_part_1(cards))
print(solve_part_2(cards))