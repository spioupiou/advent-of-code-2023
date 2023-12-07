import re
from itertools import chain

class Converter:
  def __init__(self, id, rules):
    self.id = id
    self.rules = rules

  def transform(self, seed):
    overlaps = []
    shifted = []
    for rule in self.rules:
      rule_range = range(rule[1], rule[1]+rule[2])
      overlap = range(max(rule_range.start,seed.start), min(rule_range.stop,seed.stop)) or None

      if overlap != None: 
        shifted.append(range(seed.start - rule[1] + rule[0], seed.stop - rule[1] + rule[0]))
        overlaps.append(overlap)

    overlaps = sorted(overlaps, key=lambda x: x.start)
    flat = chain((seed.start-1,), chain.from_iterable(overlaps), (seed.stop+1,))
    gaps = [range(x+1, y-1) for x, y in zip(flat, flat) if x+1 < y]

    for gap in gaps:
      if gap.start != gap.stop:
        shifted.append(gap)

    return shifted


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
      seeds = []
      seeds_str = [int(i) for i in re.findall("\d+", str)]
      for i in range(0, len(seeds_str) -1, 2):
        seeds.append(range(seeds_str[i], seeds_str[i]+seeds_str[i+1]))
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
  arr = []
  for seed in seeds:
    results = [seed]
    for i, converter in enumerate(converters):
      print(i, end = " ")
      # if i == 1: break
      transformed_ranges = []
      for result in results:
        transformed = converter.transform(result)
        transformed_ranges.extend(transformed)
      results = transformed_ranges
      print(results, end = "")
    arr.append(results)
  print(arr)
  # return min(arr)

seeds, converters = parse("test_input.txt")
solve_part_1(seeds, converters)
