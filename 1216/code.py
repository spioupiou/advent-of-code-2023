class Tile:
  def __init__(self, x, y, direction = None):
    self.x = x
    self.y = y
    self.direction = direction

  # Consider two instances equal if same x, y, direction
  def __eq__(self, other):
    if isinstance(other, Tile):
        return self.x == other.x and self.y == other.y and self.direction == other.direction
    return False

def parse(file):
  with open(file) as f:
    lines = [line.strip('\n') for line in f]
  return [list(line) for line in lines]

#---------Helpers---------
def print_matrix(matrix):
  for row in matrix:
    print(''.join(row))
  print('\n')

def move(x, y, direction):
  if direction == '^':
    return x, y - 1
  elif direction == 'v':
    return x, y + 1
  elif direction == '<':
    return x - 1, y
  elif direction == '>':
    return x + 1, y

# Define the mapping
direction_mapping = {
    ('|', '<'): ['^', 'v'],
    ('|', '>'): ['^', 'v'],
    ('-', '^'): ['<', '>'],
    ('-', 'v'): ['<', '>'],
    ('/', '<'): ['v'],
    ('/', '>'): ['^'],
    ('/', '^'): ['>'],
    ('/', 'v'): ['<'],
    ('\\', '<'): ['^'],
    ('\\', '>'): ['v'],
    ('\\', '^'): ['<'],
    ('\\', 'v'): ['>'],
}

def find_next_move(tile):
    next_x, next_y = move(tile.x, tile.y, tile.direction)
    # If next tile within the matrix
    if 0 <= next_x < len(layout[0]) and 0 <= next_y < len(layout):
        next_tile = layout[next_y][next_x]
        if next_tile in '|-/\\':
            new_directions = direction_mapping.get((next_tile, tile.direction), [tile.direction])
            return [Tile(next_x, next_y, direction) for direction in new_directions]
    # If not within the matrix, return an empty list
    else:
        return []
    # All other cases, return with same direction as before ('.', '>-', 'v|' etc.)
    return [Tile(next_x, next_y, tile.direction)]

def count_visited(start):
  visited = set()
  to_visit = [start]

  while to_visit != []:
    current = to_visit.pop()
    tiles = find_next_move(current)
    if len(tiles) == 0:
      continue
    if len(tiles) > 1:
      # Store the other tile in a list and continue with the current one (beam_trajectory[0])
      if tiles[1] not in visited:
        to_visit.append(tiles[1])
    if tiles[0] not in visited:
      to_visit.append(tiles[0])
      current = tiles[0]
    
    if current not in visited:
      visited.add(current)

  unique_tiles = {}
  for tile in visited:
    unique_tiles[(tile.x, tile.y)] = tile.direction
  return len(unique_tiles)

def solve_part_1(layout):
  current = Tile(-1, 0, '>')
  print(count_visited(current))

def solve_part_2(layout):
  all_visited_counts = []

  for y, row in enumerate(layout):
    for x, tile in enumerate(row):
      ## If first row
      if y == 0:
        # Direct downward
        start = Tile(x, y-1, 'v')
        all_visited_counts.append(count_visited(start))
        # Top-left corner
        if x == 0:
          start = Tile(x-1, y, '>')
        # Top-right corner
        elif x == len(row) - 1:
          start = Tile(x+1, y, '<')
        all_visited_counts.append(count_visited(start))

      ## Last row
      elif y == len(layout) - 1:
        start = Tile(x, y+1, '^')
        all_visited_counts.append(count_visited(start))
        # Bottom-left corner
        if x == 0:
          start = Tile(x-1, y, '>')
        # Bottom-right corner
        elif x == len(layout) - 1:
          start = Tile(x+1, y, '<')
        all_visited_counts.append(count_visited(start))

      if x == 0:
        start = Tile(x, y, '>')
        all_visited_counts.append(count_visited(start))  
      elif x == len(row) - 1:
        start = Tile(x, y, '<')
        all_visited_counts.append(count_visited(start))
  
  print(max(all_visited_counts))
  

layout = parse('input.txt')
solve_part_1(layout)
solve_part_2(layout)



