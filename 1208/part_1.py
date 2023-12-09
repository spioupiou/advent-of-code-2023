import re

def parse(file):
  with open(file) as f:
    lines = f.readlines()

  nodes = {}

  for i, line in enumerate(lines):
    if i == 0:
      instructions = line.strip('\n').replace('R', '1').replace('L', '0')
    elif line != "\n":
      matches = re.findall(r'(.+)\s=\s\((.+),\s(.+)\)', line)
      key, value1, value2 = matches[0]
      nodes[key] = (value1, value2)
  return instructions, nodes

def solve_part_1(instructions, nodes):
  steps = 0
  instructions_cp = instructions
  current = nodes['AAA']

  while current != nodes['ZZZ']:
    if len(instructions_cp) == 0:
      instructions_cp = instructions

    if instructions_cp[0] == '0':
      current = nodes[current[0]]
    else:
      current = nodes[current[1]]
    steps += 1
    instructions_cp = instructions_cp[1:]
  return steps

instructions, nodes = parse('test_input.txt')
print(solve_part_1(instructions, nodes))
  