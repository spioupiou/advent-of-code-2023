import re

def parse(file):
  with open(file) as f:
    lines = [line.strip('\n') for line in f]
  return [list(line) for line in lines]

def find_lowest_possible_move(matrix, x, y):
  # Set current row
  current = y
  # Check if there is a cube shaped rock ('#') or another round shape rock ('O') underneath current position
  if matrix[current - 1][x] == '#' or matrix[current - 1][x] == 'O':
    # If so, return current as we cannot move further down
    return current
  # Otherwise, go down until you hit a rock (0 or #)
  else: 
    down = current - 1
    while matrix[down][x] != '#' and matrix[down][x] != 'O':
      # If we hit the bottom of the matrix, break
      if down == 0:
        break
      # If the row below has a rock, break
      if matrix[down-1][x] == '#' or matrix[down-1][x] == 'O':
        break
      # Otherwise, keep going down
      down -= 1
    return down

def solve_part_1(matrix):
  for y, row in enumerate(matrix):
    # Skip the bottom of the matrix
    if y == 0:
      continue
    for x, char in enumerate(row):
      if char == 'O':
        down = find_lowest_possible_move(matrix, x, y)
        if y != down:
          matrix[y][x], matrix[down][x] = '.', 'O'
        
  total = sum(row.count('O') * i for i, row in enumerate(reversed(matrix), 1))
  print(total)

matrix = parse('input.txt')
solve_part_1(matrix)


  