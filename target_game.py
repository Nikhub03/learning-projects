import tkinter as tk
from tkinter import simpledialog, messagebox
import math

def get_ring_number(x, y, R):
    """
    Определяет номер кольца для точки (x, y) внутри круга радиуса R.
    Нумерация от внешнего края к центру: 1 (внешнее) ... 10 (центр).
    """
    dist = math.hypot(x, y)  # расстояние от центра (0,0)
    if dist > R:
        return 0  # мимо
    # Ищем минимальное i (1..10), такое что dist <= i * R/10
    for i in range(1, 11):
        if dist <= i * R / 10:
            return 11 - i  # 11-1=10, 11-2=9, ..., 11-10=1
    return 0

def main():
    root = tk.Tk()
    root.withdraw()  # скрываем главное окно, оставляем только диалоги

    # Параметры мишени
    a = 10.0           # сторона квадрата
    R = a / 2.0        # радиус мишени

    # Ввод количества игроков и попыток
    try:
        num_players = simpledialog.askinteger("Игра 'Мишень'", "Введите количество игроков:", minvalue=1)
        if num_players is None:
            return
        num_attempts = simpledialog.askinteger("Игра 'Мишень'", "Введите количество попыток для каждого игрока:", minvalue=1)
        if num_attempts is None:
            return
    except:
        messagebox.showerror("Ошибка", "Некорректный ввод")
        return

    scores = [0] * num_players

    # Игровой цикл
    for player in range(num_players):
        messagebox.showinfo("Новый игрок", f"Игрок {player+1}. Начинайте стрельбу!")
        player_score = 0
        for attempt in range(num_attempts):
            # Ввод координат
            coords = simpledialog.askstring(f"Игрок {player+1}, попытка {attempt+1}",
                                            "Введите координаты x и y через пробел\n(квадрат от -5 до 5):")
            if coords is None:
                # пользователь закрыл диалог – завершаем игру
                return
            try:
                x_str, y_str = coords.split()
                x = float(x_str)
                y = float(y_str)
            except:
                messagebox.showerror("Ошибка", "Некорректный ввод координат. Попробуйте снова.")
                # Повторяем попытку
                attempt -= 1
                continue

            # Проверка границ квадрата (опционально)
            if abs(x) > R or abs(y) > R:
                messagebox.showwarning("Вне квадрата", f"Точка ({x},{y}) выходит за пределы квадрата. Попадание не засчитывается.")
                points = 0
            else:
                points = get_ring_number(x, y, R)
                if points == 0:
                    messagebox.showinfo("Результат", f"Точка ({x},{y}) – мимо мишени. Очки: 0")
                else:
                    messagebox.showinfo("Результат", f"Точка ({x},{y}) – попадание в кольцо {points}. Очки: {points}")

            player_score += points
        scores[player] = player_score
        messagebox.showinfo("Итог игрока", f"Игрок {player+1} набрал {player_score} очков.")

    # Определение победителя
    max_score = max(scores)
    winners = [i+1 for i, s in enumerate(scores) if s == max_score]
    if len(winners) == 1:
        messagebox.showinfo("Победитель", f"Победитель – Игрок {winners[0]} с {max_score} очками!")
    else:
        messagebox.showinfo("Победители", f"Ничья! Игроки {', '.join(map(str, winners))} набрали по {max_score} очков.")

    root.destroy()

if __name__ == "__main__":
    main()