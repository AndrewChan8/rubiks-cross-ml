import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import root_mean_squared_error

# Load and parse data 
with open("cross_dataset.json", "r") as f:
  raw = json.load(f)

# Flatten into rows 
def is_valid_solution(sol):
  return isinstance(sol, dict) and "moves" in sol

rows = []
for entry in raw:
  group_id = entry.get("group_id", -1)
  scramble = entry.get("scramble", [])
  for solution in entry.get("solutions", []):
    if is_valid_solution(solution):
      rows.append({
        "group_id": group_id,
        "scramble": scramble,
        "solution": solution["moves"],
        "score": solution["score"],
        "is_best": solution.get("is_best", False)
      })

df = pd.DataFrame(rows)

# Feature encoding
def encode_moves(move_list, max_len=20):
  move_dict = {move: idx for idx, move in enumerate([
    'U', "U'", "U2", 'D', "D'", "D2",
    'L', "L'", "L2", 'R', "R'", "R2",
    'F', "F'", "F2", 'B', "B'", "B2"
  ])}
  encoded = [move_dict.get(m, 0) for m in move_list]
  return encoded[:max_len] + [0] * (max_len - len(encoded))

df["scramble_encoded"] = df["scramble"].apply(lambda x: encode_moves(x, max_len=20))
df["solution_encoded"] = df["solution"].apply(lambda x: encode_moves(x, max_len=12))

X = np.array([s + sol for s, sol in zip(df["scramble_encoded"], df["solution_encoded"])])
y = df["score"].values

# Train/dev/test split 
X_trainval, X_test, y_trainval, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train, X_dev, y_train, y_dev = train_test_split(X_trainval, y_trainval, test_size=0.25, random_state=42)

# Hyperparameter tuning 
best_depth = None
best_rmse = float("inf")

print("Tuning Decision Tree max_depth:")
for depth in [2, 4, 6, 8, 10]:
  model = DecisionTreeRegressor(max_depth=depth)
  model.fit(X_train, y_train)
  y_pred = model.predict(X_dev)
  rmse = root_mean_squared_error(y_dev, y_pred)
  print(f"  max_depth={depth} → Dev RMSE: {rmse:.3f}")
  if rmse < best_rmse:
    best_rmse = rmse
    best_depth = depth

# Retrain and evaluate
print(f"\nRetraining with best max_depth={best_depth}")
final_model = DecisionTreeRegressor(max_depth=best_depth)
final_model.fit(X_trainval, y_trainval)
y_final_pred = final_model.predict(X_test)
final_rmse = root_mean_squared_error(y_test, y_final_pred)
print(f"Test RMSE: {final_rmse:.3f}")

# Mean Reciprocal Rank (MRR) 
def mean_reciprocal_rank(grouped_preds, grouped_truths):
  reciprocal_ranks = []
  for preds, truths in zip(grouped_preds, grouped_truths):
    sorted_indices = np.argsort(preds)
    true_best_index = np.argmin(truths)
    rank = np.where(sorted_indices == true_best_index)[0][0] + 1
    reciprocal_ranks.append(1 / rank)
  return np.mean(reciprocal_ranks)

grouped_preds = []
grouped_truths = []
for i in range(0, len(y_test), 5):
  grouped_preds.append(y_final_pred[i:i+5])
  grouped_truths.append(y_test[i:i+5])

if all(len(group) == 5 for group in grouped_preds):
  mrr = mean_reciprocal_rank(grouped_preds, grouped_truths)
  print(f"Test Mean Reciprocal Rank (MRR): {mrr:.3f}")
else:
  print("Skipping MRR: not all groups have 5 candidates.")
