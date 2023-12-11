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
  # Rows entirely made of '.'
  indexes_y = []
  for i, row in enumerate(image):
    if all(num == '.' for num in row):
      indexes_y.append(i)

  # Insert new rows from bottom 
  indexes_y.reverse()
  for i in indexes_y:
    image.insert(i, ['.' for _ in range(len(image[0]))])

  # Columns entirely made of '.'
  indexes_x = []
  for i in range(len(image[0])):
    if all(row[i] == '.' for row in image):
      indexes_x.append(i)
      
  # Insert new columns
  indexes_x.reverse()
  for i in indexes_x:
      for row in image:
          for num in range(0, 1_000_000):
            row.insert(i, '.')

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

space = parse('input.txt')
print(solve_part_1(space))

  