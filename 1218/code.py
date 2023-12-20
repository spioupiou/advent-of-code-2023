import re

def parse(file):
  with open(file) as f:
    lines = [line.strip('\n') for line in f]

    instructions = []
    for line in lines:
      matches = re.search(r'(L|R|U|D)\s(\d+)', line)
      instructions.append([matches.group(1), int(matches.group(2))])

  return instructions

#---------Helpers---------
def print_matrix(matrix):
  for row in matrix:
    print(''.join(row))
  print('\n')


def draw_matrix(instructions):
  dug_tiles = set()
  current = (0, 0)
  direction_map = {'R': (1, 0), 'D': (0, 1), 'L': (-1, 0), 'U': (0, -1)}

  for direction, steps in instructions:
      dx, dy = direction_map[direction]
      for _ in range(steps):
          current = (current[0] + dx, current[1] + dy)
          dug_tiles.add(current)

  # find all coordinates within the dug_tiles
  max_y = max(dug_tiles, key=lambda coord: coord[1])[1]
  max_x = max(dug_tiles, key=lambda coord: coord[0])[0]
  min_y = min(dug_tiles, key=lambda coord: coord[1])[1]
  min_x = min(dug_tiles, key=lambda coord: coord[0])[0]

  matrix = [['#' if (x, y) in dug_tiles else '.' for x in range(min_x, max_x + 1)] for y in range(min_y, max_y + 1)]

  return matrix


def get_neighbours(matrix, current):
  neighbours = []
  x, y = current
  directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up

  for dx, dy in directions:
      nx, ny = x + dx, y + dy
      if 0 <= nx < len(matrix[0]) and 0 <= ny < len(matrix) and (nx, ny) != "#":
          neighbours.append((nx, ny))

  return neighbours


def point_in_polygon(matrix, start, dug_tiles):
  visited = []
  queue = []

  visited.extend(dug_tiles)
  queue.append(start)

  while queue != []:
    current = queue.pop(0)

    neighbours = get_neighbours(matrix, current)

    for neighbour in neighbours:
      if neighbour not in visited:
        visited.append(neighbour)
        queue.append(neighbour)
  
  return visited

def solve_part_1():
  instructions = parse('input.txt')
  matrix = draw_matrix(instructions)

  boundaries = []
  for y, row in enumerate(matrix):
    for x, tile in enumerate(row):
      if tile == '#':
        boundaries.append((x, y))

  # print(boundaries)


  # print_matrix(matrix)
  # find boundaries with the smallest y:
  bounds = list(boundaries)
  bounds.sort(key=lambda coord: (coord[1], coord[0]))
  print(bounds)
  start = ((59 + 63)//2, 1)
  print(start)

  visited = point_in_polygon(matrix, start, boundaries)
  print(len(visited))
  
solve_part_1()