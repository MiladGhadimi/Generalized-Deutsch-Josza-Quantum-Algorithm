# Generalized-Deutsch-Josza-Quantum-Algorithm
Generalized Deutsch-Josza Quantum Algorithm
# Generalized Deutsch–Josza Quantum Algorithm

This repository contains the code used in the article:

> **Generalized Deutsch–Jozsa Algorithm for Applications in Data Classification, Logistic Regression, and Quantum Key Distribution**  
> Milad Ghadimi et al., 2025.

The code implements the generalized Deutsch–Jozsa (GDJ) algorithm and the numerical experiments reported in the paper, including data classification, logistic regression, and quantum key distribution scenarios.

---

## Repository structure

- `src/`  
  Core implementation of the generalized Deutsch–Jozsa algorithm and helper functions.

- `experiments/`  
  Scripts or notebooks for running the experiments reported in the paper (classification, logistic regression, QKD, etc.).

- `figures/`  
  (Optional) Scripts or notebooks used to generate the figures in the manuscript.

- `requirements.txt`  
  Python dependencies required to run the code.

- `README.md`  
  This file.

*(Adapt the folder names to match your actual structure — e.g. `notebooks/`, `gdj/`, etc.)*

---

## Requirements

- Python 3.x
- [Qiskit](https://qiskit.org/) (or other frameworks you actually use)
- NumPy
- SciPy
- Matplotlib

Install dependencies with:

```bash
pip install -r requirements.txt

