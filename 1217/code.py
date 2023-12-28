class Graph:
  def __init__(self, tiles, height, width) -> None:
    self.tiles = tiles
    self.height = height
    self.width = width

  def get_neighbours(self, shortest_path_key, min_steps, max_steps) -> tuple:
    x, y, dir, steps = shortest_path_key
    adjacent_coordinates = {'U': (0, -1), 'R': (1, 0), 'D': (0, 1), 'L': (-1, 0)}
    neighbours = []

    for new_dir, adjacent_coordinate in adjacent_coordinates.items():
      new_x = x + adjacent_coordinate[0]
      new_y = y + adjacent_coordinate[1]

      # If neighbour not within the bounds of matrix, skip
      if new_x < 0 or new_x >= self.width or new_y < 0 or new_y >= self.height:
        continue

      # Make sure that the neighbour is not the previous node
      if (dir == 'U' and new_dir == 'D') or (dir == 'R' and new_dir == 'L') or (dir == 'D' and new_dir == 'U') or (dir == 'L' and new_dir == 'R'): 
        continue

      # Crucible can move in the same direction up to 10 steps
      if dir == new_dir and steps + 1 <= max_steps:
        neighbours.append((new_x, new_y, new_dir, steps + 1))
      # Crucible can change direction after min. 4 steps and must change direction after 10 steps
      elif dir != new_dir and min_steps <= steps <= max_steps:
        neighbours.append((new_x, new_y, new_dir, 1))
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
          heat = int(char)
          tiles[y][x] = heat
      
      return Graph(tiles, height, width)

def find_shortest_path(graph, min_steps, max_steps):
  unvisited = set()
  unvisited.add((0, 0, 'D', 0))
  unvisited.add((0, 0, 'R', 0))

  processed_nodes = set()

  # Store the minimum cost of visiting each tile starting from start. Use start with cost 0 as the starting point
  # key = coordinates, number of steps, direction -- value = heat loss to get to node
  shortest_path = {(0, 0, 'D', 0): 0, (0, 0, 'R', 0): 0}

  # While there are still unvisited nodes
  while unvisited:
    # Find the node with the smallest cost
    min_node_key = min(unvisited, key=lambda node: shortest_path[node])

    # If we reached the end in at least 4 steps in the same direction, return the total heat loss
    if min_node_key[0] == graph.width - 1 and min_node_key[1] == graph.height - 1 and min_node_key[3] >= min_steps:
      return shortest_path[min_node_key]

    neighbours = graph.get_neighbours(min_node_key, min_steps, max_steps)
    # For each neighbour of the node
    for x, y, dir, steps in neighbours:
      # Calculate the cost of getting to that neighbour
      neighbour_key = (x, y, dir, steps)
      # Skip if neighbour has already been processed
      if neighbour_key in processed_nodes: continue

      # Calculate the cost of the neighbour: 
      cost = shortest_path[min_node_key] + graph.tiles[y][x]
      # Update the cost if the cost of the neighbour is not stored yet/if the cost is less than stored cost
      if neighbour_key not in shortest_path.keys() or cost < shortest_path[neighbour_key]:
        shortest_path[neighbour_key] = cost
        # Add the neighbour to the unvisited nodes
        unvisited.add(neighbour_key)
    
    # Add the node to the processed nodes and remove it from the unvisited nodes
    processed_nodes.add(min_node_key)
    unvisited.remove(min_node_key)

def solve_part_1():
  heat_map = Graph.parse('input.txt')
  return find_shortest_path(heat_map, min_steps=0, max_steps=3)

def solve_part_2():
  heat_map = Graph.parse('input.txt')
  return find_shortest_path(heat_map, min_steps=4, max_steps=10)

print(solve_part_1())
print(solve_part_2())