
import tkinter as tk
import math
import ast
import operator

window = tk.Tk()
window.title("Scientific Calculator")
window.geometry("480x700")
window.resizable(False, False)
window.configure(bg="#1e1e2e")

angle_mode = tk.StringVar(value="DEG")
expression = tk.StringVar(value="")


def get_functions():
    if angle_mode.get() == "DEG":
        sine = lambda x: math.sin(math.radians(x))
        cosine = lambda x: math.cos(math.radians(x))
        tangent = lambda x: math.tan(math.radians(x))
        asin = lambda x: math.degrees(math.asin(x))
        acos = lambda x: math.degrees(math.acos(x))
        atan = lambda x: math.degrees(math.atan(x))
    else:
        sine = math.sin
        cosine = math.cos
        tangent = math.tan
        asin = math.asin
        acos = math.acos
        atan = math.atan

    return {
        "sin": sine,
        "cos": cosine,
        "tan": tangent,
        "asin": asin,
        "acos": acos,
        "atan": atan,
        "sqrt": math.sqrt,
        "log": math.log10,
        "ln": math.log,
        "abs": abs
    }



binary_operations = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod
}

unary_operations = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg
}


def evaluate_node(node):
    functions = get_functions()

    if isinstance(node, ast.Expression):
        return evaluate_node(node.body)

    elif isinstance(node, ast.Constant):
        if type(node.value) not in (int, float):
            raise ValueError("Invalid number")
        return node.value

    elif isinstance(node, ast.Name):
        constants = {
            "pi": math.pi,
            "e": math.e
        }

        if node.id in constants:
            return constants[node.id]

        raise ValueError("Unknown constant")

    elif isinstance(node, ast.BinOp):
        operation = binary_operations.get(type(node.op))

        if operation is None:
            raise ValueError("Invalid operation")

        left = evaluate_node(node.left)
        right = evaluate_node(node.right)

        if isinstance(node.op, ast.Pow) and abs(right) > 1000:
            raise ValueError("Power too large")

        return operation(left, right)

    elif isinstance(node, ast.UnaryOp):
        operation = unary_operations.get(type(node.op))

        if operation is None:
            raise ValueError("Invalid operation")

        return operation(evaluate_node(node.operand))

    elif isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Invalid function")

        function = functions.get(node.func.id)

        if function is None or len(node.args) != 1:
            raise ValueError("Unknown function")

        return function(evaluate_node(node.args[0]))

    raise ValueError("Invalid expression")


def calculate_value(text):
    tree = ast.parse(text, mode="eval")
    return evaluate_node(tree)


def insert(value):
    expression.set(expression.get() + value)


def clear():
    expression.set("")
    result_label.config(text="0")


def delete():
    expression.set(expression.get()[:-1])


def toggle_angle():
    if angle_mode.get() == "DEG":
        angle_mode.set("RAD")
    else:
        angle_mode.set("DEG")

    mode_button.config(text=angle_mode.get())


def calculate():
    try:
        result = calculate_value(expression.get())

        if isinstance(result, complex):
            raise ValueError("Complex result")

        if not math.isfinite(result):
            raise ValueError("Invalid result")

        if isinstance(result, float):
            if result.is_integer():
                result = int(result)
            else:
                result = round(result, 10)

        result_label.config(text=str(result))

    except ZeroDivisionError:
        result_label.config(text="Cannot divide by zero")

    except Exception:
        result_label.config(text="Invalid expression")


def use_result():
    value = result_label.cget("text")

    try:
        float(value)
        expression.set(value)
    except ValueError:
        pass



display_frame = tk.Frame(
    window,
    bg="#1e1e2e",
    padx=15,
    pady=15
)

display_frame.pack(fill="x")

mode_button = tk.Button(
    display_frame,
    text="DEG",
    font=("Arial", 11, "bold"),
    bg="#313244",
    fg="#89b4fa",
    bd=0,
    command=toggle_angle
)

mode_button.pack(anchor="w", pady=5)

display = tk.Entry(
    display_frame,
    textvariable=expression,
    font=("Arial", 25),
    bg="#313244",
    fg="white",
    insertbackground="white",
    justify="right",
    bd=0
)

display.pack(fill="x", ipady=15, pady=10)

result_label = tk.Label(
    display_frame,
    text="0",
    font=("Arial", 20),
    bg="#1e1e2e",
    fg="#a6adc8",
    anchor="e"
)

result_label.pack(fill="x", pady=5)


button_frame = tk.Frame(
    window,
    bg="#1e1e2e",
    padx=10,
    pady=10
)

button_frame.pack(fill="both", expand=True)

buttons = [
    ["sin", "cos", "tan", "log", "ln"],
    ["sqrt", "x²", "xʸ", "(", ")"],
    ["7", "8", "9", "÷", "DEL"],
    ["4", "5", "6", "×", "AC"],
    ["1", "2", "3", "-", "π"],
    ["0", ".", "=", "+", "e"]
]


def button_action(value):
    if value == "AC":
        clear()

    elif value == "DEL":
        delete()

    elif value == "=":
        calculate()

    elif value == "x²":
        insert("**2")

    elif value == "xʸ":
        insert("**")

    elif value == "sqrt":
        insert("sqrt(")

    elif value in ["sin", "cos", "tan", "log", "ln"]:
        insert(value + "(")

    elif value == "π":
        insert("pi")

    elif value == "e":
        insert("e")

    elif value == "÷":
        insert("/")

    elif value == "×":
        insert("*")

    else:
        insert(value)



for row_index, row in enumerate(buttons):
    for column_index, value in enumerate(row):

        if value == "=":
            bg_color = "#89b4fa"
            fg_color = "#11111b"

        elif value in ["AC", "DEL"]:
            bg_color = "#f38ba8"
            fg_color = "#11111b"

        elif value in ["+", "-", "×", "÷", "sin",
                       "cos", "tan", "log", "ln",
                       "sqrt", "x²", "xʸ"]:
            bg_color = "#45475a"
            fg_color = "white"

        else:
            bg_color = "#313244"
            fg_color = "white"

        button = tk.Button(
            button_frame,
            text=value,
            font=("Arial", 14, "bold"),
            bg=bg_color,
            fg=fg_color,
            activebackground="#585b70",
            activeforeground="white",
            bd=0,
            command=lambda v=value: button_action(v)
        )

        button.grid(
            row=row_index,
            column=column_index,
            sticky="nsew",
            padx=4,
            pady=5,
            ipadx=2,
            ipady=13
        )

# Make buttons expand equally
for i in range(6):
    button_frame.rowconfigure(i, weight=1)

for i in range(5):
    button_frame.columnconfigure(i, weight=1)


def keyboard_enter(event):
    calculate()
    return "break"


def keyboard_escape(event):
    clear()
    return "break"


def keyboard_delete(event):
    delete()
    return "break"


window.bind("<Return>", keyboard_enter)
window.bind("<Escape>", keyboard_escape)
window.bind("<BackSpace>", keyboard_delete)

window.mainloop()
