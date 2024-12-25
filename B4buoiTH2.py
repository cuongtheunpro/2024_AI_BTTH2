import itertools

def evaluate(expression, assignment):
    """Tính giá trị của biểu thức với một gán giá trị."""
    try:
        # Thay thế biến bằng giá trị
        for var, val in assignment.items():
            expression = expression.replace(var, str(val))
        # Thay thế các toán tử logic
        expression = expression.replace("→", " or not ")
        expression = expression.replace("∧", " and ")
        expression = expression.replace("¬", " not ")
        return eval(expression)
    except (NameError, SyntaxError):
        return None

def truth_table_prove(premises, conclusion):
    """Chứng minh bằng bảng chân trị."""
    variables = set()
    for expr in premises + [conclusion]:
        for char in expr:
            if 'A' <= char <= 'Z':
                variables.add(char)
    variables = sorted(list(variables))
    n = len(variables)

    for values in itertools.product([True, False], repeat=n):
        assignment = dict(zip(variables, values))
        premises_true = all(evaluate(p, assignment) for p in premises)
        conclusion_true = evaluate(conclusion, assignment)
        if premises_true and not conclusion_true:
            return False  # Tìm thấy trường hợp tiền đề đúng mà kết luận sai
    return True  # Không tìm thấy trường hợp nào như vậy

# Các ví dụ 
test_cases = [
    (["P → Q", "Q → R"], "P → R"), #True
    (["P", "P → Q"], "Q"), #True
    (["P ∨ Q", "¬P"], "Q"), #True
    (["P", "¬Q"], "P ∧ ¬Q"), #True
    (["P → Q", "¬Q"], "¬P"), #True
    (["P"], "¬P"), #False
    (["P","Q","R"],"P and Q and R") #true
]

for premises, conclusion in test_cases:
    print(f"\nTiền đề: {premises}")
    print(f"Kết luận: {conclusion}")
    result = truth_table_prove(premises, conclusion)
    print(f"Kết quả chứng minh: {'Đúng' if result else 'Sai'}")
    print("-" * 30)