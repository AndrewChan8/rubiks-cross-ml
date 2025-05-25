from cube_core import (
  rotate_U, rotate_D, rotate_F, rotate_B, rotate_L, rotate_R
)

MOVE_FUNCS = {
  'U': rotate_U,
  'D': rotate_D,
  'F': rotate_F,
  'B': rotate_B,
  'L': rotate_L,
  'R': rotate_R
}

def apply_moves(cube, move_str):
  """
  Applies a sequence of moves to the cube.
  Example: "R U R' U'" or "F2 D L'"
  """
  tokens = move_str.strip().split()
  for token in tokens:
    if not token:
      continue
    move = token[0]
    suffix = token[1:] if len(token) > 1 else ""

    if move not in MOVE_FUNCS:
      raise ValueError(f"Invalid move: {move}")

    times = 1
    if suffix == "'":
      times = 3  # one counter-clockwise = 3 clockwise
    elif suffix == "2":
      times = 2
    elif suffix:
      raise ValueError(f"Invalid move suffix: {suffix}")

    for _ in range(times):
      MOVE_FUNCS[move](cube)
