import re

class Pulse:
  def __init__(self, origin, value, destination):
    self.origin = origin
    self.value = value
    self.destination = destination

class Broadcaster:
  def __init__(self, destinations):
    self.destinations = destinations

  def receive(self, pulse: Pulse):
    self.send(pulse)

  def send(self, pulse):
    for destination in self.destinations:
      pulses.append(Pulse(pulse.destination, pulse.value, destination))

class FlipFlopModule:
  def __init__(self, status, destinations):
    self.status = status
    self.destinations = destinations

  def receive(self, pulse: Pulse):
    if pulse.value == 0:
      self.status = not self.status
      self.send(pulse)
  
  def send(self, pulse: Pulse):
    if self.status:
      for destination in self.destinations:
        pulses.append(Pulse(pulse.destination, 1, destination))
    else:
      for destination in self.destinations:
        pulses.append(Pulse(pulse.destination, 0, destination))
    
class ConjunctionModule:
  def __init__(self, memory: dict, destinations):
    self.memory = memory
    self.destinations = destinations

  def receive(self, pulse: Pulse):
    self.memory[pulse.origin] = pulse.value
    self.send(pulse)
  
  def send(self, pulse: Pulse):
    if all(value == 1 for value in self.memory.values()):
      for destination in self.destinations:
        pulses.append(Pulse(pulse.destination, 0, destination))
    else:
      for destination in self.destinations:
        pulses.append(Pulse(pulse.destination, 1, destination))

def parse(file):
  with open(file) as f:
    lines = [line.strip('\n') for line in f]

    modules = {}
    for line in lines:
      if line.startswith('broadcaster'):
        destinations = re.search(r'->\s(.*)', line).group(1).split(', ')
        modules['broadcaster'] = Broadcaster(destinations)
      elif line.startswith('%'):
        matches = re.search(r'%([a-zA-Z]+)\s->\s(.*)', line)
        modules[matches.group(1)] = FlipFlopModule(False, matches.group(2).split(', '))
      elif line.startswith('&'):
        matches = re.search(r'&([a-zA-Z]+)\s->\s(.*)', line)
        modules[matches.group(1)] = ConjunctionModule({}, matches.group(2).split(', '))
    return modules

modules = parse('input.txt')
# Initialize all the conjunction modules
for name, module in modules.items():
  destinations = module.destinations
  for destination in destinations:
    if destination in modules and type(modules[destination]) == ConjunctionModule:
      modules[destination].memory[name] = 0

processed = []

for i in range(0, 1000):
  pulses = [Pulse('button', 0, 'broadcaster')]
  while pulses != []:
    pulse = pulses.pop(0)
    processed.append(pulse)
    if pulse.destination in modules:
      modules[pulse.destination].receive(pulse)

high_count = 0
low_count = 0
for proc in processed:
  if proc.value == 1:
    high_count += 1
  else:
    low_count += 1

print(high_count, low_count, high_count * low_count)