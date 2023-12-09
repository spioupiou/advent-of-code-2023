import re
from math import gcd

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

def find_starting_nodes(nodes):
  starting_nodes = []
  for key, _ in nodes.items():
    if key.endswith('A'):
      starting_nodes.append(nodes[key])
  return starting_nodes


def solve_part_2(instructions, nodes):
  startings = find_starting_nodes(nodes)
  print(startings)
  total_steps = []


  for start in startings:
    instructions_cp = instructions
    steps = 0
    if instructions_cp[0] == '0':
      current = start[0]
    else:
      current = start[1]
    steps += 1
    instructions_cp = instructions_cp[1:]  
    print(current)  
    while not current.endswith('Z'):
      if len(instructions_cp) == 0:
        instructions_cp = instructions

      if instructions_cp[0] == '0':
        current = nodes[current][0]
      else:
        current = nodes[current][1]

      steps += 1
      instructions_cp = instructions_cp[1:]
    total_steps.append(steps)
    steps = 0
  
  lcm = 1
  for i in total_steps:
      lcm = lcm*i//gcd(lcm, i)
  return lcm

instructions, nodes = parse('input.txt')
print(solve_part_2(instructions, nodes))
  