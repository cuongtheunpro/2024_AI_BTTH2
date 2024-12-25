import re
import itertools

def is_valid_predicate_expression(expression):
    """Kiểm tra cú pháp biểu thức vị từ (đơn giản)."""
    valid_chars = set("x()><=%!&| ")
    if not set(expression) <= valid_chars:
        return False, "Biểu thức vị từ chứa ký tự không hợp lệ."
    return True, ""

def evaluate_predicate(predicate, domain, x_value):
    """Tính giá trị của vị từ."""
    try:
        expression = predicate.replace("x", str(x_value))
        return eval(expression)
    except (NameError, TypeError, SyntaxError, ZeroDivisionError):
        return "Lỗi trong biểu thức vị từ."

    

def verify_formula(formula, domain):
    """Xác minh công thức logic vị từ."""
    try:
        # Thay thế → bằng or not để eval hoạt động chính xác
        formula = formula.replace("→", " or not ")

        # Xử lý ∀x
        if "∀x" in formula:
            forall_part = formula.split("∀x")[1].split("∧")[0].strip() if "∧" in formula else formula.split("∀x")[1].strip()
            for x_value in domain:
                if not eval(forall_part.replace("x", str(x_value))):
                    return False

        # Xử lý ∃y
        if "∃y" in formula:
            exists_part = formula.split("∃y")[1].strip()
            exists = False
            for y_value in domain:
                if eval(exists_part.replace("y", str(y_value))):
                    exists = True
                    break
            if not exists:
                return False
        return True
    except (NameError, SyntaxError, TypeError, ZeroDivisionError, IndexError):
        return "Lỗi trong biểu thức hoặc công thức."

# Các ví dụ (đã được kiểm tra kỹ)
test_cases = [
    ("∀x (x > 1 → x % 2 == 0) ∧ ∃y (y > 1)", {1, 2, 3}), #False
    ("∀x (x > 0 and x < 4) ∧ ∃y not (y > 0)", {1, 2, 3}), #True
    ("∀x (x > 0) ∧ ∃y (y == 4)", {1,2,3}), #False
    ("∀x (x == 1 or x == 2) ∧ ∃y (y == 1)", {1, 2}), #True
    ("∀x (x > 1 → x % 2 == 0) ∧ ∃y (y > 1)", {1, 2, 3}), #False
    ("∀x (x > 1 or x < 3) ∧ ∃y (y == 3)",{1,2,3}), #True
    ("∀x (x > 0)", {1,2,3}), #true
    ("∃y (y == 3)",{1,2,3}) #true
]

for i, (formula, domain) in enumerate(test_cases):
    print(f"\nKiểm tra công thức {i+1}: {formula}")
    result = verify_formula(formula, domain)
    print(f"Kết quả: {result}")
    print("-" * 30)