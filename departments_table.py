import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

# Имя файла для хранения данных
DATA_FILE = "departments.txt"

def load_from_file():
    """Загружает данные из файла. Возвращает список словарей [{"name": ..., "room": ...}]."""
    departments = []
    if not os.path.exists(DATA_FILE):
        # Создаём файл с примером данных
        sample = [
            "Бухгалтерия;101",
            "IT-отдел;202",
            "Отдел кадров;103"
        ]
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(sample))
    # Чтение файла
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(";")
            if len(parts) != 2:
                continue
            name, room_str = parts
            try:
                room = int(room_str)
                departments.append({"name": name, "room": room})
            except ValueError:
                continue
    return departments

def save_to_file(departments):
    """Сохраняет список отделов в файл."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        for dept in departments:
            f.write(f"{dept['name']};{dept['room']}\n")

class DepartmentsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Отделы организации")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        # Загружаем данные
        self.departments = load_from_file()

        # Создаём интерфейс
        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        # Таблица (Treeview)
        self.tree = ttk.Treeview(self.root, columns=("room",), show="tree headings", height=15)
        self.tree.heading("#0", text="Название отдела")
        self.tree.heading("room", text="Кабинет")
        self.tree.column("#0", width=250)
        self.tree.column("room", width=100)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Рамка с кнопками
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(btn_frame, text="Добавить", command=self.add_department).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Удалить", command=self.delete_department).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Сохранить", command=self.save_departments).pack(side="right", padx=5)

        # Строка статуса
        self.status_label = ttk.Label(self.root, text="Готово", relief="sunken", anchor="w")
        self.status_label.pack(fill="x", padx=10, pady=5)

    def refresh_table(self):
        """Обновляет отображение таблицы из self.departments."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        for dept in self.departments:
            self.tree.insert("", tk.END, text=dept["name"], values=(dept["room"],))

    def add_department(self):
        name = simpledialog.askstring("Добавить отдел", "Название отдела:")
        if not name:
            return
        # Проверка на дубликат названия
        if any(d["name"] == name for d in self.departments):
            messagebox.showerror("Ошибка", "Отдел с таким названием уже существует")
            return
        room_str = simpledialog.askstring("Добавить отдел", "Номер кабинета:")
        if not room_str:
            return
        try:
            room = int(room_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Номер кабинета должен быть целым числом")
            return
        self.departments.append({"name": name, "room": room})
        self.refresh_table()
        self.status_label.config(text=f"Добавлен отдел: {name}")

    def delete_department(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите отдел для удаления")
            return
        item = selected[0]
        dept_name = self.tree.item(item, "text")
        # Удаляем из списка
        self.departments = [d for d in self.departments if d["name"] != dept_name]
        self.refresh_table()
        self.status_label.config(text=f"Удалён отдел: {dept_name}")

    def save_departments(self):
        save_to_file(self.departments)
        self.status_label.config(text="Данные сохранены в файл")

if __name__ == "__main__":
    root = tk.Tk()
    app = DepartmentsApp(root)
    root.mainloop()