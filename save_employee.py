import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

class EmployeeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Сохранение данных сотрудника в файл")
        self.root.geometry("750x450")
        self.root.resizable(True, True)

        # Исходные данные (для демонстрации)
        self.employees = [
            {"surname": "Иванов", "firstname": "Иван", "position": "Бухгалтер", "room": 101},
            {"surname": "Петрова", "firstname": "Мария", "position": "Программист", "room": 202},
            {"surname": "Сидоров", "firstname": "Алексей", "position": "Специалист по кадрам", "room": 103},
            {"surname": "Козлова", "firstname": "Елена", "position": "Старший бухгалтер", "room": 101},
            {"surname": "Новиков", "firstname": "Дмитрий", "position": "Системный администратор", "room": 202},
        ]

        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        # Панель с кнопками
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(control_frame, text="Добавить сотрудника", command=self.add_employee).pack(side="left", padx=2)
        ttk.Button(control_frame, text="Удалить сотрудника", command=self.delete_employee).pack(side="left", padx=2)
        ttk.Button(control_frame, text="Сохранить выбранного сотрудника", command=self.save_selected_employee).pack(side="left", padx=10)

        # Таблица сотрудников
        table_frame = ttk.LabelFrame(self.root, text="Список сотрудников", padding=5)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Treeview с 4 столбцами
        self.tree = ttk.Treeview(table_frame, columns=("surname", "firstname", "position", "room"), show="headings")
        self.tree.heading("surname", text="Фамилия")
        self.tree.heading("firstname", text="Имя")
        self.tree.heading("position", text="Должность")
        self.tree.heading("room", text="Кабинет")
        self.tree.column("surname", width=120)
        self.tree.column("firstname", width=100)
        self.tree.column("position", width=150)
        self.tree.column("room", width=80)
        self.tree.pack(fill="both", expand=True)

        # Скроллбар
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Строка статуса
        self.status_label = ttk.Label(self.root, text="Выберите сотрудника и нажмите «Сохранить»", relief="sunken", anchor="w")
        self.status_label.pack(fill="x", padx=10, pady=5)

    def refresh_table(self):
        """Обновляет отображение таблицы на основе self.employees."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        for emp in self.employees:
            self.tree.insert("", tk.END, values=(emp["surname"], emp["firstname"], emp["position"], emp["room"]))

    def add_employee(self):
        """Диалог добавления нового сотрудника."""
        surname = simpledialog.askstring("Добавить сотрудника", "Фамилия:")
        if not surname:
            return
        firstname = simpledialog.askstring("Добавить сотрудника", "Имя:")
        if not firstname:
            return
        position = simpledialog.askstring("Добавить сотрудника", "Должность:")
        if not position:
            return
        room_str = simpledialog.askstring("Добавить сотрудника", "Номер кабинета:")
        if not room_str:
            return
        try:
            room = int(room_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Номер кабинета должен быть целым числом")
            return
        self.employees.append({"surname": surname, "firstname": firstname, "position": position, "room": room})
        self.refresh_table()
        self.status_label.config(text=f"Добавлен сотрудник: {surname} {firstname}")

    def delete_employee(self):
        """Удаление выбранного сотрудника."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите сотрудника для удаления")
            return
        item = selected[0]
        values = self.tree.item(item, "values")
        surname, firstname, position, room = values
        room = int(room)
        self.employees = [e for e in self.employees if not (e["surname"] == surname and e["firstname"] == firstname and e["position"] == position and e["room"] == room)]
        self.refresh_table()
        self.status_label.config(text=f"Удалён сотрудник: {surname} {firstname}")

    def save_selected_employee(self):
        """Сохраняет данные выбранного сотрудника в текстовый файл."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Сначала выберите сотрудника в таблице")
            return
        item = selected[0]
        values = self.tree.item(item, "values")
        # values: (surname, firstname, position, room)
        surname, firstname, position, room = values
        room = int(room)
        # Формат записи: фамилия;имя;должность;кабинет
        line = f"{surname};{firstname};{position};{room}\n"
        filename = "selected_employee.txt"
        try:
            # Режим 'a' - добавление в конец (или 'w' - перезапись). Выберем добавление.
            with open(filename, "a", encoding="utf-8") as f:
                f.write(line)
            messagebox.showinfo("Сохранено", f"Сотрудник {surname} {firstname} сохранён в файл {filename}")
            self.status_label.config(text=f"Сохранён сотрудник: {surname} {firstname}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить в файл: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeApp(root)
    root.mainloop()