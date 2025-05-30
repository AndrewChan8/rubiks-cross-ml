import io
import sys
from pycuber import Cube
from pycuber.solver import CFOPSolver

class CustomCFOPSolver(CFOPSolver):
  def solve_cross_only(self):
    # Capture printed output from super().solve()
    buffer = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = buffer
    try:
      super().solve()
    finally:
      sys.stdout = sys_stdout

    # Get all printed lines
    output = buffer.getvalue().strip().splitlines()
    for line in output:
      if line.startswith("Cross:"):
        return line.replace("Cross:", "").strip()
    return None  # Fallback if not found

# Example usage
cube = Cube()
scramble = "U D' R2 F2 U R2 U' L2 B2 D B2 F' D2 F' R' D' B2 U2 B2 R2"
cube(scramble)

solver = CustomCFOPSolver(cube)
cross_moves = solver.solve_cross_only()
print("Cross solution:", cross_moves)
