import copy

def parse(file):
  with open(file) as f:
    lines = f.readlines()
  
  terrains = []
  terrain = []
  for line in lines:
    if line == '\n':
      terrains.append(terrain)
      terrain = []
    elif line == lines[-1]:
      terrain.append(line.strip('\n'))
      terrains.append(terrain)
    else:
      terrain.append(line.strip('\n'))

  return terrains

def is_symmetrical(terrain, index, axis):
  start = index
  end = index+1
  if axis == "horizontal":
    # Iterate through all the rows
    while start >= 0 and end < len(terrain):
      if terrain[start] != terrain[end]:
        return False
      start -= 1
      end += 1
    return True
  elif axis == "vertical":
    # Iterate through all the columns
    while start >= 0 and end < len(terrain[0]):
      col1 = [row[start] for row in terrain]
      col2 = [row[end] for row in terrain]
      if col1 != col2:
        return False
      start -= 1
      end += 1
    return True    


# def search_x_axis(terrain):
#   indexes_x = []
#   for i in range(len(terrain[0])-1):
#     if is_symmetrical(terrain, i, "vertical"):
#       indexes_x.append(i)
#   return [idx+1 for idx in indexes_x]


# def search_y_axis(terrain):
#   indexes_y = []
#   for i in range(len(terrain)-1):
#     if is_symmetrical(terrain, i, "horizontal"):
#       indexes_y.append(i)
#   return [idx+1 for idx in indexes_y]

def calculate_score(indexes_x, indexes_y):
  score = 0
  for index in indexes_y:
    score += index * 100

  for index in indexes_x:
    score += index
  return score

def flip_char(char):
  return '.' if char == '#' else '#'
  
def flip(block, coordinates):
  block_cp = copy.deepcopy(block)

  for y, row in enumerate(block_cp):
    for x, char in enumerate(row):
      if x == coordinates[0] and y == coordinates[1]:
        block_cp[y] = row[:x] + flip_char(char) + row[x+1:]
        return block_cp

def find_difference(indexes, original_indexes):
  if indexes != original_indexes and indexes != []:
    # Return the difference between the two lists
    return list(set(indexes).difference(set(original_indexes)))
  else:
    return []
  
def solve_part_1(terrains):
  total = 0
  for terrain in terrains:
    # Iterate through all the columns (take the length of the first row)
    # Add 1 to the index as row/column starts at 1
    axes_x = [i+1 for i in range(len(terrain[0])-1) if is_symmetrical(terrain, i, "vertical")]
    # Iterate through all the rows
    axes_y = [i+1 for i in range(len(terrain)-1) if is_symmetrical(terrain, i, "horizontal")]

    score = calculate_score(axes_x, axes_y)
    total += score

  print(total)

def solve_part_2(terrains):
  total = 0
  for terrain in terrains:
    broke = False
    # Iterate through all the columns (take the length of the first row)
    original_axes_x = [i+1 for i in range(len(terrain[0])-1) if is_symmetrical(terrain, i, "vertical")]
    # Iterate through all the rows
    original_axes_y = [i+1 for i in range(len(terrain)-1) if is_symmetrical(terrain, i, "horizontal")]

    for y, row in enumerate(terrain):
      for x, _ in enumerate(row):
        flipped_terrain = flip(terrain, (x,y))
        axes_x = [i+1 for i in range(len(terrain[0])-1) if is_symmetrical(flipped_terrain, i, "vertical")]
        axes_y = [i+1 for i in range(len(terrain)-1) if is_symmetrical(flipped_terrain, i, "horizontal")]
        result_x = find_difference(axes_x, original_axes_x)
        result_y = find_difference(axes_y, original_axes_y)
        if result_x != [] or result_y != []:
          score = calculate_score(result_x, result_y)
          total += score
          broke = True
          break
      if broke:
        break
      


  print(total)


terrains = parse('input.txt')
solve_part_1(terrains)
solve_part_2(terrains)



  