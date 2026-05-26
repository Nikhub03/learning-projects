import tkinter as tk
from tkinter import ttk, messagebox
import math
import random

def compute_intersection_area(a, R, cx, cy, num_points=500000):
    """
    Метод Монте-Карло: генерируем точки в квадрате [-a/2, a/2] x [-a/2, a/2]
    и считаем долю попавших в круг.
    """
    half = a / 2.0
    inside = 0
    for _ in range(num_points):
        x = random.uniform(-half, half)
        y = random.uniform(-half, half)
        if (x - cx)**2 + (y - cy)**2 <= R**2:
            inside += 1
    fraction = inside / num_points
    return fraction * a * a  # площадь пересечения

def calculate():
    try:
        R = float(entry_radius.get())
        cx = float(entry_cx.get())
        cy = float(entry_cy.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректные числа (радиус, координаты)")
        return

    if R <= 0:
        messagebox.showerror("Ошибка", "Радиус должен быть положительным")
        return

    # Сторона квадрата из условия: площадь круга в 3 раза меньше площади квадрата
    # S_circle = πR², S_square = a², πR² = a² / 3 → a² = 3πR² → a = R * sqrt(3π)
    a = R * math.sqrt(3 * math.pi)
    S_square = a * a
    S_circle = math.pi * R * R

    # Площадь пересечения круга и квадрата (квадрат с центром в (0,0))
    intersection = compute_intersection_area(a, R, cx, cy)
    percent = (intersection / S_square) * 100.0

    result_text = f"""Параметры:
Радиус круга: {R:.3f}
Центр круга: ({cx:.3f}, {cy:.3f})

Квадрат:
Сторона квадрата: {a:.3f}
Площадь квадрата: {S_square:.3f}
Площадь круга: {S_circle:.3f}

Пересечение:
Площадь пересечения круга и квадрата: {intersection:.3f}
Процент от площади квадрата: {percent:.2f}%

Примечание: квадрат расположен с центром в (0,0), сторона параллельна осям.
"""
    label_result.config(text=result_text)

# Создание GUI
root = tk.Tk()
root.title("Круг и квадрат – площадь пересечения")
root.geometry("550x500")
root.resizable(False, False)

frame_input = ttk.LabelFrame(root, text="Введите параметры круга", padding=10)
frame_input.pack(fill="x", padx=10, pady=5)

ttk.Label(frame_input, text="Радиус (R):").grid(row=0, column=0, sticky="e", padx=5, pady=5)
entry_radius = ttk.Entry(frame_input, width=15)
entry_radius.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_input, text="Координата X центра:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
entry_cx = ttk.Entry(frame_input, width=15)
entry_cx.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame_input, text="Координата Y центра:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
entry_cy = ttk.Entry(frame_input, width=15)
entry_cy.grid(row=2, column=1, padx=5, pady=5)

btn_calc = ttk.Button(frame_input, text="Вычислить", command=calculate)
btn_calc.grid(row=3, column=0, columnspan=2, pady=10)

# Результаты
frame_result = ttk.LabelFrame(root, text="Результат", padding=10)
frame_result.pack(fill="both", expand=True, padx=10, pady=5)

label_result = ttk.Label(frame_result, text="Введите данные и нажмите 'Вычислить'", justify="left", font=("Courier", 9))
label_result.pack(anchor="nw", fill="both", expand=True)

# Пояснение
note = ttk.Label(root, text="Примечание: квадрат зафиксирован с центром в (0,0) и стороной, параллельной осям.\n"
                            "Площадь квадрата определена из условия: S_круга = S_квадрата / 3.",
                 foreground="gray", justify="left", wraplength=530)
note.pack(pady=5)

root.mainloop()