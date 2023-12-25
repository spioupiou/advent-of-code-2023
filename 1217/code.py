import sys

class Tile:
  def __init__(self, x, y, heat):
    self.x = x
    self.y = y
    self.heat = heat
    self.last_three_moves = []
  
class Graph:
  def __init__(self, tiles, start, end) -> None:
    self.tiles = tiles
    self.start = start
    self.end = end

  # TODO: Add constraints - can't move more than 3 times in same direction, can't go back
  def get_neighbours(self, tile) -> tuple:
    # Up, right, down, left
    adjacent_coordinates = {'U': (0, -1), 'R': (1, 0), 'D': (0, 1), 'L': (-1, 0)}
    neighbours = []
    for direction, adjacent_coordinate in adjacent_coordinates.items():
      neighbour = self.find_by_coordinates(tile.x + adjacent_coordinate[0], tile.y + adjacent_coordinate[1])
      if neighbour != None:
        print(tile.x, tile.y, neighbour.x, neighbour.y, direction)
      # Only append neighbour if it is within the graph and if it doesn't violate the 3 steps constraint
      if neighbour != None and tile.last_three_moves.count(direction) < 3:
        neighbours.append((neighbour, direction))
    return neighbours
  
  def find_by_coordinates(self, x, y) -> Tile:
    for tile in self.tiles:
      if tile.x == x and tile.y == y:
        return tile

  @classmethod
  def parse(cls, file):
    with open(file) as f:
      lines = [line.strip('\n') for line in f]

      tiles = []

      for y, line in enumerate(lines):
        for x, digit in enumerate(line):
          tiles.append(Tile(x, y, int(digit)))

      return Graph(tiles, tiles[0], tiles[-1])
    
  
heat_map = Graph.parse('test_input.txt')

unvisited_nodes = list(heat_map.tiles)
start_node = heat_map.start

# Store the minimum cost of visiting each tile starting from start_node
# key = node, value = heat loss to get to node
shortest_path = {}

# Initialize all nodes to infinity
infinity = sys.maxsize
for node in unvisited_nodes:
  shortest_path[node] = infinity
# Except start node, which is 0 (no heat loss to get to start node)
shortest_path[start_node] = 0

# While there are still unvisited nodes
while unvisited_nodes:
  # Find the node with the smallest cost
  min_node = None
  for node in unvisited_nodes:
    if min_node == None:
      min_node = node
    elif shortest_path[node] < shortest_path[min_node]:
      min_node = node

  # For each neighbour of the node
  neighbours = heat_map.get_neighbours(min_node)
  for neighbour, direction in neighbours:
    # Calculate the cost of getting to the neighbour
    cost = shortest_path[min_node] + neighbour.heat
    # If the cost is less than the current cost of the neighbour
    print(neighbour.last_three_moves)
    if cost < shortest_path[neighbour]:
      # Update the cost of the neighbour
      shortest_path[neighbour] = cost
      neighbour.last_three_moves = (min_node.last_three_moves + [direction])[-3:]

  # Remove the node from the unvisited nodes
  unvisited_nodes.remove(min_node)

print(shortest_path[heat_map.end])