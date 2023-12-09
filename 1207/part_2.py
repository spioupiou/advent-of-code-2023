import re
from collections import defaultdict, Counter
from functools import cmp_to_key

card_values = [("A", 13), ("K", 12), ("Q", 11), ("J", 0), ("T", 9), ("9", 8), ("8", 7), ("7", 6), ("6", 5), ("5", 4), ("4", 3), ("3", 2), ("2", 1)]
card_values = {card: value for card, value in card_values}

hand_types = [(5, 7), (4, 6), ("full", 5), (3, 4), ("double_pair", 3), (2, 2), ("distinct", 1)]
hand_types = {hand: value for hand, value in hand_types}

def parse(file):
  players = []
  with open(file) as f:
    lines = f.readlines()
    for line in lines:
      matches = re.match(r'(\w{5})\s(\d+)', line)
      players.append({'hand': matches.group(1), 'bid': int(matches.group(2))})
  return players

def get_hand_type(hand):
  char_counts = Counter(hand)
  j_count = char_counts.pop('J', None)
  char_counts_arr = list(char_counts.values())

  if len(list(char_counts.values())) == 0:
    max_value = None
  else:
    max_value = max(list(char_counts.values())) 
  if j_count == 5 or j_count == 4:
    return hand_types[5]
  elif j_count == 3 and 2 in char_counts_arr:
    return hand_types[5]
  elif j_count == 2 and 3 in char_counts_arr:
    return hand_types[5]
  elif j_count == 2 and 2 in char_counts_arr:
    return hand_types[4]
  elif j_count == 1 and 4 in char_counts_arr:
    return hand_types[5]
  elif j_count == 1 and 3 in char_counts_arr:
    return hand_types[4]
  elif j_count == 1 and len(list(filter(lambda x: x == 2, char_counts_arr))) == 2:
    return hand_types["full"]
  elif j_count == 1 and 2 in char_counts_arr:
    return hand_types[3]
  elif j_count == 3 or j_count == 2 or j_count == 1:
    return hand_types[j_count+1]
  else:
    if 2 in char_counts_arr and 3 in char_counts_arr:
      return hand_types["full"]
    elif len(list(filter(lambda x: x == 2, char_counts_arr))) == 2:
      return hand_types["double_pair"]
    elif max_value == 1:
      return hand_types["distinct"]
    else:
      return hand_types[max_value]

def sort_hands(first_hand, second_hand):
  first_hand_type = get_hand_type(first_hand)
  second_hand_type = get_hand_type(second_hand)
  if first_hand_type != second_hand_type:
    return second_hand_type - first_hand_type
  else:
    for i in range(0, 5):
      first_card_value = card_values[first_hand[i]]
      second_card_value = card_values[second_hand[i]]
      if first_card_value != second_card_value:
        return second_card_value - first_card_value
      else:
        continue

def rank_players(players):
  hands = []
  for player in players:
    hands.append(player['hand'])

  sorted_hands = sorted(hands, key=cmp_to_key(sort_hands))

  sorted_players = []
  for hand in sorted_hands:
    for player in players:
      if hand == player['hand']:
        sorted_players.append(player)
        break
  return sorted_players

def solve_part_2(players):
  players_ranking = rank_players(players)
  rank = len(players)
  sum = 0

  for player in players_ranking:
    sum += player['bid'] * rank
    rank -= 1
    
  return sum

players = parse("input.txt")
print(solve_part_2(players))
