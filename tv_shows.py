import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

# ------------------ Хранилище передач ------------------
# Каждая передача: {"name": str, "start": str (YYYY-MM-DD HH:MM)}
shows = [
    {"name": "Новости", "start": "2026-05-27 19:00"},
    {"name": "Фильм 'Начало'", "start": "2026-05-28 21:30"},
    {"name": "Спорт: футбол", "start": "2026-05-29 18:15"},
    {"name": "Научно-популярная программа", "start": "2026-05-30 15:00"},
]

def save_shows():
    """(Опционально) Сохраняет список передач в файл."""
    pass  # можно реализовать позже

def load_shows():
    """(Опционально) Загружает список передач из файла."""
    pass

def format_datetime(dt_str):
    """Преобразует строку в объект datetime."""
    return datetime.strptime(dt_str, "%Y-%m-%d %H:%M")

def get_remaining_time(show):
    """Возвращает строку 'X ч Y мин' или 'уже прошла'."""
    start_dt = format_datetime(show["start"])
    now = datetime.now()
    if start_dt <= now:
        return "уже прошла"
    diff = start_dt - now
    total_seconds = int(diff.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{hours} ч {minutes} мин"

# ------------------ GUI ------------------
class TVShowsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Телепередачи")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        self.create_widgets()
        self.refresh_list()

    def create_widgets(self):
        # Заголовок
        ttk.Label(self.root, text="Предстоящие телепередачи", font=("Arial", 14, "bold")).pack(pady=5)

        # Список передач
        self.listbox = tk.Listbox(self.root, height=12, font=("Courier", 10))
        self.listbox.pack(fill="both", expand=True, padx=20, pady=5)
        self.listbox.bind("<<ListboxSelect>>", self.on_show_selected)

        # Кнопки управления
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=20, pady=5)

        ttk.Button(btn_frame, text="Добавить передачу", command=self.add_show).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Удалить выбранную", command=self.delete_show).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Обновить", command=self.refresh_list).pack(side="right", padx=5)

        # Пояснение
        ttk.Label(self.root, text="Щёлкните по передаче → узнайте время до начала",
                  foreground="gray", wraplength=450).pack(pady=5)

    def refresh_list(self):
        """Обновляет содержимое Listbox."""
        self.listbox.delete(0, tk.END)
        for show in shows:
            # Отображаем: "Название (дата время)"
            display = f"{show['name']} – {show['start']}"
            self.listbox.insert(tk.END, display)

    def on_show_selected(self, event):
        selection = self.listbox.curselection()
        if not selection:
            return
        index = selection[0]
        show = shows[index]
        remaining = get_remaining_time(show)
        if remaining == "уже прошла":
            messagebox.showinfo("Время начала",
                                f"Передача '{show['name']}' началась в {show['start']}\n(уже прошла)")
        else:
            messagebox.showinfo("Время до начала",
                                f"Передача '{show['name']}' начнётся через\n{remaining}")

    def add_show(self):
        """Диалог добавления новой передачи."""
        name = simpledialog.askstring("Добавление", "Введите название передачи:")
        if not name:
            return
        start_str = simpledialog.askstring("Добавление",
                                           "Введите дату и время начала (ГГГГ-ММ-ДД ЧЧ:ММ):\n"
                                           "Пример: 2026-06-01 20:30")
        if not start_str:
            return
        # Проверка формата
        try:
            datetime.strptime(start_str, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты/времени. Используйте ГГГГ-ММ-ДД ЧЧ:ММ")
            return
        shows.append({"name": name, "start": start_str})
        self.refresh_list()

    def delete_show(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Внимание", "Выберите передачу для удаления")
            return
        index = selection[0]
        del shows[index]
        self.refresh_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = TVShowsApp(root)
    root.mainloop()