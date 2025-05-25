from cube_core import create_solved_cube, FACE_INDEX
from move_parser import apply_moves

def is_white_cross_solved(cube):
  """
  Returns True if white cross is on D face and each white edge is
  aligned with the correct adjacent center color.
  """
  # Define edge positions and expected adjacent face checks
  edges = {
    (0, 1): ('F', 0, 1),  # DF
    (1, 0): ('L', 1, 2),  # DL
    (1, 2): ('R', 1, 0),  # DR
    (2, 1): ('B', 2, 1)   # DB
  }

  for (i, j), (adj_face, ai, aj) in edges.items():
    if cube[FACE_INDEX['D']][i][j] != 'W':
      print(f"[✘] D[{i}][{j}] is {cube[FACE_INDEX['D']][i][j]}, not white.")
      return False

    expected = cube[FACE_INDEX[adj_face]][1][1]  # Center of adjacent face
    actual = cube[FACE_INDEX[adj_face]][ai][aj]
    if actual != expected:
      print(f"[✘] Adjacent to D[{i}][{j}], {adj_face}[{ai}][{aj}] is {actual}, expected {expected}.")
      return False

  return True


def pretty_print(cube):
  def face_str(face):
    return [" ".join(cube[FACE_INDEX[face]][i]) for i in range(3)]

  up = face_str('U')
  left = face_str('L')
  front = face_str('F')
  right = face_str('R')
  back = face_str('B')
  down = face_str('D')

  for row in up:
    print(" " * 10 + row)
  for i in range(3):
    print(f"{left[i]}   {front[i]}   {right[i]}   {back[i]}")
  for row in down:
    print(" " * 10 + row)

if __name__ == "__main__":
  print("=== Test 1: Solved Cube ===")
  cube = create_solved_cube()
  pretty_print(cube)
  if is_white_cross_solved(cube):
    print("✅ Passed\n")
  else:
    print("❌ Failed\n")

  print("=== Test 2: Scrambled Cube (no cross) ===")
  cube = create_solved_cube()
  apply_moves(cube, "R U R' U'")
  pretty_print(cube)
  if not is_white_cross_solved(cube):
    print("✅ Passed\n")
  else:
    print("❌ Failed (should not be solved)\n")
