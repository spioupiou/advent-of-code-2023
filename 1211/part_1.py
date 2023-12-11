import re

class Galaxy:
  def __init__(self, id, coordinates):
    self.id = id
    self.coordinates = coordinates

def parse(file):
  with open(file) as f:
    lines = [line.strip('\n') for line in f]

  image = []

  i = 1
  for line in lines:
    split_line = [*line]
    for index, elt in enumerate(line):
      if elt == '#':
        split_line[index] = str(i)
        i += 1
    image.append(split_line)

  return image

def expand(image):
  indexes_y = []
  for y in range(0, len(image)):
    if all(image[y][x] == '.' for x in range(0, len(image[y]))):
      indexes_y.append(y)

  for i in indexes_y:
    image.insert(len(image[y]) - i, ['.' for i in range(0, len(image[y]))])

  indexes_x = []
  for i in range(len(image[0])):
    # getting column 
    col = [row[i] for row in image]
     
    if all(x == '.' for x in col):
      indexes_x.append(i)
    
  for row in image:
    positions = [len(row)-i for i in indexes_x]
    for pos in positions:
      row.insert(pos, '.')

  return image

def solve_part_1(space_image):
  space_image = expand(space_image)

  all_galaxies = []

  for y in range(0, len(space_image)):
    for x in range(0, len(space_image[y])):
      if space_image[y][x].isdigit():
        all_galaxies.append(Galaxy(space_image[y][x], (x, y)))

  paths = []
  for i, galaxy in enumerate(all_galaxies):
    for j in range(i, len(all_galaxies)):
      if all_galaxies[i].id == all_galaxies[j].id:
        continue
      else:
        path_length = abs(all_galaxies[j].coordinates[0] - all_galaxies[i].coordinates[0]) + abs(all_galaxies[j].coordinates[1] - all_galaxies[i].coordinates[1])
        print(all_galaxies[i].id, all_galaxies[j].id, path_length)
        paths.append(path_length)

  print(len(paths))
  return sum(paths)

space = parse('test_input.txt')
print(solve_part_1(space))

  