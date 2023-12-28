class Graph:
  def __init__(self, tiles, height, width) -> None:
    self.tiles = tiles
    self.height = height
    self.width = width

  def get_neighbours(self, coords) -> tuple:
    x, y = coords
    adjacent_coordinates = {'^': (0, -1), '>': (1, 0), 'v': (0, 1), '<': (-1, 0)}
    neighbours = []

    for dir, adjacent_coordinate in adjacent_coordinates.items():
      new_x = x + adjacent_coordinate[0]
      new_y = y + adjacent_coordinate[1]

      # If neighbour not within the bounds of matrix, skip
      if new_x < 0 or new_x >= self.width or new_y < 0 or new_y >= self.height:
        continue
      # If neighbour is # then skip
      if self.tiles[new_y][new_x] == '#':
        continue

      # If neighbour is previous node then skip
      
      # If ^ > < v then only possible move is in the direction the arrow is pointing
      if self.tiles[y][x] in ['^', '>', 'v', '<'] and self.tiles[y][x] != dir:
        continue

      neighbours.append((new_x, new_y))
    return neighbours

  @classmethod
  def parse(cls, file):
    with open(file) as f:
      lines = [line.strip('\n') for line in f]
      height = len(lines)
      width = len(lines[0])

      tiles = [[None for _ in range(width)] for _ in range(height)]

      for y, line in enumerate(lines):
        for x, char in enumerate(line):
          tiles[y][x] = char
      
      return Graph(tiles, height, width)

def find_longest_path(graph, node):
  visited = []
  queue = []

  visited.append(node)
  queue.append(node)

  while queue:
    new_node = queue.pop(0) 
    neighbours = graph.get_neighbours(new_node)
    for neighbour in neighbours:
      if neighbour not in visited:
        visited.append(neighbour)
        queue.append(neighbour)

  return len(visited)
  

def solve_part_1():
  heat_map = Graph.parse('test_input.txt')
  start_node = None
  for i, char in enumerate(heat_map.tiles[0]):
    if char != '#':
      start_node = (i, 0)
      break
  return find_longest_path(heat_map, start_node)

print(solve_part_1())