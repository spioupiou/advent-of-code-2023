import re

RED = 12
GREEN = 13
BLUE = 14

def parse(file):
  with open(file) as f:
    lines = f.readlines()

  all_games = []
  for i, line in enumerate(lines):
    line = line.strip('\n')
    number_of_cubes = re.findall(r'(\d+)\s(blue|red|green)', line)
    game = []
    for cube in number_of_cubes:
      game.append((int(cube[0]), cube[1]))
    all_games.append(game)

  return all_games

def solve_part_1(game_list):
  impossible_games = []
  for i, game in enumerate(game_list):
    for cube in game:
      match cube[1]:
        case 'blue':
          if cube[0] > BLUE:
            impossible_games.append(i+1)
            break
        case 'red':
          if cube[0] > RED:
            impossible_games.append(i+1)
            break
        case 'green':
          if cube[0] > GREEN:
            impossible_games.append(i+1)
            break
  return sum([i for i in range(1, len(game_list)+1) if i not in impossible_games])

def solve_part_2(game_list):
  powers = []
  for game in game_list:
    max_red = (0, 'red')
    max_blue = (0, 'blue')
    max_green = (0, 'green')
    for cube in game:
      match cube[1]:
        case 'blue':
          if cube[0] > max_blue[0]:
            max_blue = cube
        case 'red':
          if cube[0] > max_red[0]:
            max_red = cube
        case 'green':
          if cube[0] > max_green[0]:
            max_green = cube
    powers.append(max_red[0] * max_blue[0] * max_green[0])
  return(sum(powers))

games = parse('input.txt')
print(solve_part_1(games))
print(solve_part_2(games))

