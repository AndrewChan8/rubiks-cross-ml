import json
import random
import io
import sys
from pycuber import Cube
from pycuber.solver import CFOPSolver
from generate_cross_variants import generate_cross_variants

# All possible moves
MOVES = ['U', "U'", 'U2', 'D', "D'", 'D2',
         'L', "L'", 'L2', 'R', "R'", 'R2',
         'F', "F'", 'F2', 'B', "B'", 'B2']

def random_scramble(length=20):
  return [random.choice(MOVES) for _ in range(length)]

class CustomCFOPSolver(CFOPSolver):
  def solve_cross_only(self):
    buffer = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = buffer
    try:
      super().solve()
    finally:
      sys.stdout = sys_stdout
    output = buffer.getvalue().strip().splitlines()
    for line in output:
      if line.startswith("Cross:"):
        return line.replace("Cross:", "").strip()
    return None

def generate_dataset(n=100, output_file="cross_dataset.json"):
  dataset = []
  for i in range(n):
    scramble_moves = random_scramble()
    scramble_str = " ".join(scramble_moves)

    cube = Cube()
    cube(scramble_str)

    solver = CustomCFOPSolver(cube)
    cross_str = solver.solve_cross_only()

    if cross_str:
      best_solution = cross_str.split()
      variants = generate_cross_variants(best_solution, scramble_moves)

      group = {
        "group_id": i,
        "scramble": scramble_moves,
        "solutions": []
      }

      for j, moves in enumerate(variants):
        group["solutions"].append({
          "moves": moves,
          "score": len(moves),
          "is_best": j == 0
        })

      dataset.append(group)
      print(f"[{i+1}/{n}] ")
    else:
      print(f"[{i+1}/{n}] No cross solution found")

  with open(output_file, "w") as f:
    json.dump(dataset, f, indent=2)

  print(f"\nSaved {len(dataset)} groups to {output_file}")

if __name__ == "__main__":
  generate_dataset(100)
