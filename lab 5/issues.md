# Static Code Analysis Issues

The following issues were identified from the Bandit, Flake8, and Pylint reports, along with functional issues observed in `theater_system.py`.

| Tool / Code | Issue Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Pylint W0102 | Bug / Design | 9 | `system_logs=[]` is a mutable default argument and is shared across function calls. | Change the default to `None`, then initialize `system_logs = []` inside the function. |
| Bandit B110 / Flake8 E722 / Pylint W0702 | Exception Handling | 21 | A bare `except` catches every exception and silently ignores errors. | Catch a specific exception, such as `ValueError`, and log or handle it properly. |
| Bandit B324 | Security | 25 | MD5 is a weak hashing algorithm and should not be used for security-sensitive values. | Use `hashlib.sha256()` or `secrets.token_hex()` to generate ticket codes. |
| Bandit B103 | Security | 55 | File permissions are set to `777`, allowing everyone to read, write, and execute the file. | Use more restrictive permissions, such as `0o600`, or remove the `chmod` call. |
| Pylint C0114 | Documentation | 1 | The module does not contain a module-level docstring. | Add a descriptive docstring at the beginning of the file. |
| Pylint C0116 | Documentation | 9, 18, 24, 27, 31, 37, 42 | Functions do not have docstrings explaining their purpose. | Add a short docstring to every function. |
| Flake8 E302 | Formatting | 9, 18, 24, 27, 31, 37, 42 | Functions do not have the required two blank lines before their definitions. | Add two blank lines between top-level functions. |
| Flake8 E305 | Formatting | 57 | The file does not contain two blank lines after the final function definition. | Add two blank lines before the final executable statement, or use an `if __name__ == "__main__":` block. |
| Flake8 E501 / Pylint C0301 | Formatting | 12, 40 | Lines exceed the recommended maximum length. | Break long statements across multiple lines. |
| Pylint C0209 | Code Style | 12, 15 | Old-style `%` string formatting is used. | Replace it with f-strings, such as `f"Seat {seat_number} already taken for {show_id}"`. |
| Pylint W1514 | File Handling | 28, 33 | `open()` is used without specifying a file encoding. | Use `open(file, "w", encoding="utf-8")`. |
| Pylint R1732 | Resource Management | 28, 33 | Files are opened without being closed explicitly. | Use a `with open(...) as f:` context manager. |
| Pylint W0603 | Design | 32 | The `global shows` statement modifies global program state. | Return the loaded data from the function or encapsulate show data in a class. |
| Pylint C0103 | Naming | 37 | `printSeatingSummary` does not follow Python's snake_case naming convention. | Rename it to `print_seating_summary()`. |
| Functional Issue | Validation | 42-50 | The program accepts invalid seat values such as `-1`, `"A7"`, and string `"5"`. | Validate that the seat is an integer within the valid range before booking. |
| Functional Issue | Input Handling | 42 | User input is stored as a string, so entering `5` produces `"5"` instead of integer `5`. | Convert input using `int()`, with error handling for invalid input. |
| Functional Issue | Data Consistency | 9, 42-50 | The program does not prevent booking a seat number greater than the total number of seats, such as seat `25` when only 20 seats exist. | Check that `1 <= seat_number <= show["seats"]` before booking. |
| Functional Issue | Program Structure | 57 | `main()` is called immediately when the module is imported. | Use `if __name__ == "__main__": main()` to run it only as a script. |

## Priority

The most important issues to fix first are the weak MD5 hashing, insecure file permissions, mutable default argument, bare exception, and missing seat validation.
