import tkinter as tk
from tkinter import ttk
import math

class TriangleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Поворот треугольника")
        self.root.geometry("750x600")

        # Переменные для исходных координат вершин (float)
        self.x1 = tk.DoubleVar(value=100)
        self.y1 = tk.DoubleVar(value=50)
        self.x2 = tk.DoubleVar(value=200)
        self.y2 = tk.DoubleVar(value=150)
        self.x3 = tk.DoubleVar(value=50)
        self.y3 = tk.DoubleVar(value=150)

        # Угол поворота в градусах
        self.angle_deg = tk.IntVar(value=0)

        # Текущие повёрнутые координаты (будут пересчитываться)
        self.rx1 = tk.DoubleVar()
        self.ry1 = tk.DoubleVar()
        self.rx2 = tk.DoubleVar()
        self.ry2 = tk.DoubleVar()
        self.rx3 = tk.DoubleVar()
        self.ry3 = tk.DoubleVar()

        self.create_widgets()
        self.update_rotation()  # начальный расчёт

    def create_widgets(self):
        # Фрейм для ввода исходных координат
        input_frame = ttk.LabelFrame(self.root, text="Исходные координаты вершин", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        # Заголовки
        ttk.Label(input_frame, text="Вершина", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=2)
        ttk.Label(input_frame, text="X", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5)
        ttk.Label(input_frame, text="Y", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5)

        # Строка 1
        ttk.Label(input_frame, text="A").grid(row=1, column=0)
        self.entry_x1 = ttk.Entry(input_frame, textvariable=self.x1, width=8)
        self.entry_x1.grid(row=1, column=1, padx=5, pady=2)
        self.entry_y1 = ttk.Entry(input_frame, textvariable=self.y1, width=8)
        self.entry_y1.grid(row=1, column=2, padx=5, pady=2)

        # Строка 2
        ttk.Label(input_frame, text="B").grid(row=2, column=0)
        self.entry_x2 = ttk.Entry(input_frame, textvariable=self.x2, width=8)
        self.entry_x2.grid(row=2, column=1, padx=5, pady=2)
        self.entry_y2 = ttk.Entry(input_frame, textvariable=self.y2, width=8)
        self.entry_y2.grid(row=2, column=2, padx=5, pady=2)

        # Строка 3
        ttk.Label(input_frame, text="C").grid(row=3, column=0)
        self.entry_x3 = ttk.Entry(input_frame, textvariable=self.x3, width=8)
        self.entry_x3.grid(row=3, column=1, padx=5, pady=2)
        self.entry_y3 = ttk.Entry(input_frame, textvariable=self.y3, width=8)
        self.entry_y3.grid(row=3, column=2, padx=5, pady=2)

        # Привязываем события изменения полей для автоматического пересчёта
        for var in [self.x1, self.y1, self.x2, self.y2, self.x3, self.y3]:
            var.trace_add("write", lambda *args: self.update_rotation())

        # Фрейм для угла поворота
        angle_frame = ttk.LabelFrame(self.root, text="Угол поворота (градусы)", padding=10)
        angle_frame.pack(fill="x", padx=10, pady=5)

        self.angle_scale = ttk.Scale(angle_frame, from_=0, to=360, variable=self.angle_deg,
                                     orient="horizontal", command=self.on_angle_change)
        self.angle_scale.pack(fill="x", padx=5, pady=5)

        self.angle_label = ttk.Label(angle_frame, text="0°")
        self.angle_label.pack()

        # Фрейм для результатов (повёрнутые координаты)
        result_frame = ttk.LabelFrame(self.root, text="Повёрнутые координаты", padding=10)
        result_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(result_frame, text="A':").grid(row=0, column=0, sticky="e", padx=5)
        self.label_rx1 = ttk.Label(result_frame, textvariable=self.rx1, width=10, relief="sunken")
        self.label_rx1.grid(row=0, column=1, padx=5)
        self.label_ry1 = ttk.Label(result_frame, textvariable=self.ry1, width=10, relief="sunken")
        self.label_ry1.grid(row=0, column=2, padx=5)

        ttk.Label(result_frame, text="B':").grid(row=1, column=0, sticky="e", padx=5)
        self.label_rx2 = ttk.Label(result_frame, textvariable=self.rx2, width=10, relief="sunken")
        self.label_rx2.grid(row=1, column=1, padx=5)
        self.label_ry2 = ttk.Label(result_frame, textvariable=self.ry2, width=10, relief="sunken")
        self.label_ry2.grid(row=1, column=2, padx=5)

        ttk.Label(result_frame, text="C':").grid(row=2, column=0, sticky="e", padx=5)
        self.label_rx3 = ttk.Label(result_frame, textvariable=self.rx3, width=10, relief="sunken")
        self.label_rx3.grid(row=2, column=1, padx=5)
        self.label_ry3 = ttk.Label(result_frame, textvariable=self.ry3, width=10, relief="sunken")
        self.label_ry3.grid(row=2, column=2, padx=5)

        # Canvas для визуализации
        canvas_frame = ttk.LabelFrame(self.root, text="Визуализация", padding=10)
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.canvas = tk.Canvas(canvas_frame, bg="white", width=600, height=400)
        self.canvas.pack(fill="both", expand=True)

        # Настройка области отображения (масштаб и смещение)
        self.canvas.bind("<Configure>", self.on_canvas_resize)

    def on_angle_change(self, event=None):
        """Вызывается при движении слайдера."""
        angle = self.angle_deg.get()
        self.angle_label.config(text=f"{angle}°")
        self.update_rotation()

    def update_rotation(self):
        """Пересчитывает повёрнутые координаты и обновляет canvas."""
        try:
            # Получаем исходные координаты
            pts = [(self.x1.get(), self.y1.get()),
                   (self.x2.get(), self.y2.get()),
                   (self.x3.get(), self.y3.get())]
        except tk.TclError:
            return  # если в полях ввода некорректные значения

        # Центр треугольника (среднее арифметическое)
        cx = sum(p[0] for p in pts) / 3
        cy = sum(p[1] for p in pts) / 3

        # Угол в радианах
        angle_rad = math.radians(self.angle_deg.get())
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        rotated = []
        for x, y in pts:
            # Смещение относительно центра
            dx = x - cx
            dy = y - cy
            # Поворот
            new_x = cx + dx * cos_a - dy * sin_a
            new_y = cy + dx * sin_a + dy * cos_a
            rotated.append((new_x, new_y))

        # Обновляем переменные для отображения
        self.rx1.set(round(rotated[0][0], 2))
        self.ry1.set(round(rotated[0][1], 2))
        self.rx2.set(round(rotated[1][0], 2))
        self.ry2.set(round(rotated[1][1], 2))
        self.rx3.set(round(rotated[2][0], 2))
        self.ry3.set(round(rotated[2][1], 2))

        # Перерисовываем canvas
        self.draw_triangles(pts, rotated)

    def draw_triangles(self, original, rotated):
        """Рисует исходный (серый) и повёрнутый (красный) треугольники."""
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 10 or h < 10:
            return

        # Функция преобразования координат: ось Y перевёрнута (вниз) и масштабирование
        # Находим минимумы и максимумы для всех точек
        all_x = [p[0] for p in original] + [p[0] for p in rotated]
        all_y = [p[1] for p in original] + [p[1] for p in rotated]
        if not all_x:
            return
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        # Добавляем поля
        margin = 30
        range_x = max_x - min_x if max_x != min_x else 1
        range_y = max_y - min_y if max_y != min_y else 1
        scale_x = (w - 2 * margin) / range_x
        scale_y = (h - 2 * margin) / range_y
        scale = min(scale_x, scale_y)

        def to_canvas(x, y):
            cx = margin + (x - min_x) * scale
            cy = h - margin - (y - min_y) * scale
            return cx, cy

        # Рисуем исходный треугольник (серый, пунктир)
        pts_original = [to_canvas(x, y) for x, y in original]
        if len(pts_original) == 3:
            self.canvas.create_polygon(pts_original, outline="gray", fill="lightgray", width=2, dash=(5,2))

        # Рисуем повёрнутый треугольник (красный)
        pts_rotated = [to_canvas(x, y) for x, y in rotated]
        if len(pts_rotated) == 3:
            self.canvas.create_polygon(pts_rotated, outline="red", fill="", width=2)

        # Подписи
        self.canvas.create_text(10, 10, text="Исходный (серый) → Повёрнутый (красный)", anchor="nw", fill="black")

    def on_canvas_resize(self, event):
        """Перерисовываем при изменении размера окна."""
        self.update_rotation()

if __name__ == "__main__":
    root = tk.Tk()
    app = TriangleApp(root)
    root.mainloop()