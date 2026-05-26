import tkinter as tk
from tkinter import ttk, messagebox

# ------------------ Основные функции перевода ------------------
def decimal_to_base(n: int, base: int) -> str:
    """Переводит целое неотрицательное десятичное число в систему с основанием base (2 <= base <= 36)."""
    if n == 0:
        return "0"
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    res = ""
    while n > 0:
        res = digits[n % base] + res
        n //= base
    return res

def base_to_decimal(s: str, base: int) -> int:
    """Переводит строку (цифры/буквы) из системы base в десятичное число."""
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    s = s.upper().strip()
    value = 0
    for ch in s:
        if ch not in digits[:base]:
            raise ValueError(f"Символ '{ch}' недопустим для системы с основанием {base}")
        value = value * base + digits.index(ch)
    return value

# ------------------ Регистрация систем счисления ------------------
# Словарь: название системы -> основание
# Можно легко добавлять новые системы, просто дописав сюда запись.
NUMERAL_SYSTEMS = {
    "Двоичная (2)": 2,
    "Троичная (3)": 3,
    "Восьмеричная (8)": 8,
    "Десятичная (10)": 10,   # для полноты, хотя ввод и так десятичный
    "Шестнадцатеричная (16)": 16,
    "Двадцатеричная (20)": 20,
    "Тридцатишестиричная (36)": 36,
}

# ------------------ GUI приложения ------------------
class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Перевод систем счисления")
        self.root.geometry("500x300")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        # Рамка ввода десятичного числа
        input_frame = ttk.LabelFrame(self.root, text="Входное число (десятичное)", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        self.num_entry = ttk.Entry(input_frame, width=30, font=("Courier", 12))
        self.num_entry.pack(fill="x", pady=5)
        self.num_entry.insert(0, "42")

        # Рамка выбора системы счисления
        sys_frame = ttk.LabelFrame(self.root, text="Целевая система счисления", padding=10)
        sys_frame.pack(fill="x", padx=10, pady=5)

        self.sys_var = tk.StringVar(value=list(NUMERAL_SYSTEMS.keys())[0])
        self.sys_combo = ttk.Combobox(sys_frame, textvariable=self.sys_var,
                                      values=list(NUMERAL_SYSTEMS.keys()),
                                      state="readonly", width=30)
        self.sys_combo.pack(pady=5)

        # Кнопка перевода
        self.convert_btn = ttk.Button(self.root, text="Перевести", command=self.convert)
        self.convert_btn.pack(pady=10)

        # Рамка результата
        result_frame = ttk.LabelFrame(self.root, text="Результат", padding=10)
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.result_label = ttk.Label(result_frame, text="", font=("Courier", 14, "bold"), foreground="blue")
        self.result_label.pack(pady=10)

        # Пояснение по расширяемости
        note = ttk.Label(self.root,
                         text="Примечание: новые системы счисления можно добавить в словарь NUMERAL_SYSTEMS в коде.\n"
                              "Основание должно быть от 2 до 36.",
                         foreground="gray", wraplength=480, justify="center")
        note.pack(pady=5)

    def convert(self):
        num_str = self.num_entry.get().strip()
        if not num_str:
            messagebox.showerror("Ошибка", "Введите десятичное число")
            return

        # Проверяем, что введено целое неотрицательное число
        try:
            num = int(num_str)
            if num < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целое неотрицательное число (0, 1, 2, ...)")
            return

        selected_system = self.sys_var.get()
        base = NUMERAL_SYSTEMS.get(selected_system)
        if base is None:
            messagebox.showerror("Ошибка", "Система счисления не найдена")
            return

        # Перевод
        result = decimal_to_base(num, base)
        self.result_label.config(text=f"{num}₁₀ = {result}_{base}")

# ------------------ Демонстрация расширяемости ------------------
# Чтобы добавить новую систему, просто добавьте запись в словарь NUMERAL_SYSTEMS, например:
# NUMERAL_SYSTEMS["Пятеричная (5)"] = 5
# NUMERAL_SYSTEMS["Двенадцатеричная (12)"] = 12
# Это не требует изменения остального кода.

# ------------------ Запуск ------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()