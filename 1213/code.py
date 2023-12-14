import copy

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

def calculate_score(indexes_x, indexes_y):
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

def difference(indexes, original_indexes):
  print(indexes, original_indexes, end =" ")
  if indexes != original_indexes and indexes != []:
    print("in the loop")
    sX = set(indexes)
    soX = set(original_indexes)
    return list(sX.difference(soX))
  else:
    return []
  
def solve_part_1(terrains):
  total = 0
  for terrain in terrains:
    indexes_x = search_x_axis(terrain)
    indexes_y = search_y_axis(terrain)
    score = calculate_score(indexes_x, indexes_y)
    total += score

  print(total)

def solve_part_2(terrains):
  total = 0
  for terrain in terrains:
    broke = False
    original_indexes_x = search_x_axis(terrain)
    original_indexes_y = search_y_axis(terrain)
    print("ORIGINAL: ", original_indexes_x, original_indexes_y)
    for y, row in enumerate(terrain):
      for x, _ in enumerate(row):
        flipped_terrain = flip(copy.deepcopy(terrain), (x,y))
        indexes_x = search_x_axis(flipped_terrain)
        indexes_y = search_y_axis(flipped_terrain)
        result_x = difference(indexes_x, original_indexes_x)
        result_y = difference(indexes_y, original_indexes_y)
        print(result_x, result_y)
        if result_x != [] or result_y != []:
          score = calculate_score(result_x, result_y)
          total += score
          print("in nested loop")
          broke = True
          break
      if broke:
        break
      


  print(total)


terrains = parse('input.txt')
# solve_part_1(terrains)
solve_part_2(terrains)



  