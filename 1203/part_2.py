import re

def parse(file):
  with open(file) as f:
    lines = f.readlines()

  return [line.strip('\n') for line in lines]

def find_gear_neighbours(matrix):
    gears = {}
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)]

    for y, row in enumerate(matrix):
      for x, char in enumerate(row):
         if char == "*":
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(matrix[0]) and 0 <= ny < len(matrix):
                    if (x, y) in gears.keys():
                      gears[(x, y)].append((nx, ny))
                    else:
                      gears[(x, y)] = [(nx, ny)]
    return gears

def solve_part_2(matrix, gear_neighbours):
  digit = ""
  asterisk = ()
  arr = []

  numbers_next_to_gears = {}

  for y, row in enumerate(matrix):
    for x, char in enumerate(row):
      if char.isdigit():
        digit += char
        for gear, neighbours in gear_neighbours.items():
          if (x, y) in neighbours:
            asterisk = gear
      else:
        if digit != "" and asterisk != ():
          try:
            numbers_next_to_gears[asterisk].append(int(digit))
          except KeyError:
            numbers_next_to_gears[asterisk] = [int(digit)]
        digit = ""
        asterisk = ()
        
  products = []
  for gear, adjacent_numbers in numbers_next_to_gears.items():
    if len(adjacent_numbers) == 2:
      products.append(adjacent_numbers[0] * adjacent_numbers[1])
  
  return(sum(products))
 


matrix = parse("input.txt")
gear_neighbours = find_gear_neighbours(matrix)
print(solve_part_2(matrix, gear_neighbours))