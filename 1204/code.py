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
  duplicate_cards = {}
  for i in range(0, len(cards)):
    duplicate_cards[i] = 1

  for i in range(0, len(cards)):
    total = 0
    number_of_cards = duplicate_cards[i]
    for n in range(0, number_of_cards):
      for num in cards[i][1]:
        if num in cards[i][0]:
          total += 1
      while total > 0:
        duplicate_cards[i+total] += 1
        total -= 1
    
  return sum(duplicate_cards.values())

  
cards = parse("input.txt")
print(solve_part_1(cards))
print(solve_part_2(cards))