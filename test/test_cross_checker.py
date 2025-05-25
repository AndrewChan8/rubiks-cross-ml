from cube_core import create_solved_cube
from move_parser import apply_moves
from cross_checker import is_white_cross_solved
from visualization import print_cube

def test_cross_solved():
  print("=== Test 1: Solved Cube ===")
  cube = create_solved_cube()
  print_cube(cube)
  result = is_white_cross_solved(cube)
  print("✅ Passed" if result else "❌ Failed", "\n")

def test_cross_2():
  print("=== Test 2: Scrambled Cube (yes cross) ===")
  cube = create_solved_cube()
  apply_moves(cube, "R U R' U'")
  print_cube(cube)
  result = is_white_cross_solved(cube)
  print("✅ Passed" if result else "❌ Failed", "\n")

def test_cross_scrambled():
  print("=== Test 3: Scrambled Cube (no cross) ===")
  cube = create_solved_cube()
  apply_moves(cube, "D")
  print_cube(cube)
  result = is_white_cross_solved(cube)
  print("❌ Failed" if result else "✅ Passed", "\n")

def test_cross_3():
  print("=== Test 3: Scrambled Cube (no cross) ===")
  cube = create_solved_cube()
  apply_moves(cube, "D R U R' U' D'")
  print_cube(cube)
  result = is_white_cross_solved(cube)
  print("❌ Failed" if result else "✅ Passed", "\n")


if __name__ == "__main__":
  test_cross_solved()
  test_cross_2()
  test_cross_scrambled()
  test_cross_3()