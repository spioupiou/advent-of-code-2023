class Graph:
  def __init__(self, tiles, start, end) -> None:
    self.tiles = tiles
    self.start = start
    self.end = end

  def get_neighbours(self, coords) -> tuple:
    x, y = coords
    adjacent_coordinates = {'^': (0, -1), '>': (1, 0), 'v': (0, 1), '<': (-1, 0)}
    neighbours = []

    for dir, adjacent_coordinate in adjacent_coordinates.items():
      new_x = x + adjacent_coordinate[0]
      new_y = y + adjacent_coordinate[1]

      # If neighbour not within the bounds of matrix, skip
      if new_x < 0 or new_x >= len(self.tiles[0]) or new_y < 0 or new_y >= len(self.tiles):
        continue
      # If neighbour is # then skip
      if self.tiles[new_y][new_x] == '#':
        continue
      
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
      start, end = None, None

      tiles = [[None for _ in range(width)] for _ in range(height)]

      for y, line in enumerate(lines):
        for x, char in enumerate(line):
          tiles[y][x] = char
      
      for y, row in enumerate(tiles):
        for x, char in enumerate(row):
          if y == 0 and char == '.':
            start = (x, y)
          elif y == len(tiles) - 1 and char == '.':
            end = (x, y)
            break

      return Graph(tiles, start, end)

def dfs(graph, node):
  # List to store all the paths from the start node to the end node
  all_paths = []
  # Keep track of the node that needs to be visited next and the path to reach each node
  stack = [(node, [node])]

  # As long as the stack is not empty
  while stack:
    # path = path from the start node to the current node
    node, path = stack.pop()
    # iterate over the neighbours of the current node which are not already in the path
    for next in set(graph.get_neighbours(node)) - set(path):
      # If the neighbour is the end node, add the path to all_paths
      if next == graph.end:
        all_paths.append(path + [next])
      # If the neighbour is not the end node, add the neighbour and the path to reach it to the stack
      else:
        stack.append((next, path + [next]))
    neighbours = graph.get_neighbours(node)

  return all_paths

def find_longest_path(graph):
  all_paths = dfs(graph, graph.start)
  longest_path = max(all_paths, key=len)
  return len(longest_path) - 1
  

def solve_part_1():
  heat_map = Graph.parse('input.txt')

  return find_longest_path(heat_map)

print(solve_part_1())