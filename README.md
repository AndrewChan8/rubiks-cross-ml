# Rubik's Cube Cross Solution Ranking with Machine Learning

## Overview

This project applies machine learning to rank Rubik's Cube cross solutions based on scramble state and proposed solution moves. The goal is to train a model that can score and rank candidate solutions, selecting the most efficient one automatically.

## Project Structure

- `generate_cross_dataset.py`: Generates randomized scrambles, solves the white cross using PyCuber, creates perturbed variants, and stores all in `cross_dataset.json`.
- `generate_cross_variants.py`: Perturbs optimal cross solutions to produce alternative (less optimal) variants.
- `train_model.py`: Trains a single Decision Tree Regressor on the dataset and reports test RMSE and MRR.
- `train_and_compare_models.py`: Trains and compares multiple models (Decision Tree, Ridge Regression, Random Forest) using RMSE and Mean Reciprocal Rank.
- `cross_dataset.json`: The dataset file containing scramble/solution pairs and their scores.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Required packages include:
   - `pycuber`
   - `scikit-learn`
   - `pandas`
   - `numpy`

2. (Optional) Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

## How to Run

1. Generate the dataset:
   ```bash
   python3 generate_cross_dataset.py
   ```

2. Train and evaluate a single model:
   ```bash
   python3 train_model.py
   ```

3. Train and compare multiple models:
   ```bash
   python3 train_and_compare_models.py
   ```

## Output

- `cross_dataset.json`: Contains scramble state, 5 solution variants per scramble, and scores.
- Model performance printed in the console, including RMSE and MRR metrics.

## Notes

- The model scores solutions based on move count, treating shorter solutions as better.
- MRR (Mean Reciprocal Rank) is used to evaluate how well the model ranks the true best solution among the 5 candidates.
