import re

# Pulse is high or low (boolean?)

class Broadcaster:
  def __init__(self, destinations):
    self.destinations = destinations

  def send(self, modules):
    for destination in self.destinations:
      modules[destination].receive(0)

class FlipFlopModule:
  def __init__(self, status):
    self.status = status

  def receive(self, pulse):
    if pulse == 0:
      self.status = not self.status
      self.send()
  
  def send(self):
    if self.status:
      return 1
    else:
      return 0
    
class ConjunctionModule:
  def __init__(self, memory: dict):
    self.memory = memory
  
  def send(self):
    if self.status:
      return 1
    else:
      return 0

def parse(file):
  with open(file) as f:
    lines = [line.strip('\n') for line in f]

    modules = {}
    for line in lines:
      print(line)
      if line.startswith('broadcaster'):
        print("are you working?")
        destinations = re.search(r'->\s(.*)', line).group(1).split(', ')
        modules['broadcaster'] = Broadcaster(destinations)

    return modules

def solve_part_1(workflows, parts):
  return True

modules = parse('test_input.txt')
for module in modules.items():
  print(module)
# print(modules['broadcaster'])