import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import calendar

def get_weekday_name(year, month, day):
    """Возвращает название дня недели (на русском) для заданной даты."""
    # datetime.weekday(): понедельник = 0, воскресенье = 6
    weekday_num = datetime(year, month, day).weekday()
    weekdays = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
    return weekdays[weekday_num]

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Даты текущего месяца")
        self.root.geometry("300x400")
        self.root.resizable(False, False)

        # Получаем текущую дату
        now = datetime.now()
        self.year = now.year
        self.month = now.month

        # Заголовок
        month_names = ["январь", "февраль", "март", "апрель", "май", "июнь",
                       "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"]
        title = f"{month_names[self.month-1]} {self.year}"
        ttk.Label(root, text=title, font=("Arial", 14, "bold")).pack(pady=10)

        # Listbox со списком дней
        self.listbox = tk.Listbox(root, height=20, font=("Courier", 12))
        self.listbox.pack(fill="both", expand=True, padx=20, pady=10)

        # Заполняем список днями месяца
        num_days = calendar.monthrange(self.year, self.month)[1]
        for day in range(1, num_days + 1):
            self.listbox.insert(tk.END, str(day))

        # Привязываем событие выбора
        self.listbox.bind("<<ListboxSelect>>", self.on_date_selected)

        # Пояснение
        ttk.Label(root, text="Щёлкните на дате → день недели и текущее время",
                  foreground="gray", wraplength=280).pack(pady=5)

    def on_date_selected(self, event):
        selection = self.listbox.curselection()
        if not selection:
            return
        day_str = self.listbox.get(selection[0])
        if not day_str:
            return
        day = int(day_str)

        # День недели
        weekday = get_weekday_name(self.year, self.month, day)

        # Текущее время (момент выбора)
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")

        messagebox.showinfo("Информация",
                            f"Дата: {day}.{self.month:02d}.{self.year}\n"
                            f"День недели: {weekday}\n"
                            f"Текущее время: {time_str}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()