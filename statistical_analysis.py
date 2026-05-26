import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import math
from collections import Counter
import itertools

# ------------------ Базовые статистические функции ------------------
def mean(data):
    """Среднее арифметическое"""
    if not data:
        return None
    return sum(data) / len(data)

def median(data):
    """Медиана"""
    if not data:
        return None
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_data[mid-1] + sorted_data[mid]) / 2
    else:
        return sorted_data[mid]

def mode(data):
    """Мода (первое значение с максимальной частотой)"""
    if not data:
        return None
    counter = Counter(data)
    max_freq = max(counter.values())
    modes = [k for k, v in counter.items() if v == max_freq]
    return modes[0]  # возвращаем первое модальное значение

def variance(data, sample=True):
    """Дисперсия (sample=True - выборочная, False - генеральная)"""
    if len(data) < 2:
        return None
    m = mean(data)
    squared_diffs = [(x - m) ** 2 for x in data]
    if sample:
        return sum(squared_diffs) / (len(data) - 1)
    else:
        return sum(squared_diffs) / len(data)

def std_dev(data, sample=True):
    """Среднеквадратичное отклонение"""
    var = variance(data, sample)
    return math.sqrt(var) if var is not None else None

def expectation(data):
    """Математическое ожидание (для выборки = среднее)"""
    return mean(data)

def covariance(data1, data2):
    """Ковариация двух выборок одинаковой длины"""
    if len(data1) != len(data2) or len(data1) == 0:
        return None
    m1 = mean(data1)
    m2 = mean(data2)
    n = len(data1)
    cov = sum((data1[i] - m1) * (data2[i] - m2) for i in range(n)) / (n - 1)
    return cov

def pearson_correlation(data1, data2):
    """Коэффициент корреляции Пирсона"""
    if len(data1) != len(data2) or len(data1) < 2:
        return None
    std1 = std_dev(data1, sample=True)
    std2 = std_dev(data2, sample=True)
    if std1 == 0 or std2 == 0:
        return None
    cov = covariance(data1, data2)
    return cov / (std1 * std2)

def linear_regression(data1, data2):
    """
    Простая линейная регрессия: y = a + b*x
    Возвращает (a, b, r2)
    """
    if len(data1) != len(data2) or len(data1) < 2:
        return None, None, None
    n = len(data1)
    x = data1
    y = data2
    mean_x = mean(x)
    mean_y = mean(y)
    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    denominator = sum((x[i] - mean_x) ** 2 for i in range(n))
    if denominator == 0:
        return None, None, None
    b = numerator / denominator
    a = mean_y - b * mean_x
    # Коэффициент детерминации R^2
    ss_res = sum((y[i] - (a + b * x[i])) ** 2 for i in range(n))
    ss_tot = sum((y[i] - mean_y) ** 2 for i in range(n))
    r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else None
    return a, b, r2

# ------------------ Регистрация методов ------------------
class StatMethod:
    def __init__(self, name, func, requires_two_series=False):
        self.name = name
        self.func = func
        self.requires_two_series = requires_two_series

# Словарь доступных методов (можно расширять)
AVAILABLE_METHODS = {
    "Среднее арифметическое": StatMethod("Среднее арифметическое", mean, False),
    "Медиана": StatMethod("Медиана", median, False),
    "Мода": StatMethod("Мода", mode, False),
    "Дисперсия (выборочная)": StatMethod("Дисперсия (выборочная)", variance, False),
    "Среднеквадратичное отклонение (выборочное)": StatMethod("Среднеквадратичное отклонение (выборочное)", std_dev, False),
    "Математическое ожидание": StatMethod("Математическое ожидание", expectation, False),
    "Ковариация": StatMethod("Ковариация", covariance, True),
    "Корреляция Пирсона": StatMethod("Корреляция Пирсона", pearson_correlation, True),
    "Линейная регрессия (y = a + b*x)": StatMethod("Линейная регрессия", linear_regression, True),
}

