import re
#1. Logic mệnh đề - Kiểm tra tính hợp lệ của biểu thức logic
def is_valid_expression(expression):
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

# Các biểu thức và biến (được đặt trong tuple)
test_cases = [
    ("(A ∧ B) → ¬C", {"A": True, "B": False, "C": True}),
    ("(A ∧ B) → ¬C → D", {"A": True, "B": False, "C": True, "D": False}),
    ("(A ∧ B) ∧∧ ¬C", {}),  # Biểu thức lỗi, không cần biến
    ("(A ∧ B) ¬C", {"A":True,"B":False,"C":True}),
    ("(A ∧ B) → ¬(C∨(D∧E))", {"A": True, "B": False, "C": True, "D": True, "E": False}),
]

# Duyệt qua từng trường hợp kiểm tra
for i, (expression, variables) in enumerate(test_cases):
    print(f"Kiểm tra biểu thức {i+1}: {expression}")
    is_valid, message = is_valid_expression(expression)
    print(message)
    if is_valid:
        result = evaluate_expression(expression, variables)
        print(f"Giá trị của biểu thức: {result}")
    print("-" * 20)  # In dấu phân cách giữa các kết quả