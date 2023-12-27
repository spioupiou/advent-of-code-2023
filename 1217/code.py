import sys

class Tile:
  def __init__(self, x, y, heat):
    self.x = x
    self.y = y
    self.heat = heat
    self.steps = 0
    self.direction = None
    self.prev = None
  
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

      if neighbour != None and neighbour != tile.prev:
        neighbour.direction = direction
        neighbour.prev = tile
        if neighbour.direction != tile.direction:
          neighbour.steps = 1
        else:
          neighbour.steps = tile.steps + 1
        if neighbour.steps <= 3:
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
start_node = heat_map.start
queue = set()
queue.add((start_node.x, start_node.y, 0, 'R'))

processed_nodes = set()

# Store the minimum cost of visiting each tile starting from start_node. Use start_node with cost 0 as the starting point
# key = coordinates, number of steps, direction -- value = heat loss to get to node
shortest_path = {(start_node.x, start_node.y, 0, 'R'): 0}

i = 0
# While there are still unvisited nodes
while queue:
  # Find the node with the smallest cost
  min_node_key = None
  for node_key in queue:
    if min_node_key == None:
      min_node_key = node_key
    elif shortest_path[node_key] < shortest_path[min_node_key]:
      min_node_key = node_key

  # For each neighbour of the node
  neighbours = heat_map.get_neighbours(heat_map.find_by_coordinates(min_node_key[0], min_node_key[1]))
  for neighbour in neighbours:
    # Calculate the cost of getting to the neighbour
    neighbour_key = (neighbour.x, neighbour.y, neighbour.steps, neighbour.direction)
    if neighbour_key in processed_nodes: continue
    cost = shortest_path[min_node_key] + neighbour.heat
    # If the cost is less than the current cost of the neighbour or if the neighbour has not been visited yet
    if neighbour_key not in shortest_path.keys() or cost < shortest_path[neighbour_key]:
      # Update the cost of the neighbour
      shortest_path[neighbour_key] = cost
      print(min_node_key, neighbour_key, cost)
      queue.add(neighbour_key)
  print('---')
  processed_nodes.add(min_node_key)
  # Remove the node from the unvisited nodes
  queue.remove(min_node_key)