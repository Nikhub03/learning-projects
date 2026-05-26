import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import math

# Доступные математические функции для eval
safe_math = {
    'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
    'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
    'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
    'exp': math.exp, 'log': math.log, 'log10': math.log10,
    'sqrt': math.sqrt, 'abs': abs, 'pi': math.pi, 'e': math.e
}

def make_function(expr):
    """Создаёт функцию f(x) из строкового выражения expr (использует x как переменную)"""
    def f(x):
        # Ограниченное пространство имён: x + математические функции
        safe_dict = safe_math.copy()
        safe_dict['x'] = x
        # Вычисляем выражение, но перехватываем любые ошибки
        try:
            return eval(expr, {"__builtins__": None}, safe_dict)
        except Exception as e:
            raise ValueError(f"Ошибка вычисления f({x}): {e}")
    return f

# ------------------ Численные методы ------------------
def bisection_method(f, a, b, eps=1e-6, max_iter=100):
    """
    Метод половинного деления.
    Возвращает (корень, список итераций, сообщение об ошибке)
    """
    if f(a) * f(b) >= 0:
        return None, None, "На интервале [a, b] функция не меняет знак (f(a)*f(b) >= 0)"
    iterations = []
    fa = f(a)
    fb = f(b)
    for i in range(max_iter):
        c = (a + b) / 2
        fc = f(c)
        iterations.append((i+1, a, b, c, fc))
        if abs(fc) < eps or (b - a)/2 < eps:
            return c, iterations, None
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
    return (a + b) / 2, iterations, "Достигнуто максимальное число итераций"

# Дополнительные методы (для расширения)
def newton_method(f, df, x0, eps=1e-6, max_iter=100):
    """Метод Ньютона (требует производную). Для простоты не включаем в GUI по умолчанию."""
    # Реализация может быть добавлена позже
    raise NotImplementedError

def secant_method(f, x0, x1, eps=1e-6, max_iter=100):
    raise NotImplementedError

# Регистрация методов
SOLVER_METHODS = {
    "Метод половинного деления": bisection_method,
    # "Метод Ньютона": newton_method,   # потребует ввода производной
    # "Метод секущих": secant_method,
}

