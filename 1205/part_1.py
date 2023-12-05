import re

class Converter:
  def __init__(self, id, rules):
    self.id = id
    self.rules = rules

  def transform(self, seed):
    for rule in self.rules:
      if seed in range(rule[1], rule[1]+rule[2]):
        diff = seed - rule[1]
        return diff + rule[0]
    return seed


def parse(file):
  converters = []
  converter_ids = {
    "seed-to-soil": 0,
    "soil-to-fertilizer": 1,
    "fertilizer-to-water": 2,
    "water-to-light": 3,
    "light-to-temperature": 4,
    "temperature-to-humidity": 5,
    "humidity-to-location": 6,
  }

  with open(file) as f:
    lines = f.readlines()
  for i, line in enumerate(lines):
    str = line.strip("\n")
    if str.startswith("seeds: "):
      seeds = [int(i) for i in re.findall("\d+", str)]
    else:
      for key, id in converter_ids.items():
        if str.startswith(key):
          converter_rules = []
          index = i + 1
          while index < len(lines) and lines[index] != "\n":
              rule = [int(i) for i in re.findall("\d+", lines[index])]
              converter_rules.append(rule)
              index += 1
          converters.append(Converter(id, converter_rules))
          break

  return seeds, converters


def solve_part_1(seeds, converters):
  arr =[]
  for seed in seeds:
    result = seed
    for converter in converters:
      result = converter.transform(result)
    arr.append(result)

  return min(arr)

seeds, converters = parse("input.txt")
print(solve_part_1(seeds, converters))
