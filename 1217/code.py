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

  def get_neighbours(self, tile, dir, steps) -> tuple:
    adjacent_coordinates = {'U': (0, -1), 'R': (1, 0), 'D': (0, 1), 'L': (-1, 0)}
    neighbours = []

    for new_dir, adjacent_coordinate in adjacent_coordinates.items():
      neighbour = self.find_by_coordinates(tile.x + adjacent_coordinate[0], tile.y + adjacent_coordinate[1])

      # If neighbour within bounds
      if neighbour != None:
        # Make sure that the neighbour is not the previous node
        if (dir == 'U' and new_dir == 'D') or (dir == 'R' and new_dir == 'L') or (dir == 'D' and new_dir == 'U') or (dir == 'L' and new_dir == 'R'): 
          continue
        # Crucible can move in the same direction up to 10 steps
        if dir == new_dir and steps + 1 <= 10:
          neighbours.append((neighbour, new_dir, steps + 1))
        # Crucible can change direction after 4 steps and must change direction after 10 steps
        elif dir != new_dir and 4 <= steps <= 10:
          neighbours.append((neighbour, new_dir, 1))
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

def find_shortest_path(graph):
  start = graph.start
  end = graph.end
  unvisited = set()
  unvisited.add((start.x, start.y, 'D', 0))
  unvisited.add((start.x, start.y, 'R', 0))

  processed_nodes = set()

  # Store the minimum cost of visiting each tile starting from start. Use start with cost 0 as the starting point
  # key = coordinates, number of steps, direction -- value = heat loss to get to node
  shortest_path = {(start.x, start.y, 'D', 0): 0, (start.x, start.y, 'R', 0): 0}

  # results = []

  # While there are still unvisited nodes
  while unvisited:
    # Find the node with the smallest cost
    min_node_key = min(unvisited, key=lambda node: shortest_path[node])
    
    if min_node_key[0] == end.x and min_node_key[1] == end.y and min_node_key[3] >= 4:
      return shortest_path[min_node_key]

    neighbours = heat_map.get_neighbours(graph.find_by_coordinates(min_node_key[0], min_node_key[1]), min_node_key[2], min_node_key[3])
    # For each neighbour of the node
    for neighbour, dir, steps in neighbours:
      # Calculate the cost of getting to that neighbour
      neighbour_key = (neighbour.x, neighbour.y, dir, steps)
      # Skip if neighbour has already been processed
      if neighbour_key in processed_nodes: continue

      # Calculate the cost of the neighbour: 
      cost = shortest_path[min_node_key] + neighbour.heat
      # Update the cost if the cost of the neighbour is not stored yet/if the cost is less than stored cost
      if neighbour_key not in shortest_path.keys() or cost < shortest_path[neighbour_key]:
        shortest_path[neighbour_key] = cost
        # Add the neighbour to the unvisited nodes
        unvisited.add(neighbour_key)
    
    # Add the node to the processed nodes and remove it from the unvisited nodes
    processed_nodes.add(min_node_key)
    unvisited.remove(min_node_key)

heat_map = Graph.parse('test_input.txt')
result = find_shortest_path(heat_map)
print(result)