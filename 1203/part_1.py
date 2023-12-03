def parse(file):
  with open(file) as f:
    lines = f.readlines()
  return [line.strip('\n') for line in lines]
 
def is_symbol_adjacent(matrix, coordinates):
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)]
    for dx, dy in directions:
        nx, ny = coordinates[0] + dx, coordinates[1] + dy
        if 0 <= nx < len(matrix[0]) and 0 <= ny < len(matrix):
            if matrix[ny][nx] != "." and not matrix[ny][nx].isalnum():
                return True
    return False

def find_part_numbers(matrix):
  number = ""
  is_adjacent = False
  part_numbers = []

  for y, row in enumerate(matrix):
    for x, char in enumerate(row):
      if char.isdigit():
        number += char
        if is_symbol_adjacent(matrix, (x, y)):
          is_adjacent = True
      else:
        if number != "" and is_adjacent:
          part_numbers.append(int(number))
        number = ""
        is_adjacent = False

  return part_numbers
      
matrix = parse("input.txt")
part_numbers = find_part_numbers(matrix)
print(sum(part_numbers))