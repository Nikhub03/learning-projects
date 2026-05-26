import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# ------------------ Матричные операции ------------------
def parse_matrix(text):
    """
    Преобразует текст в матрицу (список списков).
    Формат: строки разделены точкой с запятой ';', числа в строке - пробелами или запятыми.
    Пример: "1 2 3; 4 5 6"
    """
    rows = text.strip().split(';')
    matrix = []
    for row in rows:
        # Разделяем числа по пробелам или запятым
        numbers = row.replace(',', ' ').split()
        if not numbers:
            continue
        row_numbers = []
        for num in numbers:
            try:
                row_numbers.append(float(num))
            except ValueError:
                raise ValueError(f"Некорректное число: {num}")
        matrix.append(row_numbers)
    if not matrix:
        raise ValueError("Матрица не содержит данных")
    # Проверка, что все строки одинаковой длины
    ncols = len(matrix[0])
    for i, row in enumerate(matrix):
        if len(row) != ncols:
            raise ValueError(f"Строка {i+1} имеет {len(row)} элементов, ожидалось {ncols}")
    return matrix

def matrix_to_string(matrix):
    """Преобразует матрицу в удобочитаемую строку"""
    if not matrix:
        return "[]"
    return "\n".join([" ".join(f"{x:8.4f}" for x in row) for row in matrix])

def matrix_add(A, B):
    """Сложение матриц A и B"""
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        raise ValueError("Размерности матриц не совпадают для сложения")
    result = [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
    return result

def matrix_multiply(A, B):
    """Умножение матриц A * B"""
    if len(A[0]) != len(B):
        raise ValueError("Число столбцов A не равно числу строк B")
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            total = 0
            for k in range(cols_A):
                total += A[i][k] * B[k][j]
            result[i][j] = total
    return result

# ------------------ Регистрация операций ------------------
class MatrixOperation:
    def __init__(self, name, func, needs_two=True):
        self.name = name
        self.func = func   # принимает (A, B) или (A,) для унарных
        self.needs_two = needs_two  # бинарная или унарная операция

# Словарь доступных операций (можно расширять)
OPERATIONS = {
    "Сложение матриц": MatrixOperation("Сложение матриц", matrix_add, needs_two=True),
    "Умножение матриц": MatrixOperation("Умножение матриц", matrix_multiply, needs_two=True),
    # Примеры дополнительных операций (раскомментируйте для добавления):
    # "Вычитание матриц": MatrixOperation("Вычитание матриц", matrix_subtract, needs_two=True),
    # "Транспонирование (матрица A)": MatrixOperation("Транспонирование", matrix_transpose, needs_two=False),
    # "Умножение на скаляр (матрица A)": MatrixOperation("Умножение на скаляр", matrix_scalar_multiply, needs_two=False),
}

# Дополнительные операции (раскомментируйте при необходимости)
def matrix_subtract(A, B):
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        raise ValueError("Размерности матриц не совпадают для вычитания")
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_transpose(A):
    return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]

def matrix_scalar_multiply(A, scalar):
    return [[x * scalar for x in row] for row in A]