# ------------------ GUI приложения ------------------
class SolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Решение алгебраических уравнений")
        self.root.geometry("750x650")

        self.method_var = tk.StringVar(value=list(SOLVER_METHODS.keys())[0])
        self.create_widgets()

    def create_widgets(self):
        # Выбор метода
        method_frame = ttk.LabelFrame(self.root, text="Численный метод", padding=10)
        method_frame.pack(fill="x", padx=10, pady=5)
        ttk.Combobox(method_frame, textvariable=self.method_var, values=list(SOLVER_METHODS.keys()),
                     state="readonly", width=35).pack(fill="x", pady=2)

        # Ввод функции
        func_frame = ttk.LabelFrame(self.root, text="Уравнение f(x) = 0", padding=10)
        func_frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(func_frame, text="f(x) =").pack(anchor="w")
        self.func_entry = ttk.Entry(func_frame, width=60, font=("Courier", 10))
        self.func_entry.pack(fill="x", pady=2)
        self.func_entry.insert(0, "x**2 - 2")   # пример: x^2 = 2, корень sqrt(2)
        ttk.Label(func_frame, text="Примеры: sin(x), x**3 - 2*x + 1, log(x) - 2, sqrt(x) - 1", foreground="gray").pack(anchor="w")

        # Параметры метода
        param_frame = ttk.LabelFrame(self.root, text="Параметры метода", padding=10)
        param_frame.pack(fill="x", padx=10, pady=5)

        # a, b, eps, max_iter
        row0 = ttk.Frame(param_frame)
        row0.pack(fill="x", pady=2)
        ttk.Label(row0, text="a (левая граница):").pack(side="left", padx=5)
        self.a_entry = ttk.Entry(row0, width=10)
        self.a_entry.pack(side="left", padx=5)
        self.a_entry.insert(0, "0")
        ttk.Label(row0, text="b (правая граница):").pack(side="left", padx=5)
        self.b_entry = ttk.Entry(row0, width=10)
        self.b_entry.pack(side="left", padx=5)
        self.b_entry.insert(0, "2")

        row1 = ttk.Frame(param_frame)
        row1.pack(fill="x", pady=2)
        ttk.Label(row1, text="Точность (ε):").pack(side="left", padx=5)
        self.eps_entry = ttk.Entry(row1, width=10)
        self.eps_entry.pack(side="left", padx=5)
        self.eps_entry.insert(0, "1e-6")
        ttk.Label(row1, text="Макс. итераций:").pack(side="left", padx=5)
        self.max_iter_entry = ttk.Entry(row1, width=10)
        self.max_iter_entry.pack(side="left", padx=5)
        self.max_iter_entry.insert(0, "100")

        # Кнопка "Решить"
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(btn_frame, text="Решить уравнение", command=self.solve).pack()

        # Область вывода результата
        result_frame = ttk.LabelFrame(self.root, text="Результат", padding=10)
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.result_text = scrolledtext.ScrolledText(result_frame, height=12, font=("Courier", 9))
        self.result_text.pack(fill="both", expand=True)

        # Пояснение
        note = ttk.Label(self.root,
                         text="Примечание: для метода половинного деления требуется f(a)*f(b) < 0.\n"
                              "Доступные функции: sin, cos, tan, asin, acos, atan, sinh, cosh, tanh, exp, log, log10, sqrt, abs, pi, e.",
                         foreground="gray", wraplength=700)
        note.pack(pady=2)

    def solve(self):
        # Получаем данные
        method_name = self.method_var.get()
        solver = SOLVER_METHODS.get(method_name)
        if not solver:
            messagebox.showerror("Ошибка", "Метод не найден")
            return

        expr = self.func_entry.get().strip()
        if not expr:
            messagebox.showerror("Ошибка", "Введите выражение f(x)")
            return

        try:
            a = float(self.a_entry.get().strip())
            b = float(self.b_entry.get().strip())
            eps = float(self.eps_entry.get().strip())
            max_iter = int(self.max_iter_entry.get().strip())
        except ValueError:
            messagebox.showerror("Ошибка", "Неверные числовые параметры")
            return

        # Создаём функцию f(x)
        try:
            f = make_function(expr)
        except Exception as e:
            messagebox.showerror("Ошибка в выражении", str(e))
            return

        # Проверяем знаки на концах (для метода половинного деления)
        if method_name == "Метод половинного деления":
            try:
                fa = f(a)
                fb = f(b)
            except Exception as e:
                messagebox.showerror("Ошибка вычисления", f"Не удалось вычислить f(a) или f(b): {e}")
                return
            if fa * fb > 0:
                messagebox.showerror("Неподходящий интервал", f"f({a})={fa}, f({b})={fb}. На интервале нет смены знака. Выберите a и b так, чтобы f(a) и f(b) имели разные знаки.")
                return

        # Решаем
        result = None
        iterations = None
        error_msg = None
        try:
            # В зависимости от метода вызываем с нужными параметрами
            if method_name == "Метод половинного деления":
                result, iterations, error_msg = solver(f, a, b, eps, max_iter)
            else:
                # Для других методов нужно расширить
                result = solver(f, a, b, eps, max_iter)
                error_msg = None
        except Exception as e:
            messagebox.showerror("Ошибка при решении", str(e))
            return

        # Вывод результата
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, f"Метод: {method_name}\n")
        self.result_text.insert(tk.END, f"Уравнение: f(x) = {expr}\n")
        self.result_text.insert(tk.END, f"Интервал: [{a}, {b}]\n")
        self.result_text.insert(tk.END, f"Точность: {eps}\n")
        self.result_text.insert(tk.END, f"Макс. итераций: {max_iter}\n\n")

        if error_msg:
            self.result_text.insert(tk.END, f"ОШИБКА: {error_msg}\n")
        elif result is not None:
            self.result_text.insert(tk.END, f"Найденный корень: {result:.10f}\n")
            try:
                f_res = f(result)
                self.result_text.insert(tk.END, f"Значение f(x) в корне: {f_res:.2e}\n")
            except:
                pass
            # Вывод итераций, если есть
            if iterations:
                self.result_text.insert(tk.END, "\nИтерации:\n")
                self.result_text.insert(tk.END, "№ |        a        |        b        |        c        |      f(c)\n")
                self.result_text.insert(tk.END, "-" * 70 + "\n")
                for it in iterations:
                    self.result_text.insert(tk.END, f"{it[0]:2} | {it[1]:15.8f} | {it[2]:15.8f} | {it[3]:15.8f} | {it[4]:12.4e}\n")
        else:
            self.result_text.insert(tk.END, "Не удалось найти корень.\n")

# ------------------ Запуск ------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = SolverApp(root)
    root.mainloop()