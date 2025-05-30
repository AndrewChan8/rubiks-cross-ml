from copy import deepcopy

# No-op patterns: These are identity or cancel out
NO_OP_INSERTIONS = [
  ["R", "R'"],
  ["U", "U'"],
  ["F2", "F2"],
  ["L", "L", "L"],  # L L L = L'
  ["D2", "D2"]
]

def insert_no_ops(solution, pattern, position):
  """Insert a no-op move sequence into a copy of the solution at the given position."""
  return solution[:position] + pattern + solution[position:]

def generate_cross_variants(base_solution, scramble, max_variants=4):
  """Generate variants of a cross solution by inserting known-safe no-op move patterns."""
  variants = [base_solution]  # include the original
  attempt = 0
  i = 0
  while len(variants) < max_variants + 1 and attempt < 20:
    new_variant = insert_no_ops(base_solution, NO_OP_INSERTIONS[i % len(NO_OP_INSERTIONS)], (i + 1) % len(base_solution))
    if new_variant not in variants:
      variants.append(new_variant)
    i += 1
    attempt += 1
  return variants
