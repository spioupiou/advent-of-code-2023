import numpy as np

def parse(file):
  with open(file) as f:
    lines = [line.strip('\n') for line in f]
  return [list(line) for line in lines]

#---------Helpers---------
def print_matrix(matrix):
  for row in matrix:
    print(''.join(row))
  print('\n') 

def hash_matrix(matrix):
  return ', '.join([''.join(row) for row in matrix])

def unhash_matrix(matrix_hash):
  matrix = matrix_hash.split(', ')
  matrix = [[*row] for row in matrix]
  return matrix


#----------Tilt-----------
def find_lowest_possible_move(matrix, x, y):
  # Set 'down' to current row
  down = y
  # Check if there is a cube shaped rock ('#') or another round shape rock ('O') underneath current position
  if matrix[down - 1][x] == '#' or matrix[down - 1][x] == 'O':
    # If so, return current row as we cannot move further down
    return down
  # Otherwise, go down until you hit a rock (0 or #)
  else: 
    down = down - 1
    while matrix[down][x] != '#' and matrix[down][x] != 'O':
      # If we reach the bottom of the matrix, break
      if down == 0:
        break
      # If the row below has a rock, break
      if matrix[down-1][x] == '#' or matrix[down-1][x] == 'O':
        break
      # Otherwise, keep going down
      down -= 1
    return down

def find_most_left_possible_move(matrix, x, y):
  # Set 'left' to current column
  left = x
  # Check if there is a 'O' or '#' to the left, if so return the current position
  if matrix[y][left-1] == '#' or matrix[y][left-1] == 'O':
    return left
  else:
    left = left -1
    while matrix[y][left] != '#' and matrix[y][left] != 'O':
    # If we reach the first column, break
      if left == 0:
        break
      if matrix[y][left-1] == '#' or matrix[y][left-1] == 'O':
        break
      left -= 1
    return left

def tilt_north(matrix):
  for y, row in enumerate(matrix):
  # Skip the bottom of the matrix
    if y == 0:
      continue
    for x, char in enumerate(row):
      if char == 'O':
        down = find_lowest_possible_move(matrix, x, y)
        # Swap
        if y != down:
          matrix[y][x], matrix[down][x] = '.', 'O'
  return matrix

def tilt_west(matrix):
  for y, row in enumerate(matrix):
    for x, char in enumerate(row):
      # Skip the first column
      if x == 0:
        continue
      if char == 'O':
        left = find_most_left_possible_move(matrix, x, y)
        # Swap
        if x != left:
          matrix[y][x], matrix[y][left] = '.', 'O'
  return matrix

def tilt_counter_clock_wise(matrix):
  # North
  matrix = tilt_north(matrix)

  # West 
  matrix = tilt_west(matrix)

  # South (reverse the rows in the matrix and use North function)
  matrix = np.flipud(matrix)
  matrix = tilt_north(matrix)
  matrix = np.flipud(matrix)

  # East (reverse each row and use West function)
  matrix = [row[::-1] for row in matrix]
  matrix = tilt_west(matrix)
  matrix = [row[::-1] for row in matrix]

  return matrix


def solve_part_1(matrix):
  north_inclined = tilt_north(matrix)
  total = sum(row.count('O') * i for i, row in enumerate(reversed(north_inclined), 1))
  print(total)

def solve_part_2(matrix):  
  #-------Find cycle------0
  # Keep trace of previous matrixes, to detect the cycle
  history = {}

  # Find the breaking point (where a matrix is the same as a previous one)
  breaking_point = 0
  repeated_cycle = 0
  for i in range(200):
    # One cycle - north west south east
    matrix = tilt_counter_clock_wise(matrix)

    # Hash the matrix and check if there is a corresponding hash in the history dict
    matrix_hash = hash_matrix(matrix)
    if matrix_hash in history.keys():
      breaking_point, repeated_cycle = i+1, history[matrix_hash]
      break
    else:
      history[matrix_hash] = i+1

  cycle_length = breaking_point - repeated_cycle
  cycle_offset = 1_000_000_000 % cycle_length
  while cycle_offset < repeated_cycle:
    cycle_offset += cycle_length

  for matrix_hash, cycle in history.items():
    if cycle == cycle_offset:
      matrix = unhash_matrix(matrix_hash)
      total = sum(row.count('O') * i for i, row in enumerate(reversed(matrix), 1))
      print(total)
      break





matrix = parse('input.txt')
solve_part_1(matrix)
solve_part_2(matrix)

  