import re

def parse(file):
  with open(file) as f:
    lines = [line.strip('\n') for line in f]

    parts = []
    for i in range(len(lines)-1, 0, -1):
      if lines[i] == '':
        break
      values = re.findall(r'(\d+)', lines[i])
      parts.append([int(val) for val in values])

    workflows = {}
    for line in lines:
      if line == '': break
      workflow_name = re.search(r'([a-z]+){', line).group(1)
      conditions = re.findall(r'([x|m|a|s]{1}[>|<]\d+):([a-zA-Z]+)', line)
      else_condition = re.search(r',([a-zA-Z]+)}', line).group(1)
      conditions.append(('else', else_condition))
      workflows[workflow_name] = conditions

    return workflows, parts

def make_workflow(conditions):
  fun_string = 'lambda x, m, a, s: '
  for i, condition in enumerate(conditions):
    if condition[0] == 'else':
      fun_string = fun_string + ' else ' + '"' + condition[1] + '"'
    elif i == 0:
      fun_string = fun_string + '"' + condition[1] + '"' + ' if ' + condition[0]
    else:
      fun_string = fun_string + ' else ' + '"' + condition[1] + '"' + ' if ' + condition[0]
  return eval(fun_string)

def solve_part_1(workflows, parts):
  accepted = []
  for part in parts:
    result = make_workflow(workflows['in'])(*part)
    while result != 'A' and result != 'R':
      result = make_workflow(workflows[result])(*part)
    if result == 'A':
      accepted.extend(part)
  return sum(accepted)

workflows, parts = parse('input.txt')
print(solve_part_1(workflows, parts))