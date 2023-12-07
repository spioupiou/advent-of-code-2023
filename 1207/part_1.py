import re
from collections import defaultdict, Counter
from functools import cmp_to_key

card_values = [("A", 13), ("K", 12), ("Q", 11), ("J", 10), ("T", 9), ("9", 8), ("8", 7), ("7", 6), ("6", 5), ("5", 4), ("4", 3), ("3", 2), ("2", 1)]
card_values = {card: value for card, value in card_values}

hand_types = [("five", 5), ("four", 4), ("full", "full"), ("three", 3), ("double_pair", "double_pair"), ("pair", 2), ("distinct", 1)]
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
  char_counts = {char: 0 for char in hand}
  for char in hand:
    count = hand.count(char)
    char_counts[char] = count
  char_counts_arr = list(char_counts.values())
  max_value = max(list(char_counts.values()))

  if 2 in char_counts_arr and 3 in char_counts_arr:
    return "full"
  elif len(list(filter(lambda x: x == 2, char_counts_arr))) == 2:
    return "double_pair"
  elif max_value == 5:
    return "five"
  elif max_value == 4:
    return "four"
  elif max_value == 3:
    return "three"
  elif max_value == 2:
    return "pair"
  else:
    return "distinct"

def sort_players_by_hand_type(players):
  players_sorted_by_type = {i: [] for i in hand_types.keys()}

  for player in players:
      hand_type = get_hand_type(player['hand'])
      players_sorted_by_type[hand_type].append(player)

  return players_sorted_by_type

def sort_hands(first_hand, second_hand):
  for i in range(0, 5):
    first_hand_card = first_hand[i]
    second_hand_card = second_hand[i]
    if card_values[first_hand_card] > card_values[second_hand_card]:
      # Return first hand in 0 - 1 comparison
      return -1
      # return first_hand
    elif card_values[first_hand_card] < card_values[second_hand_card]:
      return 1
      # return second_hand
    else:
      continue

def sort_players_by_hand_value(players):
  print("before sorting: ", players)
  hands = []
  for player in players:
    hands.append(player['hand'])

  sorted_hands = sorted(hands, key=cmp_to_key(sort_hands))
  print("sorted hands: ", sorted_hands)

  # TODO: return the players not just the hands ~
  sorted_players = []
  for hand in sorted_hands:
    for player in players:
      if hand == player['hand']:
        sorted_players.append(player)
        break
  print("sorted players: ", sorted_players)
  return sorted_players


def sort_players(players):
  players_by_hand_type = sort_players_by_hand_type(players)
  sorted_players_with_ranks = []
  rank = len(players)
  for type, players in players_by_hand_type.items():
    if len(players) == 1:
      player = players[0]
      sorted_players_with_ranks.append({rank: player})
      rank -= 1
    elif len(players) > 1:
      sorted_players = sort_players_by_hand_value(players)
      for player in sorted_players:
        sorted_players_with_ranks.append({rank: player})
        rank -= 1
  return sorted_players_with_ranks

sum = 0
players = parse("input.txt")
sorted_players = sort_players(players)
for dict in sorted_players:
  for rank, player in dict.items():
    sum += player['bid'] * rank
print(sum)



      
# print(card_values)

# print(total)
