class Node:
  def __init__(self, x, y, neighbours = None) -> None:
    self.x = x
    self.y = y
    self.neighbours = neighbours


class Graph:
  def __init__(self, tiles, start, end) -> None:
    self.tiles = tiles
    self.start = start
    self.end = end

  def get_neighbours(self, coords) -> tuple:
    x, y = coords
    adjacent_coordinates = {'^': (0, -1), '>': (1, 0), 'v': (0, 1), '<': (-1, 0)}
    neighbours = {}

    for dir, adjacent_coordinate in adjacent_coordinates.items():
      new_x = x + adjacent_coordinate[0]
      new_y = y + adjacent_coordinate[1]

      # If neighbour not within the bounds of matrix, skip
      if new_x < 0 or new_x >= len(self.tiles[0]) or new_y < 0 or new_y >= len(self.tiles):
        continue
      # If neighbour is # then skip
      if self.tiles[new_y][new_x] == '#':
        continue

      neighbours[(new_x, new_y)] = 1
    return neighbours
  
  def create_weighted_graph(self):
    weighted_graph = {}
    for y in range(0, len(self.tiles)):
      for x in range(0, len(self.tiles[y])):
        if self.tiles[y][x] == '.':
          neighbours = self.get_neighbours((x, y))
          weighted_graph[(x, y)] = Node(x, y, neighbours)

    # Copy the graph to avoid modifying it while iterating
    # graph = weighted_graph.copy()
    nodes_to_remove = []

    ## Reduce the graph: delete node with two neighbours and connect the neighbours
    # {
    #   (3, 3): Node(x=3, y=3, neighbours = {(3, 4):1, ...})
    #   (3, 4): Node(x=3, y=4, neighbours = {(3, 3):1, (3, 5):1})
    #   (3, 5): Node(x=3, y=5, neighbours = {(3, 4):1, ...})
    # }

    # {
    #   (3, 3): Node(x=3, y=3, neighbours = {(3, 5):2, ...})
    #   (3, 5): Node(x=3, y=5, neighbours = {(3, 3):2, ...})
    # }
    for node, data in weighted_graph.items():

      if len(data.neighbours) == 2:
        # Get the two neighbours
        (neighbour1), (neighbour2) = data.neighbours.items()

        # Remove the current node from the neighbours
        removed = weighted_graph[neighbour1[0]].neighbours.pop(node)
        weighted_graph[neighbour1[0]].neighbours[neighbour2[0]] = removed + neighbour2[1]

        removed = weighted_graph[neighbour2[0]].neighbours.pop(node)
        weighted_graph[neighbour2[0]].neighbours[neighbour1[0]] = removed + neighbour1[1]

        # Mark the node for removal
        nodes_to_remove.append(node)

    # Remove the nodes
    for node in nodes_to_remove:
      del weighted_graph[node]

    return weighted_graph

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
          if char in ['^', '>', 'v', '<']:
            tiles[y][x] = '.'
          else:
            tiles[y][x] = char
      
      for y, row in enumerate(tiles):
        for x, char in enumerate(row):
          if y == 0 and char == '.':
            start = (x, y)
          elif y == len(tiles) - 1 and char == '.':
            end = (x, y)
            break

      return Graph(tiles, start, end)
    


def dfs(reduced, start, end):
  # List to store all the paths from the start node to the end node
  all_paths = []
  stack = [[(start, 0)]]

  while stack:
    # Get the last path from the stack
    path = stack.pop()
    # Get the last node from the path
    node, steps = path[-1]
    # If we reached the end node, add the path to the list of paths
    if node == end:
      all_paths.append(path)
    else:
      # Push paths with the neighbours to the stack
      for neighbour, step in reduced[node].neighbours.items():
          if neighbour not in [node for node, _ in path]:
            new_path = list(path)
            new_path.append((neighbour, steps + step))
            stack.append(new_path)
  return all_paths

def solve_part_2():
  weighted_graph = {}
  heat_map = Graph.parse('input.txt')
  weighted_graph = heat_map.create_weighted_graph()
  all_paths = dfs(weighted_graph, heat_map.start, heat_map.end)
  return max([path[-1][1] for path in all_paths])

print(solve_part_2())

