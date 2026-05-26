import tkinter as tk
from tkinter import ttk, messagebox
import math

# ------------------ Базовый класс для всех фигур ------------------
class Shape:
    """Абстрактный класс для пространственных фигур."""
    name = "Фигура"

    @staticmethod
    def get_input_fields():
        """Возвращает список кортежей (имя_параметра, единица_измерения, подсказка)."""
        return []

    def set_params(self, **kwargs):
        """Устанавливает параметры фигуры."""
        self.params = kwargs

    def volume(self):
        """Возвращает объём фигуры. Должен быть переопределён в наследниках."""
        raise NotImplementedError

# ------------------ Конкретные фигуры ------------------
class Cube(Shape):
    name = "Куб"

    @staticmethod
    def get_input_fields():
        return [("a", "см", "Длина ребра")]

    def volume(self):
        a = self.params.get("a", 0)
        return a ** 3

class Sphere(Shape):
    name = "Шар"

    @staticmethod
    def get_input_fields():
        return [("r", "см", "Радиус")]

    def volume(self):
        r = self.params.get("r", 0)
        return (4/3) * math.pi * r ** 3

# Пример добавления новой фигуры (раскомментируйте для использования):
# class Cylinder(Shape):
#     name = "Цилиндр"
#
#     @staticmethod
#     def get_input_fields():
#         return [("r", "см", "Радиус основания"), ("h", "см", "Высота")]
#
#     def volume(self):
#         r = self.params.get("r", 0)
#         h = self.params.get("h", 0)
#         return math.pi * r * r * h

# Регистрация всех доступных фигур (словарь для расширения)
SHAPES = {
    "Куб": Cube,
    "Шар": Sphere,
    # "Цилиндр": Cylinder,   # раскомментируйте после добавления класса
}

# ------------------ GUI приложения ------------------
class VolumeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Вычисление объёмов пространственных фигур")
        self.root.geometry("500x350")
        self.root.resizable(False, False)

        self.current_shape = None          # текущий выбранный класс фигуры
        self.param_entries = {}            # словарь для хранения полей ввода (имя -> виджет)

        self.create_widgets()
        self.on_shape_selected()           # инициализация полей по умолчанию

    def create_widgets(self):
        # Выбор фигуры
        shape_frame = ttk.LabelFrame(self.root, text="Выберите фигуру", padding=10)
        shape_frame.pack(fill="x", padx=10, pady=5)

        self.shape_var = tk.StringVar(value=list(SHAPES.keys())[0])
        self.shape_combo = ttk.Combobox(shape_frame, textvariable=self.shape_var,
                                        values=list(SHAPES.keys()),
                                        state="readonly", width=30)
        self.shape_combo.pack(pady=5)
        self.shape_combo.bind("<<ComboboxSelected>>", lambda e: self.on_shape_selected())

        # Динамическая область для ввода параметров
        self.params_frame = ttk.LabelFrame(self.root, text="Параметры фигуры", padding=10)
        self.params_frame.pack(fill="x", padx=10, pady=5)

        # Кнопка вычисления
        self.calc_btn = ttk.Button(self.root, text="Вычислить объём", command=self.calculate)
        self.calc_btn.pack(pady=10)

        # Область результата
        result_frame = ttk.LabelFrame(self.root, text="Результат", padding=10)
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.result_label = ttk.Label(result_frame, text="", font=("Courier", 14, "bold"), foreground="blue")
        self.result_label.pack(pady=10)

        # Пояснение о расширяемости
        note = ttk.Label(self.root,
                         text="Примечание: новые фигуры можно добавить в словарь SHAPES, создав класс-наследник Shape.\n"
                              "Пример: класс Cylinder с методами get_input_fields() и volume().",
                         foreground="gray", wraplength=480, justify="center")
        note.pack(pady=5)

    def on_shape_selected(self):
        """Обработчик смены фигуры: перестраивает поля ввода."""
        shape_name = self.shape_var.get()
        shape_class = SHAPES.get(shape_name)
        if not shape_class:
            return

        self.current_shape = shape_class

        # Очищаем старые виджеты
        for widget in self.params_frame.winfo_children():
            widget.destroy()

        self.param_entries.clear()

        # Создаём новые поля согласно get_input_fields()
        fields = shape_class.get_input_fields()
        if not fields:
            ttk.Label(self.params_frame, text="Нет параметров").pack()
        else:
            for field_name, unit, label_text in fields:
                frame = ttk.Frame(self.params_frame)
                frame.pack(fill="x", pady=2)

                ttk.Label(frame, text=f"{label_text} ({unit}):", width=15, anchor="e").pack(side="left", padx=5)
                entry = ttk.Entry(frame, width=15)
                entry.pack(side="left", padx=5)
                self.param_entries[field_name] = entry

    def calculate(self):
        """Считывает параметры, создаёт экземпляр фигуры, вычисляет объём."""
        if not self.current_shape:
            messagebox.showerror("Ошибка", "Фигура не выбрана")
            return

        # Собираем параметры
        params = {}
        for field_name, entry in self.param_entries.items():
            value_str = entry.get().strip()
            if not value_str:
                messagebox.showerror("Ошибка", f"Введите значение для '{field_name}'")
                return
            try:
                value = float(value_str)
                if value < 0:
                    raise ValueError
                params[field_name] = value
            except ValueError:
                messagebox.showerror("Ошибка", f"Значение '{field_name}' должно быть неотрицательным числом")
                return

        # Создаём экземпляр и вычисляем объём
        try:
            shape_instance = self.current_shape()
            shape_instance.set_params(**params)
            vol = shape_instance.volume()
            # Форматируем вывод
            vol_str = f"{vol:.4f}".rstrip('0').rstrip('.') if vol != int(vol) else str(int(vol))
            shape_name = self.shape_var.get()
            # Строим строку параметров для вывода
            params_str = ", ".join([f"{k}={v}" for k, v in params.items()])
            self.result_label.config(text=f"{shape_name} ({params_str}) → Объём = {vol_str} куб. ед.")
        except Exception as e:
            messagebox.showerror("Ошибка вычисления", str(e))

# ------------------ Запуск ------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = VolumeApp(root)
    root.mainloop()