import re

def parse(file):
  with open(file) as f:
    lines = f.readlines()

  nums = []
  for line in lines:
    nums.append([int(i) for i in re.findall(r'-?\d+', line)])
  return nums

def solve_part_1(sequences):
  sum = 0
  for sequence in sequences:
    all_patterns = [sequence]
    pattern = [sequence[i+1] - sequence[i] for i in range(len(sequence)-1)]
    all_patterns.append(pattern)
    while not all(i == 0 for i in pattern):
      pattern = [pattern[i+1] - pattern[i] for i in range(len(pattern)-1)]
      all_patterns.append(pattern)
    
    all_patterns.reverse()
    for i, pattern in enumerate(all_patterns):
      if all(i == 0 for i in pattern):
        pattern.append(0)
      else:
        pattern.append(all_patterns[i-1][-1]+pattern[-1])
      
    sum += all_patterns[-1][-1]

  return sum

def solve_part_2(sequences):
  sum = 0
  for sequence in sequences:
    all_patterns = [sequence]
    pattern = [sequence[i+1] - sequence[i] for i in range(len(sequence)-1)]
    all_patterns.append(pattern)
    while not all(i == 0 for i in pattern):
      pattern = [pattern[i+1] - pattern[i] for i in range(len(pattern)-1)]
      all_patterns.append(pattern)
    
    all_patterns.reverse()

    for i, pattern in enumerate(all_patterns):
      if all(i == 0 for i in pattern):
        pattern.insert(0, 0)
      else:
        pattern.insert(0, pattern[0]-all_patterns[i-1][0])
    sum += all_patterns[-1][0]

  return sum

sequences = parse('input.txt')
print(solve_part_1(sequences))
print(solve_part_2(sequences))

  