# ------------------ GUI приложения ------------------
class MatrixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Операции линейной алгебры (матрицы)")
        self.root.geometry("750x650")

        self.selected_op = tk.StringVar(value=list(OPERATIONS.keys())[0] if OPERATIONS else "")
        self.create_widgets()

    def create_widgets(self):
        # Выбор операции
        op_frame = ttk.LabelFrame(self.root, text="Выберите операцию", padding=10)
        op_frame.pack(fill="x", padx=10, pady=5)
        self.op_combo = ttk.Combobox(op_frame, textvariable=self.selected_op, values=list(OPERATIONS.keys()),
                                     state="readonly", width=40)
        self.op_combo.pack(fill="x", pady=5)
        self.op_combo.bind("<<ComboboxSelected>>", self.on_op_changed)

        # Фрейм для матриц (будет меняться в зависимости от бинарности операции)
        self.matrix_frame = ttk.Frame(self.root)
        self.matrix_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # По умолчанию показываем две матрицы (бинарная операция)
        self.show_two_matrices()

        # Кнопка "Вычислить"
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(btn_frame, text="Вычислить", command=self.calculate).pack()

        # Область результата
        result_frame = ttk.LabelFrame(self.root, text="Результат", padding=10)
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.result_text = scrolledtext.ScrolledText(result_frame, height=8, font=("Courier", 10))
        self.result_text.pack(fill="both", expand=True)

        # Пояснение по формату
        help_label = ttk.Label(self.root,
                               text="Формат ввода: строки разделяются точкой с запятой (;), числа в строке — пробелами или запятыми.\n"
                                    "Пример: 1 2 3; 4 5 6",
                               foreground="gray", justify="left", wraplength=700)
        help_label.pack(pady=2)

    def show_two_matrices(self):
        """Отображает поля для двух матриц"""
        # Очищаем matrix_frame
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        # Матрица A
        frameA = ttk.LabelFrame(self.matrix_frame, text="Матрица A", padding=5)
        frameA.pack(side="left", fill="both", expand=True, padx=5)
        self.textA = scrolledtext.ScrolledText(frameA, height=10, width=30)
        self.textA.pack(fill="both", expand=True)
        self.textA.insert("1.0", "1 2 3; 4 5 6")

        # Матрица B
        frameB = ttk.LabelFrame(self.matrix_frame, text="Матрица B", padding=5)
        frameB.pack(side="right", fill="both", expand=True, padx=5)
        self.textB = scrolledtext.ScrolledText(frameB, height=10, width=30)
        self.textB.pack(fill="both", expand=True)
        self.textB.insert("1.0", "7 8; 9 10; 11 12")  # для умножения 2x3 * 3x2

    def show_one_matrix(self):
        """Отображает поле для одной матрицы (унарные операции)"""
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        frameA = ttk.LabelFrame(self.matrix_frame, text="Матрица A", padding=5)
        frameA.pack(fill="both", expand=True, padx=5)
        self.textA = scrolledtext.ScrolledText(frameA, height=10, width=60)
        self.textA.pack(fill="both", expand=True)
        self.textA.insert("1.0", "1 2 3; 4 5 6")
        # Скрываем поле для B
        self.textB = None

    def on_op_changed(self, event=None):
        op_name = self.selected_op.get()
        op = OPERATIONS.get(op_name)
        if op and not op.needs_two:
            self.show_one_matrix()
        else:
            self.show_two_matrices()

    def get_matrix_from_text(self, text_widget):
        """Возвращает матрицу из виджета, выдаёт исключение при ошибке"""
        raw = text_widget.get("1.0", tk.END)
        return parse_matrix(raw)

    def calculate(self):
        op_name = self.selected_op.get()
        op = OPERATIONS.get(op_name)
        if not op:
            messagebox.showerror("Ошибка", "Операция не выбрана")
            return

        self.result_text.delete("1.0", tk.END)
        try:
            if op.needs_two:
                if not self.textB:
                    raise ValueError("Для этой операции нужны две матрицы, но интерфейс не настроен")
                A = self.get_matrix_from_text(self.textA)
                B = self.get_matrix_from_text(self.textB)
                result = op.func(A, B)
                self.result_text.insert(tk.END, f"Матрица A:\n{matrix_to_string(A)}\n\n")
                self.result_text.insert(tk.END, f"Матрица B:\n{matrix_to_string(B)}\n\n")
                self.result_text.insert(tk.END, f"Результат {op.name}:\n{matrix_to_string(result)}")
            else:
                A = self.get_matrix_from_text(self.textA)
                # Унарная функция может принимать разные параметры (для скаляра добавим диалог)
                # По умолчанию для унарных операций вызываем func(A)
                # Для умножения на скаляр нужен дополнительный ввод. Для простоты оставим заглушку.
                result = op.func(A)
                self.result_text.insert(tk.END, f"Матрица A:\n{matrix_to_string(A)}\n\n")
                self.result_text.insert(tk.END, f"Результат {op.name}:\n{matrix_to_string(result)}")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

# ------------------ Запуск ------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixApp(root)
    root.mainloop()