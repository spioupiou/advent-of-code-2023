import re

def parse(file):
  with open(file) as f:
    lines = [line.strip('\n') for line in f]

    matrix = []
    start = (0,0)
    for y, line in enumerate(lines):
      matrix.append(list(line))
      for x, char in enumerate(line):
        if char == 'S':
          start = (x, y)

    return matrix, start

def find_possible_moves(matrix, coordinates: list):
  # Define neighbours
  neighbours = [(0,1), (1,0), (0,-1), (-1,0)]
  possible_moves = set()
  for x, y in coordinates:
    for neighbour in neighbours:
      new_x, new_y = x + neighbour[0], y + neighbour[1]
      if 0 <= new_x < len(matrix[0]) and 0 <= new_y < len(matrix):
        if matrix[new_y][new_x] != '#':
          possible_moves.add((new_x, new_y))

  return possible_moves

def solve_part_1():
  garden, start = parse('input.txt')
  # Start with the starting position
  to_visit = [[start]]

  for i in range(0, 64):
    # Take first set of positions
    last = to_visit.pop(0)

    # Find all possible moves from that set of positions
    possible_moves = find_possible_moves(garden, last)

    # Add all possible moves to the to_visit array
    to_visit.append(possible_moves)

  print(len(possible_moves))

solve_part_1()