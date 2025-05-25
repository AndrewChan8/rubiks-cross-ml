from colorama import Fore, Style
from cube_core import FACE_INDEX

COLOR_MAP = {
  'W': Fore.WHITE,
  'Y': Fore.YELLOW,
  'G': Fore.GREEN,
  'B': Fore.BLUE,
  'O': Fore.MAGENTA,
  'R': Fore.RED
}

def colored(facelet):
  return COLOR_MAP.get(facelet, "") + f" {facelet} " + Style.RESET_ALL  # fixed width

def print_cube(cube):
  def row(face, r):
    return "".join(colored(cube[FACE_INDEX[face]][r][c]) for c in range(3))

  # U face (top)
  for r in range(3):
    print(" " * 9 + row('U', r))

  # Middle layer: L F R B
  for r in range(3):
    print("".join(row(f, r) for f in ['L', 'F', 'R', 'B']))

  # D face (bottom)
  for r in range(3):
    print(" " * 9 + row('D', r))
