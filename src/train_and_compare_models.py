import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error

# Load and parse data 
with open("cross_dataset.json", "r") as f:
  raw = json.load(f)

# Flatten JSON structure 
def is_valid_solution(val):
  return isinstance(val, list) and all(isinstance(m, str) for m in val)

rows = []
for entry in raw:
  group_id = entry.get("group_id", -1)
  scramble = entry.get("scramble", [])
  for sol in entry.get("solutions", []):
    rows.append({
      "group_id": group_id,
      "scramble": scramble,
      "solution": sol["moves"],
      "score": sol["score"],
      "is_best": sol["is_best"]
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

X = np.array([s + a for s, a in zip(df["scramble_encoded"], df["solution_encoded"])])
y = df["score"].values

# Split data 
X_trainval, X_test, y_trainval, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train, X_dev, y_train, y_dev = train_test_split(X_trainval, y_trainval, test_size=0.25, random_state=42)

# Decision Tree Model 
print("\nDecision Tree Regressor")
best_depth = None
best_rmse = float("inf")

for depth in [2, 4, 6, 8, 10]:
  model = DecisionTreeRegressor(max_depth=depth)
  model.fit(X_train, y_train)
  pred = model.predict(X_dev)
  rmse = root_mean_squared_error(y_dev, pred)
  print(f"  max_depth={depth} → Dev RMSE: {rmse:.3f}")
  if rmse < best_rmse:
    best_rmse = rmse
    best_depth = depth

final_dt = DecisionTreeRegressor(max_depth=best_depth)
final_dt.fit(X_trainval, y_trainval)
dt_pred = final_dt.predict(X_test)

# Ridge Regression Model 
print("\nRidge Regression")
best_alpha = None
best_rmse = float("inf")

for alpha in [0.01, 0.1, 1, 10, 100]:
  model = Ridge(alpha=alpha)
  model.fit(X_train, y_train)
  pred = model.predict(X_dev)
  rmse = root_mean_squared_error(y_dev, pred)
  print(f"  alpha={alpha} → Dev RMSE: {rmse:.3f}")
  if rmse < best_rmse:
    best_rmse = rmse
    best_alpha = alpha

final_ridge = Ridge(alpha=best_alpha)
final_ridge.fit(X_trainval, y_trainval)
ridge_pred = final_ridge.predict(X_test)

# Random Forest Regressor 
print("\nRandom Forest Regressor")
best_estimators = None
best_rmse = float("inf")

for est in [10, 50, 100, 200]:
  model = RandomForestRegressor(n_estimators=est, random_state=42)
  model.fit(X_train, y_train)
  pred = model.predict(X_dev)
  rmse = root_mean_squared_error(y_dev, pred)
  print(f"  n_estimators={est} → Dev RMSE: {rmse:.3f}")
  if rmse < best_rmse:
    best_rmse = rmse
    best_estimators = est

final_rf = RandomForestRegressor(n_estimators=best_estimators, random_state=42)
final_rf.fit(X_trainval, y_trainval)
rf_pred = final_rf.predict(X_test)

# Evaluation 
def mean_reciprocal_rank(grouped_preds, grouped_truths):
  reciprocal_ranks = []
  for preds, truths in zip(grouped_preds, grouped_truths):
    sorted_indices = np.argsort(preds)
    true_best_index = np.argmin(truths)
    rank = np.where(sorted_indices == true_best_index)[0][0] + 1
    reciprocal_ranks.append(1 / rank)
  return np.mean(reciprocal_ranks)

def evaluate_model(name, preds):
  rmse = root_mean_squared_error(y_test, preds)
  grouped_preds = [preds[i:i+5] for i in range(0, len(preds), 5)]
  grouped_truths = [y_test[i:i+5] for i in range(0, len(y_test), 5)]
  if all(len(g) == 5 for g in grouped_preds):
    mrr = mean_reciprocal_rank(grouped_preds, grouped_truths)
    print(f"{name} → Test RMSE: {rmse:.3f}, MRR: {mrr:.3f}")
  else:
    print(f"{name} → Test RMSE: {rmse:.3f}, MRR skipped (uneven groups)")

print("\nFinal Model Evaluation:")
evaluate_model("Decision Tree", dt_pred)
evaluate_model("Ridge Regression", ridge_pred)
evaluate_model("Random Forest", rf_pred)
