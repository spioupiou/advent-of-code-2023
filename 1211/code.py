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
  for y, line in enumerate(lines):
    split_line = [*line]
    for x, elt in enumerate(line):
      if elt == '#':
        split_line[x] = Galaxy(i, (x, y))
        i += 1
    image.append(split_line)

  return image

def expand(image, num):
  # Rows entirely made of '.'
  indexes_y = []
  for i, row in enumerate(image):
    if all(num == '.' for num in row):
      indexes_y.append(i)

  # Columns entirely made of '.'
  indexes_x = []
  for i in range(len(image[0])):
    if all(row[i] == '.' for row in image):
      indexes_x.append(i)

  expended_galaxies = []
  for row in image:
    for galaxy in row:
      if type(galaxy) == Galaxy:
        expended_galaxies.append(galaxy)

  if num != 1: num -=1

  for galaxy in expended_galaxies:
    original_x, original_y = galaxy.coordinates
    for i in indexes_y:
      if i <= original_y:
        galaxy.coordinates = (galaxy.coordinates[0], galaxy.coordinates[1]+num)

    for j in indexes_x:
      if j <= original_x:
        galaxy.coordinates = (galaxy.coordinates[0]+num, galaxy.coordinates[1])

  return expended_galaxies
  

def calculate_distance(space_image, num):
  all_galaxies = expand(space_image, num)

  paths = []
  for i, galaxy in enumerate(all_galaxies):
    for j in range(i, len(all_galaxies)):
      if all_galaxies[i].id == all_galaxies[j].id:
        continue
      else:
        path_length = abs(all_galaxies[j].coordinates[0] - all_galaxies[i].coordinates[0]) + abs(all_galaxies[j].coordinates[1] - all_galaxies[i].coordinates[1])
        paths.append(path_length)

  return sum(paths)

space = parse('test_input.txt')
print(calculate_distance(space, 1))
print(calculate_distance(space, 1_000_000))

  