import numpy as np

# Define face colors
FACE_COLORS = {
  'U': 'Y',  # White
  'D': 'W',  # Yellow
  'F': 'G',  # Green
  'B': 'B',  # Blue
  'L': 'R',  # Orange
  'R': 'O'   # Red
}

# Face index mapping
FACE_INDEX = {
  'U': 0,
  'D': 1,
  'F': 2,
  'B': 3,
  'L': 4,
  'R': 5
}

def rotate_face_cw(face):
  return np.rot90(face, k=-1)

def create_solved_cube():
  return np.array([[[color] * 3 for _ in range(3)] for color in FACE_COLORS.values()])

def rotate_U(cube):
  cube[FACE_INDEX['U']] = rotate_face_cw(cube[FACE_INDEX['U']])
  F, R, B, L = FACE_INDEX['F'], FACE_INDEX['R'], FACE_INDEX['B'], FACE_INDEX['L']
  cube[F, 0], cube[R, 0], cube[B, 0], cube[L, 0] = \
    cube[R, 0].copy(), cube[B, 0].copy(), cube[L, 0].copy(), cube[F, 0].copy()

def rotate_D(cube):
  cube[FACE_INDEX['D']] = rotate_face_cw(cube[FACE_INDEX['D']])
  F, L, B, R = FACE_INDEX['F'], FACE_INDEX['L'], FACE_INDEX['B'], FACE_INDEX['R']
  cube[F, 2], cube[L, 2], cube[B, 2], cube[R, 2] = \
    cube[L, 2].copy(), cube[B, 2].copy(), cube[R, 2].copy(), cube[F, 2].copy()

def rotate_F(cube):
  cube[FACE_INDEX['F']] = rotate_face_cw(cube[FACE_INDEX['F']])
  U, R, D, L = FACE_INDEX['U'], FACE_INDEX['R'], FACE_INDEX['D'], FACE_INDEX['L']
  top = cube[U, 2].copy()
  cube[U, 2] = np.flip(cube[L, :, 2])
  cube[L, :, 2] = cube[D, 0]
  cube[D, 0] = np.flip(cube[R, :, 0])
  cube[R, :, 0] = top

def rotate_B(cube):
  cube[FACE_INDEX['B']] = rotate_face_cw(cube[FACE_INDEX['B']])
  U, L, D, R = FACE_INDEX['U'], FACE_INDEX['L'], FACE_INDEX['D'], FACE_INDEX['R']
  top = cube[U, 0].copy()
  cube[U, 0] = cube[R, :, 2]
  cube[R, :, 2] = np.flip(cube[D, 2])
  cube[D, 2] = cube[L, :, 0]
  cube[L, :, 0] = np.flip(top)

def rotate_L(cube):
  cube[FACE_INDEX['L']] = rotate_face_cw(cube[FACE_INDEX['L']])
  U, F, D, B = FACE_INDEX['U'], FACE_INDEX['F'], FACE_INDEX['D'], FACE_INDEX['B']
  col = cube[U, :, 0].copy()
  cube[U, :, 0] = cube[B, ::-1, 2]
  cube[B, ::-1, 2] = cube[D, :, 0]
  cube[D, :, 0] = cube[F, :, 0]
  cube[F, :, 0] = col

def rotate_R(cube):
  cube[FACE_INDEX['R']] = rotate_face_cw(cube[FACE_INDEX['R']])
  U, B, D, F = FACE_INDEX['U'], FACE_INDEX['B'], FACE_INDEX['D'], FACE_INDEX['F']
  col = cube[U, :, 2].copy()
  cube[U, :, 2] = cube[F, :, 2]
  cube[F, :, 2] = cube[D, :, 2]
  cube[D, :, 2] = cube[B, ::-1, 0]
  cube[B, ::-1, 0] = col
