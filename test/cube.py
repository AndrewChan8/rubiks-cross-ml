from cube_core import create_solved_cube
from move_parser import apply_moves
from visualization import print_cube


if __name__ == "__main__":
  cube = create_solved_cube()
  apply_moves(cube, "R U R' U'")
  print_cube(cube)
