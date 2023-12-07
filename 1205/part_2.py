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
        start_bound = seed.start if seed.start in overlap else overlap.start
        end_bound = seed.stop if seed.stop in overlap else overlap.stop
        shifted1 = start_bound - rule[1] + rule[0]  
        shifted2 = end_bound - rule[1] + rule[0]
        shifted.append(range(min([shifted1, shifted2]), max([shifted1, shifted2]))) 
        print("shifted: ", range(start_bound, end_bound), shifted[-1], end = " ")
        overlaps.append(overlap)


    overlaps = sorted((x.start, x.stop) for x in overlaps)
    print("overlaps: ", overlaps, end = " ")
    gaps = []
    if not overlaps:
      # If no overlaps (no matching rules) then use seed as is
      gaps = [seed]
    else:
      # Add the first gap if it exists
      if seed.start < overlaps[0][0]:
          gaps.append(range(seed.start, overlaps[0][0] - 1))
      # Add gaps between overlaps
      for i in range(len(overlaps) - 1):
          if overlaps[i][1] < overlaps[i+1][0]:
              gaps.append(range(overlaps[i][1] + 1, overlaps[i+1][0] - 1))
      # Add the last gap if it exists
      if seed.stop > overlaps[-1][1]:
          gaps.append(range(overlaps[-1][1] + 1, seed.stop))
    print("gaps:", gaps)
    shifted.extend([gap for gap in gaps])

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


def solve_part_2(seeds, converters):
  arr = []
  for i, seed in enumerate(seeds):
    results = [seed]
    for i, converter in enumerate(converters):
      print("converter ", i + 1, end = " - ")
      transformed_ranges = []
      for result in results:
        transformed = converter.transform(result)
        transformed_ranges.extend(transformed)
      results = transformed_ranges
      print("result: ", results)
    arr.extend(results)
  # return min(arr)

  print("RESULTS: ")
  print(arr)
  arr2 = []
  for result in arr:
    arr2.append(result.start)

  print(min(arr2))

seeds, converters = parse("input.txt")
solve_part_2(seeds, converters)
