import itertools

def evaluate(expression, assignment):
    """Tính giá trị của biểu thức với một gán giá trị."""
    try:
        for var, val in assignment.items():
            expression = expression.replace(var, str(val))
        expression = expression.replace("∨", " or ")
        expression = expression.replace("∧", " and ")
        expression = expression.replace("¬", " not ")
        return eval(expression)
    except (NameError, SyntaxError):
        return None

def find_model(expression):
    """Tìm mẫu giá trị cho biểu thức."""
    variables = set()
    for char in expression:
        if 'A' <= char <= 'Z':
            variables.add(char)
    variables = sorted(list(variables))
    n = len(variables)

    for values in itertools.product([True, False], repeat=n):
        assignment = dict(zip(variables, values))
        if evaluate(expression, assignment):
            return assignment
    return None

# Các ví dụ
test_cases = [
    "(A ∨ B) ∧ (¬A ∨ C)",
    "A ∧ ¬A",
    "P ∨ ¬P",
    "(A ∧ B) → C",
    "A ∧ (B ∨ C) ∧ (¬A ∨ ¬B) ∧ (¬A ∨ ¬C)"
]

for expression in test_cases:
    print(f"\nBiểu thức: {expression}")
    model = find_model(expression)
    if model:
        print("Mẫu giá trị:", model)
    else:
        print("Không tìm thấy mẫu giá trị.")
    print("-" * 30)