from itertools import product
import re

def parse(file):
  with open(file) as f:
    lines = [line.strip('\n') for line in f]

  springs = []
  for line in lines:
    matches = re.search(r'(.*)\s(.*)', line)
    sequence, condition = matches.group(1), matches.group(2)
    condition = condition.split(',')
    springs.append((sequence, [int(i) for i in condition]))

  return springs

def check_valid(sequence, condition):
  regex_str = ''
  for i, con in enumerate(condition):
    if i == len(condition) - 1:
      regex_str += '#{%d}' % con
    else:
      regex_str += '#{%d}\.+' % con
  
  regex_str = '^\.*' + regex_str + '\.*$'
  return re.match(regex_str, sequence)


def generate_all_sequences(sequence, condition):
  broken_diff = sum(condition) - sequence.count('#')
  unknowns = sequence.count('?')
  operational_diff = unknowns - broken_diff
  indexes = [i for i, char in enumerate(sequence) if char == '?']
  count = 0
  possibilities = product(['.', '#'], repeat=operational_diff + broken_diff)
  possibilities = [''.join(p) for p in possibilities if p.count('.') == operational_diff and p.count('#') == broken_diff]
  for pos in possibilities:
    for i, num in enumerate(indexes):
      sequence = sequence[:num] + pos[i] + sequence[num + 1:]
    if check_valid(sequence, condition):
      count += 1
  return count

springs = parse('input.txt')

total = 0
for record in springs:
  sequence, condition = record[0], record[1]
  count = generate_all_sequences(sequence, condition)
  total += count

print(total)


  