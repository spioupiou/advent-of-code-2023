import copy
import re

def parse(file):
  with open(file) as f:
    lines = f.readlines()
  
  terrains = []
  terrain = []
  for i, line in enumerate(lines):
    if line == '\n':
      terrains.append(terrain)
      terrain = []
    elif line == lines[-1]:
      terrain.append(line.strip('\n'))
      terrains.append(terrain)
    else:
      terrain.append(line.strip('\n'))

  return terrains

def check_horizontal_symmetry(terrain, index):
  start = index
  end = index+1
  while start >= 0 and end < len(terrain):
    if terrain[start] != terrain[end]:
      return False
    start -= 1
    end += 1
  return True

def check_vertical_symmetry(terrain, index):
  start = index
  end = index+1
  while start >= 0 and end < len(terrain[0]):
    col1 = [row[start] for row in terrain]
    col2 = [row[end] for row in terrain]
    if col1 != col2:
      return False
    start -= 1
    end += 1
  return True

def search_x_axis(terrain):
  indexes_x = []
  for i in range(len(terrain[0])-1):
    if all(row[i] == row[i+1] for row in terrain) and check_vertical_symmetry(terrain, i):
      indexes_x.append(i)
  return [idx+1 for idx in indexes_x]


def search_y_axis(terrain):
  indexes_y = []
  for i in range(len(terrain)-1):
    if terrain[i] == terrain[i+1] and check_horizontal_symmetry(terrain, i):
      indexes_y.append(i)
  return [idx+1 for idx in indexes_y]

def calculate_score(terrain):
  indexes_x = search_x_axis(terrain)
  indexes_y = search_y_axis(terrain)

  score = 0
  for index in indexes_y:
    score += index * 100

  for index in indexes_x:
    score += index
  return score

def flip_char(char):
  if char == '#':
    return '.'
  else:
    return '#'
  
def flip(block, coordinates):
  for y, row in enumerate(block):
    for x, char in enumerate(row):
      if x == coordinates[0] and y == coordinates[1]:
        block[y] = row[:x] + flip_char(char) + row[x+1:]
        return block

def solve_part_1(terrains):
  total = 0
  for terrain in terrains:
    score = calculate_score(terrain)
    total += score

  print(total)

def solve_part_2(terrains):
  total = 0
  for terrain in terrains:
    original_score = calculate_score(terrain)
    for y, row in enumerate(terrain):
      for x, _ in enumerate(row):
        score = calculate_score(flip(copy.deepcopy(terrain), (x,y)))
        if score != original_score and score != 0:
          total += score
          break
    
  print(total)


terrains = parse('test_input.txt')
solve_part_1(terrains)
solve_part_2(terrains)






# print(terrain)


  