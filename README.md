# Lab 5 — Static Code Analysis: Supplier Orders

## Deliverables

- `supplier_orders.py` — revised implementation of the supplier order program.
- `original_supplier_orders.py` — original implementation used for comparison.
- `issues.md` — issue table documenting the findings and fixes.
- `reflection.md` — reflection answers for the lab questions.
- `pylint_report.txt` — Pylint report for the corrected implementation.
- `bandit_report.txt` — Bandit report for the corrected implementation.
- `flake8_report.txt` — Flake8 report for the corrected implementation.
- `smoke_test.txt` — record of the program execution test.

## Requirements

- Python 3.11 or a compatible Python version.
- Pylint
- Bandit
- Flake8

## Run locally

Create and activate a virtual environment.

**Windows Command Prompt:**

```bat
python -m venv venv
venv\Scripts\activate.bat
python -m pip install pylint bandit flake8
```

**Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install pylint bandit flake8
```

## Run the program and static analysis tools

Run the corrected program:

```bash
python supplier_orders.py
```

Run the three analysis tools:

```bash
pylint supplier_orders.py > pylint_report.txt
bandit -r supplier_orders.py > bandit_report.txt 2>&1
flake8 supplier_orders.py > flake8_report.txt
```

To analyze the original implementation for comparison, run:

```bash
pylint original_supplier_orders.py > original_pylint_report.txt
bandit -r original_supplier_orders.py > original_bandit_report.txt 2>&1
flake8 original_supplier_orders.py > original_flake8_report.txt
```

## Verification results

The corrected implementation was executed successfully and checked using all three tools.

- **Pylint:** 10.00/10
- **Bandit:** No issues identified.
- **Flake8:** No violations reported.

The original implementation received a Pylint score of 2.41/10. Bandit reported three findings: one high-severity, one medium-severity, and one low-severity issue. Flake8 reported four violations.

See `issues.md` for the identified issues and corresponding fixes, and `reflection.md` for the lab reflections.

## Note

Static analysis helps identify potential security vulnerabilities and code-quality problems, but clean reports do not guarantee that a program is completely free of defects.
