# DS231 Assignment 4

## Overview and Objectives

In this assignment, you will build a payroll management system — a structured program that manages employee records, tracks pay and benefits, and maintains history of changes made to the system. The primary goal is to practice working with Python's core sequence data structures — lists, sets, tuples, and dictionaries — and to understand how each one plays a distinct, irreplaceable role in a realistic program.

Beyond data structures, this assignment reinforces three important programming concepts:

- Exception handling: Your functions must anticipate invalid inputs and raise appropriate exceptions rather than crashing.
- Aliasing vs. cloning: When saving a snapshot of data to a change log, you will learn why a plain assignment is not enough — and how `copy.deepcopy()` ensures your saved copy stays frozen even as the original changes.

## Instructions

1. All your code goes into `payroll.py`, the starter file provided. You do not need to create any new Python files. The functions you need to implement are: `add_employee()`, `run_registration()`, `get_employee()`, `get_employees_by_department()`, `get_employees_by_level()`, `assign_benefit()`, `save_to_change_log()`, `update_employee_pay()`, `update_employee_level()`, and `remove_employee()`.

2. Do not modify the global variable initialization block at the top of `payroll.py`, or the `if __name__ == "__main__":` block at the bottom. These are provided for you and must remain unchanged.

3. Grading basis varies by function. Most functions in this assignment are graded on their **return values** and the **state of the global variables** after they run. Thus, as mentioned above, it is important that you don't modify global variable initialization. The function `run_registration()` is graded on what it **prints to the terminal** — for that function, your output must match the example output exactly, including spacing, punctuation, and capitalization. Each task description will make clear which grading basis applies.

4. Ensure that your program runs without errors. If your code fails to execute due to a syntax error or uncaught exception at import time, a flat **20% point deduction** will be applied, regardless of the nature of the error.

5. To be eligible for partial credit on select functions, use the intermediate variable names specified in each task's ***Function specification*** section.


## The Payroll System

Before writing any functions, read through this section carefully to understand the system you are building and the data it manages.

### Purpose

The payroll system tracks a company's employees across departments and seniority levels. It stores each employee's pay information and benefit enrollments, and maintains a change log — a permanent record of every modification made to existing employee data.

### System Features

- **Register** new employees by parsing a formatted input string containing their name, level, department, pay type, and pay amount.
- **Look up** employees by name, department, or seniority level.
- **Assign** benefit programs to employees.
- **Update** an employee's pay or level, with every change automatically recorded in the change log.
- **Remove** employees from the system, with their last known record saved before deletion.

### Global Variables

The following variables are declared at the top of `payroll.py`. **Every function you implement will read from or write to these globals.** 

| Variable | Type | Purpose |
|---|---|---|
| `employee_list` | `list` | Ordered record of employee names, in the order they were registered |
| `employee_set` | `set` | Set of all current employee names, used for fast uniqueness checking |
| `employee_records` | `dict` | Maps each employee name to a dictionary of their info: `level`, `dept`, `pay_type`, `pay_amount` |
| `employee_benefits` | `dict` | Maps each employee name to a set of benefit codes they are enrolled in |
| `VALID_LEVELS` | `set` | The allowed seniority levels: `{'employee', 'manager', 'executive'}` |
| `VALID_DEPARTMENTS` | `set` | The allowed departments: `{'engineering', 'marketing', 'hr', 'finance', 'operations'}` |
| `VALID_PAY_TYPES` | `set` | The allowed pay types: `{'hourly', 'salary'}` |
| `BENEFITS` | `dict` | Maps benefit codes to a tuple of `(description, monthly_cost)` |
| `change_log` | `list` | A list of snapshots recording the state of an employee record *before* a modification or deletion |

The `BENEFITS` dictionary is pre-loaded with three available benefit programs:

```python
BENEFITS = {
    'healthcare': ('Health Insurance', 150.0),
    'childcare':  ('Child Care Support', 100.0),
    'transport':  ('Public Transport Benefit', 50.0)
}
```

