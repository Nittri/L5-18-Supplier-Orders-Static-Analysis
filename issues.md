# Static Code Analysis — Supplier Orders

## 1. Objective

The original `original_supplier_orders.py` program was analyzed using Pylint, Bandit, and Flake8. The identified issues were prioritized by security risk and code quality. The corrected implementation is provided in `supplier_orders.py`.

## 2. Original Analysis Results

| Tool | Result |
|---|---|
| Pylint | 2.41/10 |
| Bandit | 3 potential issues: 1 High, 1 Medium, 1 Low |
| Flake8 | 4 reported violations |

## 3. Issues Identified and Fixes Applied

| No. | Issue | Severity | Evidence | Fix applied |
|---|---|---|---|---|
| 1 | Potential command injection | High | Bandit B605, line 21: `os.system("echo notifying warehouse about " + supplier)` | Replaced shell command execution with structured logging. Supplier input is no longer concatenated into a shell command. |
| 2 | Potential SQL injection | Medium | Bandit B608, line 11: SQL query constructed using `%` string formatting | Replaced string-built SQL with parameterized SQL queries. |
| 3 | Exceptions silently ignored | Low | Bandit B110, lines 27–28: `except Exception: pass` | Replaced the silent, broad exception handler with specific database exception handling and logging. |
| 4 | Global mutable state | Code quality | Pylint W0603: use of the `global` statement for `order_total` | Removed the global counter and used a more maintainable approach to track order information. |
| 5 | Poor function and variable naming | Code quality | Pylint C0103: names such as `placeOrder`, `markReceived`, `notifyWarehouse`, and `pendingCount` | Renamed functions to snake_case and followed appropriate naming conventions. |
| 6 | Missing documentation | Code quality | Pylint C0114 and C0116: missing module and function docstrings | Added module and function docstrings. |
| 7 | Long lines and formatting errors | Style | Pylint C0301 and Flake8 E501/E225 | Wrapped long statements and corrected whitespace around operators. |
| 8 | Unused function argument | Code quality | Pylint W0613: unused `remarks` argument in `markReceived` | Reviewed the function interface and revised the implementation to avoid an unused argument. |
| 9 | Broad exception handling | Code quality | Pylint W0718: catching the general `Exception` type | Narrowed exception handling to the relevant database errors. |

## 4. Corrected Implementation

The corrected program is available in `supplier_orders.py`. The changes improve security, readability, error reporting, and maintainability while retaining the supplier-order workflow.

The implementation uses parameterized SQL queries, input validation, structured logging, specific database exception handling, and a main-entry-point guard.

## 5. Final Tool Results

| Tool | Result after correction |
|---|---|
| Pylint | 10.00/10 |
| Bandit | No issues identified |
| Flake8 | No violations reported |
| Execution test | Program executed successfully and printed the expected workflow messages |

## 6. Conclusion

The analysis identified security risks and maintainability problems in the original program. The most important fixes addressed potential command injection and SQL injection. Exception handling was also improved so that failures are not silently discarded. Naming, documentation, and formatting improvements made the program easier to understand and maintain.

After correction, the program achieved a Pylint score of 10/10, Bandit reported zero issues, and Flake8 reported no violations. These results indicate that the identified static-analysis findings were addressed; they do not guarantee that the program is free of every possible vulnerability.
