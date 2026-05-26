import tkinter as tk
from tkinter import ttk, messagebox
import re

def is_safe_expression(expr, var_name):
    """
    Простая проверка: разрешены только цифры, операторы +-*/., скобки, пробелы,
    и указанная переменная. Запрещены вызовы функций, импорты и т.п.
    """
    # Заменяем переменную на временный маркер для проверки
    temp_expr = expr.replace(var_name, "x")
    # Разрешённые символы: цифры 0-9, + - * / . ( ) пробелы, и x (маркер)
    allowed = r'^[\d\+\-\*\/\.\(\)\sx]+$'
    if re.match(allowed, temp_expr):
        return True
    return False

def calculate():
    expr = entry_expr.get().strip()
    var_name = entry_var.get().strip()
    value_str = entry_value.get().strip()

    if not expr or not var_name or not value_str:
        messagebox.showerror("Ошибка", "Заполните все поля!")
        return

    # Проверяем, что имя переменной состоит только из букв (без пробелов)
    if not var_name.isidentifier():
        messagebox.showerror("Ошибка", "Имя переменной должно быть корректным идентификатором (буквы, цифры, _)")
        return

    # Пытаемся преобразовать значение в число (int или float)
    try:
        value = float(value_str)
        if value.is_integer():
            value = int(value)
    except ValueError:
        messagebox.showerror("Ошибка", "Значение переменной должно быть числом")
        return

    # Проверка безопасности выражения
    if not is_safe_expression(expr, var_name):
        messagebox.showerror("Ошибка", "Выражение содержит недопустимые символы. Разрешены только цифры, + - * / . ( ) и пробелы.")
        return

    # Подставляем значение переменной
    # Чтобы не заменить части других слов (например, если var_name='a', а в выражении 'abs' - не должны менять),
    # используем границы слов. Упрощённо: заменяем все вхождения var_name как отдельного слова.
    import re
    # Регулярное выражение: \b - граница слова
    pattern = r'\b' + re.escape(var_name) + r'\b'
    substituted = re.sub(pattern, str(value), expr)

    try:
        # Вычисляем выражение
        result = eval(substituted)
        # Форматируем результат: если целое число - без .0
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        messagebox.showinfo("Результат", f"Выражение: {expr}\nПодстановка: {var_name} = {value}\nРезультат: {result}")
    except ZeroDivisionError:
        messagebox.showerror("Ошибка", "Деление на ноль в выражении!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось вычислить выражение:\n{str(e)}")

# Создание GUI
root = tk.Tk()
root.title("Вычисление выражения с переменной")
root.geometry("500x250")
root.resizable(False, False)

# Основной фрейм
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill="both", expand=True)

# Поле "Математическое выражение"
ttk.Label(main_frame, text="Выражение (с одной переменной):", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
entry_expr = ttk.Entry(main_frame, width=40, font=("Courier", 10))
entry_expr.grid(row=1, column=0, pady=5, sticky="ew")
entry_expr.insert(0, "2*a/4-1")  # пример

# Поле "Имя переменной"
ttk.Label(main_frame, text="Имя переменной:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", pady=5)
entry_var = ttk.Entry(main_frame, width=20)
entry_var.grid(row=3, column=0, pady=5, sticky="w")
entry_var.insert(0, "a")

# Поле "Значение переменной"
ttk.Label(main_frame, text="Значение переменной:", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky="w", pady=5)
entry_value = ttk.Entry(main_frame, width=20)
entry_value.grid(row=5, column=0, pady=5, sticky="w")
entry_value.insert(0, "2")

# Кнопка
btn_calc = ttk.Button(main_frame, text="Вычислить", command=calculate)
btn_calc.grid(row=6, column=0, pady=15)

# Пояснение
note = ttk.Label(main_frame, text="Примечание: поддерживаются операции +, -, *, /, скобки и числа.\n"
                                  "Используйте точку в качестве десятичного разделителя.",
                 foreground="gray", wraplength=450)
note.grid(row=7, column=0, pady=5)

# Разрешаем растягивание поля ввода выражения по горизонтали
main_frame.columnconfigure(0, weight=1)

root.mainloop()