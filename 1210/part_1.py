import re

class Pipe:
  def __init__(self, coordinates, type):
    self.coordinates = coordinates
    self.type = type

class PipeNetwork:
  def __init__(self, pipes, start = None, visited = None):
    self.types = pipes
    self.visited = visited
    self.start = start

  def is_valid_neighbour(self, pipe, neighbour):
    if pipe.type == '.' or pipe.type == 'S':
      return False
    # if neighbour is up
    if neighbour.coordinates[1] == pipe.coordinates[1]-1:
      if pipe.type in ['|', 'L', 'J'] and neighbour.type in ['F','7', '|']:
        return True
    # elif neighbour is down
    elif neighbour.coordinates[1] == pipe.coordinates[1]+1:
      if pipe.type in ['|', '7', 'F'] and neighbour.type in ['|', 'L', 'J']:
        return True
    # elif neighbour is left
    elif neighbour.coordinates[0] == pipe.coordinates[0]-1:
        if pipe.type in ['-', 'J', '7'] and neighbour.type in ['-', 'F', 'L']:
          return True
    # elif neighbour is right
    elif neighbour.coordinates[0] == pipe.coordinates[0]+1:
        if pipe.type in ['-', 'L', 'F'] and neighbour.type in ['-', '7', 'J']:
            return True

    return False
  
  def find_in_pipes(self, coordinates):
    for pipe in self.types:
      if pipe.coordinates == coordinates:
        return pipe
    return None

  def get_neighbours(self, pipe):
    NEIGHBOURS_COORDINATES = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbours = []
    for coordinates in NEIGHBOURS_COORDINATES:
      neighbour = self.find_in_pipes((pipe.coordinates[0]+coordinates[0], pipe.coordinates[1]+coordinates[1]))
      if neighbour != None and self.is_valid_neighbour(pipe, neighbour):
        neighbours.append(neighbour)

    return neighbours

def parse(file):
  with open(file) as f:
    lines = f.readlines()

  network = PipeNetwork([])
  for y, line in enumerate(lines):
    line = line.strip('\n')
    for x in range(0, len(line)):
      if line[x] == 'S':
        network.start = Pipe((x, y), line[x])
      network.types.append(Pipe((x, y), line[x]))
  return network

def bfs(graph, node):
  visited = []
  queue = []

  visited.append(node)
  queue.append(node)

  while queue:          # Creating loop to visit each node
    new_node = queue.pop(0) 
    neighbours = graph.get_neighbours(new_node)
    print("node: ", new_node.coordinates, new_node.type, end = " ")
    for neighbour in neighbours:
      print('neighbour: ', neighbour.coordinates, neighbour.type, end = " ")
      if neighbour not in visited:
        visited.append(neighbour)
        queue.append(neighbour)
    print('\n')

  return(len(visited)/2)

def solve_part_1(network):
  visited_list = []

  neighbours = network.get_neighbours(network.start)
  for neighbour in neighbours:
    print(neighbour.coordinates, neighbour.type, end = " ")

  for i in ['|', '-', 'L', 'J', '7', 'F']:
    starting_point = Pipe(network.start.coordinates, i)
    val = bfs(network, starting_point)
    visited_list.append(val)

  return max(visited_list)

network = parse('input.txt')
print(solve_part_1(network))

  