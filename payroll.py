import copy

# ── Global variables — do not modify ─────────────────────────────────────────

employee_list = []
employee_set  = set()
employee_records  = {}
employee_benefits = {}

VALID_LEVELS      = {'employee', 'manager', 'executive'}
VALID_DEPARTMENTS = {'engineering', 'marketing', 'hr', 'finance', 'operations'}
VALID_PAY_TYPES   = {'hourly', 'salary'}

BENEFITS = {
    'healthcare': ('Health Insurance',        150.0),
    'childcare':  ('Child Care Support',      100.0),
    'transport':  ('Public Transport Benefit', 50.0),
}

change_log = []

# ── Your implementations go below ────────────────────────────────────────────


# Part 1 — Employee Registration

def add_employee(input_str):
    pass


def run_registration():
    pass


# Part 2 — Accessors

def get_employee(name):
    pass


def get_employees_by_department(dept):
    pass


def get_employees_by_level(level):
    pass


# Part 3 — Benefit Assignment

def assign_benefit(name, benefit_code):
    pass


# Part 4 — Change Log and Modifiers

def save_to_change_log(name):
    pass


def update_employee_pay(name, new_amount):
    pass


def update_employee_level(name, new_level):
    pass


def remove_employee(name):
    pass

