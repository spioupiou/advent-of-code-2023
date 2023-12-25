import sys

class Tile:
  def __init__(self, x, y, heat):
    self.x = x
    self.y = y
    self.heat = heat
  
class Graph:
  def __init__(self, tiles, start, end) -> None:
    self.tiles = tiles
    self.start = start
    self.end = end

  # TODO: Add constraints - can't move more than 3 times in same direction, can't go back
  def get_neighbours(self, tile) -> tuple:
    # Up, right, down, left
    adjacent_coordinates = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    neighbours = []
    for adjacent_coordinate in adjacent_coordinates:
      neighbour = self.find_by_coordinates(tile.x + adjacent_coordinate[0], tile.y + adjacent_coordinate[1])
      # Only append neighbour if it is within the graph
      if neighbour != None:
        neighbours.append(neighbour)
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
  for neighbour in heat_map.get_neighbours(min_node):
    # Calculate the cost of getting to the neighbour
    cost = shortest_path[min_node] + neighbour.heat
    # If the cost is less than the current cost of the neighbour
    if cost < shortest_path[neighbour]:
      # Update the cost of the neighbour
      shortest_path[neighbour] = cost

  # Remove the node from the unvisited nodes
  unvisited_nodes.remove(min_node)

print(shortest_path[heat_map.end])