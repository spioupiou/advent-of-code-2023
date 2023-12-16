import re

def parse(file):
  with open(file) as f:
    lines = [line.strip('\n') for line in f]
  return lines[0].split(',')

def hash_word(word):
  current_val = 0
  for char in word:
    current_val += ord(char)
    current_val *= 17
    current_val %= 256
  return current_val

def solve_part_1(sequence):
  total = 0
  for word in sequence:
    total += hash_word(word)
  print(total)

def insert_in_box(boxes, word):
  matches = re.match(r'([a-z]+)(\-|=)(\d?)', word)
  label = matches.group(1)
  box_num = hash_word(label)
  operation = matches.group(2)
  if operation == '-':
    if label in boxes[box_num]:
      boxes[box_num].pop(label)
  else:
    boxes[box_num][label] = int(matches.group(3))

def calculate_focusing_power(boxes):
  total = 0
  for i, box in enumerate(boxes):
    box_num = i + 1
    slot_num = 0
    for focal_length in box.values():
      slot_num += 1
      total += box_num * focal_length * slot_num
  return(total)

def solve_part_2(sequence):
  boxes = [{} for i in range(0, 256)]
  for word in sequence:
    insert_in_box(boxes, word)
  print(calculate_focusing_power(boxes))

sequence = parse('input.txt')
solve_part_1(sequence)
solve_part_2(sequence)