Each benefit's value is a tuple — an immutable, ordered pair of `(description, monthly_cost)`. Tuples are appropriate here because benefit definitions are fixed: the description and cost of a plan never change at runtime.

Notice that `employee_list` and `employee_set` both track employee names but serve different roles. The list preserves insertion order, which is important for traversal. The set enables efficient membership checking, which is important for fast duplicate detection. Both must be kept in sync whenever an employee is added or removed.


## Part 1. Employee Registration [35 Points]

This part asks you to build the primary entry point of the system: code that accepts raw text input, validates every field, and registers a new employee across all relevant data structures.

### Task 1.1 — Register a New Employee [25 Points]

**`add_employee(input_str)`** parses a single line of text and registers a new employee in the system. The input is a space-separated string with exactly five fields:

```
"John-Smith employee engineering salary 75000"
```

The fields, in order, are:

| Field | Expected format | Valid values |
|---|---|---|
| `name` | One word; use dashes in place of spaces (e.g. `John-Smith`) | Any string; must be unique and not duplicate of any existing names |
| `level` | One word, lowercase | Stored in `VALID_LEVELS` (`employee`, `manager`, `executive`) |
| `dept` | One word, lowercase | Stored in `VALID_DEPARTMENTS` (`engineering`, `marketing`, `hr`, `finance`, `operations`) |
| `pay_type` | One word, lowercase | Stored in `VALID_PAY_TYPES` (hourly`, `salary`) |
| `pay_amount` | A number (integer or decimal) | Any value convertible to `float` |

The function must validate each field **in the order listed above** and raise a `ValueError` with a descriptive message at the **first** problem encountered. If all fields are valid and the name has not been registered before, it adds the employee to all four tracking structures.

**Validation steps, in order:**

1. Split `input_str` on whitespace. If the result does not contain exactly 5 elements, raise `ValueError(f"Expected 5 fields, got {n}")` where `n` is the actual count.
2. Check that `name` is **not** already in `employee_set`. If it is, raise `ValueError(f"Name already exists: {name}")`.
3. Check that `level` is in `VALID_LEVELS`. If not, raise `ValueError(f"Invalid level: {level}")`.
4. Check that `dept` is in `VALID_DEPARTMENTS`. If not, raise `ValueError(f"Invalid department: {dept}")`.
5. Check that `pay_type` is in `VALID_PAY_TYPES`. If not, raise `ValueError(f"Invalid pay type: {pay_type}")`.
6. Try to convert `pay_amount` to a `float`. If conversion fails, raise `ValueError(f"Invalid pay amount: {pay_amount}")`.

On success, update the global variables as follows:
- Append `name` to `employee_list`
- Add `name` to `employee_set`
- Add an entry to `employee_records`: `employee_records[name] = {'level': level, 'dept': dept, 'pay_type': pay_type, 'pay_amount': <float>}`
- Initialize `employee_benefits[name] = set()`

New employees are **not** added to `change_log`. The change log is only for updates and deletions of existing records.

***Function specification.***
- Input: `input_str` (str)
- Return: the newly created record dictionary for the employee (dict)
- Raises: `ValueError` for any invalid or missing field, or a duplicate name
- Intermediate variable for partial credit: `fields` — the list produced by calling `.split()` on `input_str` [5 pts]

***Function demonstration.***

```python
>>> add_employee("John-Smith employee engineering salary 75000")
{'level': 'employee', 'dept': 'engineering', 'pay_type': 'salary', 'pay_amount': 75000.0}

# After this call:
# employee_list    → ['John-Smith']
# employee_set     → {'John-Smith'}
# employee_records → {'John-Smith': {'level': 'employee', 'dept': 'engineering', 'pay_type': 'salary', 'pay_amount': 75000.0}}
# employee_benefits → {'John-Smith': set()}

>>> add_employee("John-Smith manager hr hourly 30")
ValueError: Name already exists: John-Smith

>>> add_employee("Bob intern engineering salary 50000")
ValueError: Invalid level: intern

>>> add_employee("Alice engineer")
ValueError: Expected 5 fields, got 2
```

***Hint.***
- Use `str.split()` with no arguments — it splits on any whitespace and handles extra spaces automatically.
- To safely convert a string to a float, use a `try`/`except` block: put `float(pay_amount_str)` inside `try`, and raise your `ValueError` in the `except` clause.
- To check set membership, use the `in` operator: `name in employee_set`.


### Task 1.2 — Interactive Registration Loop [10 Points]

**`run_registration()`** runs an interactive loop that lets a user register multiple employees one at a time by typing formatted input strings. It calls `add_employee()` internally to process each entry.

On each iteration, the function:
1. Prompts the user with the exact string `"Enter employee info (or 'quit' to stop): "`.
2. If the user types `"quit"`, exits the loop and prints the final count of successfully registered employees.
3. Otherwise, calls `add_employee()` with the raw input.
   - If `add_employee()` succeeds, print `"Employee {name} added successfully."` where `name` is the employee's name field (the first word of the input string).
   - If `add_employee()` raises a `ValueError`, print `"Error: {message}. Please try again."` where `message` is the text of the exception. Then continue the loop and prompt again.

***Function specification.***
- Input: none
- Return: none
- Graded on: **terminal output** — your printed output must match the example below exactly, including punctuation, capitalization, and spacing.

***Example output.*** Your program's output must match the format below exactly.

```text
Enter employee info (or 'quit' to stop): John-Smith employee engineering salary 75000
Employee John-Smith added successfully.
Enter employee info (or 'quit' to stop): John-Smith manager hr hourly 30
Error: Name already exists: John-Smith. Please try again.
Enter employee info (or 'quit' to stop): Bob intern engineering salary 50000
Error: Invalid level: intern. Please try again.
Enter employee info (or 'quit' to stop): Alice-Chen manager marketing salary 95000
Employee Alice-Chen added successfully.
Enter employee info (or 'quit' to stop): quit
2 employee(s) registered.
```

***Hint.***
- Use a `while True:` loop and `break` out of it when the user types `"quit"`.
- Keep a counter that you increment each time `add_employee()` completes without raising an exception.
- To extract the name from the raw input string for the success message, use `input_str.split()[0]`. Do this only when you are sure the input has at least one word (i.e., inside the `try` block after `add_employee()` succeeds).
- When `add_employee()` raises a `ValueError`, your `except ValueError:` block catches it — this means the error is handled and **the program does not crash or stop**. After the `except` block finishes, execution continues normally, and the loop goes around to prompt the user again. This is the key purpose of `try`/`except`: intercepting an error so the program can recover instead of terminating.
- To print the error message from the exception, you need to capture the exception in a variable. The syntax `except ValueError as err:` does exactly that — `err` holds the exception object, and `str(err)` converts it to the message string. Here is an illustration:

  ```python
  try:
      add_employee("Bob intern engineering salary 50000")
  except ValueError as err:
      print(str(err))   # prints: Invalid level: intern
  ```

  You can then use `str(err)` inside your print statement to match the required output format.


## Part 2. Accessors [15 Points]

These three functions retrieve information from the global variables without modifying them. All three are graded on their **return values**.

### Task 2.1 — Look Up a Single Employee [5 Points]

**`get_employee(name)`** retrieves the full record for a single employee by name.

***Function specification.***
- Input: `name` (str)
- Return: the employee's record dictionary from `employee_records` (dict)
- Raises: `KeyError` if `name` is not found in `employee_records`

***Function demonstration.***

```python
>>> get_employee("John-Smith")
{'level': 'employee', 'dept': 'engineering', 'pay_type': 'salary', 'pay_amount': 75000.0}

>>> get_employee("Nobody")
KeyError: 'Nobody'
```

***Hint.*** Accessing `employee_records[name]` directly will raise a `KeyError` automatically if the key does not exist — you do not need to raise it yourself.


### Task 2.2 — Look Up Employees by Department [5 Points]

**`get_employees_by_department(dept)`** returns a list of all employee names currently assigned to a given department.

***Function specification.***
- Input: `dept` (str)
- Return: a list of employee names whose `dept` field matches the argument; an empty list if none are found (list)

***Function demonstration.***

```python
>>> get_employees_by_department("engineering")
['John-Smith']

>>> get_employees_by_department("marketing")
['Alice-Chen']

>>> get_employees_by_department("finance")
[]
```


### Task 2.3 — Look Up Employees by Level [5 Points]

**`get_employees_by_level(level)`** returns a list of all employee names at a given seniority level.

***Function specification.***
- Input: `level` (str)
- Return: a list of employee names whose `level` field matches the argument; an empty list if none are found (list)

***Function demonstration.***

```python
>>> get_employees_by_level("manager")
['Alice-Chen']

>>> get_employees_by_level("executive")
[]
```


## Part 3. Benefit Assignment [15 Points]

### Task 3.1 — Enroll an Employee in a Benefit Program [15 Points]

**`assign_benefit(name, benefit_code)`** enrolls an employee in one of the three available benefit programs. Each employee's benefit enrollments are stored as a **set** in `employee_benefits[name]`. Because it is a set, enrolling an employee in the same benefit twice has no effect — sets never store duplicate values.

**Validation steps:**
1. Check that `name` is in `employee_records`. If not, raise `KeyError(name)`.
2. Check that `benefit_code` is in `BENEFITS`. If not, raise `ValueError(f"Invalid benefit code: {benefit_code}")`.
3. Add `benefit_code` to `employee_benefits[name]`.

***Function specification.***
- Input: `name` (str), `benefit_code` (str)
- Return: none
- Raises: `KeyError` if the employee is not found; `ValueError` if the benefit code is not in `BENEFITS`
- Graded on: the state of `employee_benefits` after the call

***Function demonstration.***

```python
>>> assign_benefit("John-Smith", "healthcare")
# employee_benefits["John-Smith"] → {'healthcare'}

>>> assign_benefit("John-Smith", "healthcare")   # duplicate — no effect
# employee_benefits["John-Smith"] → {'healthcare'}

>>> assign_benefit("John-Smith", "transport")
# employee_benefits["John-Smith"] → {'healthcare', 'transport'}

>>> assign_benefit("John-Smith", "dental")
ValueError: Invalid benefit code: dental

>>> assign_benefit("Nobody", "healthcare")
KeyError: 'Nobody'
```

***Hint.*** Use `.add()` to insert an element into a set. Unlike a list's `.append()`, set `.add()` silently does nothing if the value is already present — that is exactly the behavior you want here.


## Part 4. Change Log and Modifiers [35 Points]

This part introduces one of the most important ideas in the assignment: the difference between aliasing and cloning an object in memory.

### Aliasing vs. Cloning

Recall that assigning one dictionary to another variable creates an alias — both names point to the same object, so later changes to the original will silently affect the alias. Use `copy.deepcopy()` to create a fully independent snapshot instead. This is exactly what the change log requires: each entry must stay frozen at the moment it was saved, regardless of what happens to the original record afterward.

Each entry appended to `change_log` has the following structure:

```python
{'name': 'John-Smith', 'old_record': {'level': 'employee', 'dept': 'engineering', 'pay_type': 'salary', 'pay_amount': 75000.0}}
```

The `name` field identifies which employee's record was snapshotted, and serves as the version identifier for that log entry. The `old_record` field holds the frozen copy of the employee's data as it existed before the change. New employee registrations do **not** generate change log entries — only updates and deletions do.


### Task 4.1 — Save a Snapshot to the Change Log [10 Points]

**`save_to_change_log(name)`** is a helper function that must be called by all modifier and deletion functions before making any changes. It appends a frozen snapshot of the employee's current record to `change_log`.

***Function specification.***
- Input: `name` (str)
- Return: none
- Graded on: the state of `change_log` after the call — specifically, that `change_log[-1]['old_record']` holds the correct pre-change values even after `employee_records[name]` is subsequently modified

***Function demonstration.***

```python
>>> add_employee("John-Smith employee engineering salary 75000")
>>> save_to_change_log("John-Smith")
>>> employee_records["John-Smith"]["pay_amount"] = 80000.0   # simulate a later change

>>> change_log[-1]
{'name': 'John-Smith', 'old_record': {'level': 'employee', 'dept': 'engineering', 'pay_type': 'salary', 'pay_amount': 75000.0}}
# old_record still shows 75000.0 — the snapshot was frozen at the time save_to_change_log was called.
```

***Hint.*** Use `copy.deepcopy(employee_records[name])` to create the frozen snapshot. `import copy` is already included at the top of `payroll.py` — you do not need to import it again.


### Task 4.2 — Update an Employee's Pay [5 Points]

**`update_employee_pay(name, new_amount)`** updates an employee's pay amount. It automatically saves a snapshot to the change log before making any change.

**Steps, in order:**
1. Check that `name` is in `employee_records`. If not, raise `KeyError(name)`.
2. Try to convert `new_amount` to `float`. If conversion fails, raise `ValueError(f"Invalid pay amount: {new_amount}")`.
3. Call `save_to_change_log(name)`.
4. Update `employee_records[name]['pay_amount']` to the converted float value.

***Function specification.***
- Input: `name` (str), `new_amount` (int, float, or str)
- Return: none
- Raises: `KeyError` if employee not found; `ValueError` if amount is not numeric
- Graded on: state of `employee_records` and `change_log` after the call


### Task 4.3 — Update an Employee's Level [5 Points]

**`update_employee_level(name, new_level)`** updates an employee's seniority level. It automatically saves a snapshot to the change log before making any change.

**Steps, in order:**
1. Check that `name` is in `employee_records`. If not, raise `KeyError(name)`.
2. Check that `new_level` is in `VALID_LEVELS`. If not, raise `ValueError(f"Invalid level: {new_level}")`.
3. Call `save_to_change_log(name)`.
4. Update `employee_records[name]['level']` to `new_level`.

***Function specification.***
- Input: `name` (str), `new_level` (str)
- Return: none
- Raises: `KeyError` if employee not found; `ValueError` if level is not in `VALID_LEVELS`
- Graded on: state of `employee_records` and `change_log` after the call


### Task 4.4 — Remove an Employee [15 Points]

**`remove_employee(name)`** permanently removes an employee from all tracking structures, after first saving a final snapshot of their record to the change log.

**Steps, in order:**
1. Check that `name` is in `employee_records`. If not, raise `KeyError(name)`.
2. Call `save_to_change_log(name)`.
3. Delete `name` from `employee_records`.
4. Remove `name` from `employee_set`.
5. Remove `name` from `employee_list`.
6. Delete `name` from `employee_benefits`.

***Function specification.***
- Input: `name` (str)
- Return: none
- Raises: `KeyError` if employee not found
- Graded on: state of all four global tracking structures and `change_log` after the call

***Function demonstration.***

```python
# Before: employee_list = ['John-Smith'], employee_records has John-Smith's entry

>>> remove_employee("John-Smith")
# change_log[-1] → {'name': 'John-Smith', 'old_record': {'level': 'employee', ...}}
# employee_list    → []
# employee_set     → set()
# employee_records → {}
# employee_benefits → {}

>>> remove_employee("Nobody")
KeyError: 'Nobody'
```

***Hint.***
- Use `employee_list.remove(name)` to remove a value by content. This is different from `del employee_list[index]`, which removes by position.
- Use `employee_set.remove(name)` or `employee_set.discard(name)` for the set. Since you already verified the employee exists, either works.
- Use `del employee_records[name]` and `del employee_benefits[name]` to remove dictionary entries.