# ------------------ GUI приложения ------------------
class StatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Статистический анализ данных")
        self.root.geometry("800x650")

        # Переменные для ввода
        self.data_type = tk.StringVar(value="one")  # one или two
        self.selected_method = tk.StringVar(value=list(AVAILABLE_METHODS.keys())[0])

        self.create_widgets()

    def create_widgets(self):
        # Выбор типа данных (один или два ряда)
        type_frame = ttk.LabelFrame(self.root, text="Тип данных", padding=10)
        type_frame.pack(fill="x", padx=10, pady=5)
        ttk.Radiobutton(type_frame, text="Один ряд чисел", variable=self.data_type, value="one", command=self.toggle_data_input).pack(anchor="w")
        ttk.Radiobutton(type_frame, text="Два ряда чисел (X и Y)", variable=self.data_type, value="two", command=self.toggle_data_input).pack(anchor="w")

        # Фрейм для ввода данных
        self.input_frame = ttk.Frame(self.root)
        self.input_frame.pack(fill="x", padx=10, pady=5)

        # Один ряд
        self.frame_one = ttk.Frame(self.input_frame)
        ttk.Label(self.frame_one, text="Введите числа (через пробел, запятую или точку с запятой):").pack(anchor="w")
        self.text_one = scrolledtext.ScrolledText(self.frame_one, height=5, width=70)
        self.text_one.pack(fill="x", pady=5)
        self.text_one.insert("1.0", "10 20 30 40 50")

        # Два ряда
        self.frame_two = ttk.Frame(self.input_frame)
        ttk.Label(self.frame_two, text="Ряд X (независимая переменная):").pack(anchor="w")
        self.text_x = scrolledtext.ScrolledText(self.frame_two, height=4, width=70)
        self.text_x.pack(fill="x", pady=2)
        self.text_x.insert("1.0", "1 2 3 4 5")
        ttk.Label(self.frame_two, text="Ряд Y (зависимая переменная):").pack(anchor="w")
        self.text_y = scrolledtext.ScrolledText(self.frame_two, height=4, width=70)
        self.text_y.pack(fill="x", pady=2)
        self.text_y.insert("1.0", "2 4 6 8 10")

        self.frame_one.pack(fill="x")
        self.frame_two.pack_forget()  # изначально скрыт

        # Выбор статистического метода
        method_frame = ttk.LabelFrame(self.root, text="Статистический метод", padding=10)
        method_frame.pack(fill="x", padx=10, pady=5)

        self.method_combo = ttk.Combobox(method_frame, textvariable=self.selected_method, values=list(AVAILABLE_METHODS.keys()), state="readonly", width=40)
        self.method_combo.pack(fill="x", pady=5)
        self.method_combo.bind("<<ComboboxSelected>>", self.on_method_changed)

        # Кнопка "Вычислить"
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(btn_frame, text="Вычислить", command=self.calculate).pack()

        # Результат
        result_frame = ttk.LabelFrame(self.root, text="Результат", padding=10)
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.result_text = scrolledtext.ScrolledText(result_frame, height=12, width=80, font=("Courier", 10))
        self.result_text.pack(fill="both", expand=True)

        # Пояснение о расширяемости
        note = ttk.Label(self.root, text="Примечание: новые методы можно добавить в словарь AVAILABLE_METHODS в коде.",
                         foreground="gray", font=("Arial", 8))
        note.pack(pady=2)

    def toggle_data_input(self):
        """Показывает/скрывает поля ввода в зависимости от выбора типа данных"""
        if self.data_type.get() == "one":
            self.frame_one.pack(fill="x")
            self.frame_two.pack_forget()
        else:
            self.frame_one.pack_forget()
            self.frame_two.pack(fill="x")

    def on_method_changed(self, event=None):
        """Обновляет предупреждение, если метод требует два ряда"""
        method_name = self.selected_method.get()
        method = AVAILABLE_METHODS.get(method_name)
        if method and method.requires_two_series and self.data_type.get() == "one":
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert("1.0", "⚠️ Внимание: выбранный метод требует двух рядов данных.\nПереключитесь на 'Два ряда чисел'.")
        else:
            self.result_text.delete("1.0", tk.END)

    def parse_numbers(self, text):
        """Преобразует текст в список чисел (поддерживает разделители: пробел, запятая, точка с запятой)"""
        import re
        numbers = re.split(r'[ ,;]+', text.strip())
        result = []
        for num in numbers:
            if num:
                try:
                    result.append(float(num))
                except ValueError:
                    pass
        return result

    def calculate(self):
        """Основная логика вычислений"""
        method_name = self.selected_method.get()
        method = AVAILABLE_METHODS.get(method_name)
        if not method:
            messagebox.showerror("Ошибка", "Метод не найден")
            return

        # Парсим данные
        if self.data_type.get() == "one":
            data_text = self.text_one.get("1.0", tk.END)
            data = self.parse_numbers(data_text)
            if len(data) == 0:
                messagebox.showerror("Ошибка", "Введите хотя бы одно число")
                return
            if method.requires_two_series:
                messagebox.showerror("Ошибка", f"Метод '{method_name}' требует два ряда данных. Переключитесь на 'Два ряда чисел'.")
                return
            # Вычисляем
            try:
                result = method.func(data)
                self.display_result_one(method_name, data, result)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка вычисления: {str(e)}")
        else:  # два ряда
            x_text = self.text_x.get("1.0", tk.END)
            y_text = self.text_y.get("1.0", tk.END)
            x = self.parse_numbers(x_text)
            y = self.parse_numbers(y_text)
            if len(x) == 0 or len(y) == 0:
                messagebox.showerror("Ошибка", "Введите хотя бы одно число в каждый ряд")
                return
            if len(x) != len(y):
                messagebox.showerror("Ошибка", f"Длины рядов не совпадают: X={len(x)}, Y={len(y)}")
                return
            if len(x) < 2 and method_name in ["Ковариация", "Корреляция Пирсона", "Линейная регрессия"]:
                messagebox.showerror("Ошибка", f"Для метода '{method_name}' нужно не менее 2 пар значений")
                return
            try:
                result = method.func(x, y)
                self.display_result_two(method_name, x, y, result)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка вычисления: {str(e)}")

    def display_result_one(self, method_name, data, result):
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", f"Метод: {method_name}\n")
        self.result_text.insert(tk.END, f"Данные (n={len(data)}): {data}\n\n")
        if result is None:
            self.result_text.insert(tk.END, "Результат: невозможно вычислить (недостаточно данных).\n")
        else:
            # Форматирование числа
            if isinstance(result, float):
                formatted = f"{result:.6f}".rstrip('0').rstrip('.') if result != int(result) else str(int(result))
            else:
                formatted = str(result)
            self.result_text.insert(tk.END, f"Результат: {formatted}\n")

    def display_result_two(self, method_name, x, y, result):
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", f"Метод: {method_name}\n")
        self.result_text.insert(tk.END, f"Ряд X (n={len(x)}): {x}\n")
        self.result_text.insert(tk.END, f"Ряд Y (n={len(y)}): {y}\n\n")
        if method_name == "Линейная регрессия (y = a + b*x)":
            a, b, r2 = result
            if a is None:
                self.result_text.insert(tk.END, "Невозможно вычислить регрессию (недостаточно вариации данных).\n")
            else:
                self.result_text.insert(tk.END, f"Коэффициент a (свободный член): {a:.6f}\n")
                self.result_text.insert(tk.END, f"Коэффициент b (наклон): {b:.6f}\n")
                self.result_text.insert(tk.END, f"Уравнение: y = {a:.4f} + {b:.4f} * x\n")
                if r2 is not None:
                    self.result_text.insert(tk.END, f"Коэффициент детерминации R²: {r2:.6f}\n")
        else:
            if result is None:
                self.result_text.insert(tk.END, "Результат: невозможно вычислить.\n")
            else:
                if isinstance(result, float):
                    formatted = f"{result:.6f}".rstrip('0').rstrip('.') if result != int(result) else str(int(result))
                else:
                    formatted = str(result)
                self.result_text.insert(tk.END, f"Результат: {formatted}\n")

# ------------------ Запуск ------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = StatApp(root)
    root.mainloop()