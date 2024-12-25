import itertools
import re

def is_valid_expression(expression):
    """Kiểm tra tính hợp lệ của biểu thức logic."""
    expression = expression.replace(" ", "")
    valid_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ()¬∧∨→↔")
    if not set(expression) <= valid_chars:
        return False, "Biểu thức chứa ký tự không hợp lệ."

    open_brackets = 0
    for char in expression:
        if char == "(": open_brackets += 1
        elif char == ")": open_brackets -= 1
        if open_brackets < 0:
            return False, "Lỗi ngoặc: ngoặc đóng nhiều hơn ngoặc mở."
    if open_brackets != 0:
        return False, "Lỗi ngoặc: số lượng ngoặc mở và đóng không bằng nhau."

    # Kiểm tra cú pháp bằng regex 
    if re.search(r"[∧∨→↔]{2}|¬[∧∨→↔]|[(][∧∨→↔]|[∧∨→↔][)]", expression):
        return False, "Lỗi cú pháp: toán tử logic không hợp lệ."
    return True, "Biểu thức hợp lệ."

def evaluate_expression(expression, variables):
    """Tính giá trị của biểu thức logic."""
    try:
        for var, value in variables.items():
            expression = expression.replace(var, str(value))

        expression = expression.replace("¬", "not ")
        expression = expression.replace("∧", "and ")
        expression = expression.replace("∨", "or ")
        expression = expression.replace("→", "or not ") #a->b = not a or b
        expression = expression.replace("↔", "==") # a<->b = a==b
        expression = expression.replace("or not (", "or not ") # Xử lý ngoặc thừa

        return eval(expression)
    except (NameError, SyntaxError):
        return "Lỗi biểu thức hoặc biến không được định nghĩa."

def generate_truth_table(expression):
    """Tạo bảng chân trị cho biểu thức."""
    variables = sorted(set(re.findall(r"[A-Z]", expression))) # Tìm tất cả biến trong biểu thức
    if not variables:
        return "Không tìm thấy biến trong biểu thức."

    print(" ".join(variables) + " Kết quả") # In header của bảng
    print("-" * (len(variables) + 7))

    for values in itertools.product([True, False], repeat=len(variables)): # tạo tất cả các trường hợp True/False
        var_values = dict(zip(variables, values)) # gán giá trị cho biến
        result = evaluate_expression(expression, var_values)
        if type(result) == str: # kiểm tra lỗi khi tính toán
            print(result)
            return
        row = " ".join(["T" if v else "F" for v in values]) + " " + ("T" if result else "F")
        print(row)

# Các biểu thức kiểm tra
test_cases = [
    "(A ∨ ¬B) ∧ C",
    "A → (B ∨ C)",
    "(A ∧ B) ↔ (¬A ∨ ¬B)",
    "A ∧ (B ∨ ¬A) → C",
    "A ∧∧ B" #ví dụ lỗi
]

# Duyệt qua các biểu thức
for i, expression in enumerate(test_cases):
    print(f"\nBảng chân trị cho biểu thức {i+1}: {expression}")
    is_valid, message = is_valid_expression(expression)
    print(message)
    if is_valid:
        generate_truth_table(expression)
    print("-" * 30)