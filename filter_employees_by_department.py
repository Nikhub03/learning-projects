import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class OrgApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Фильтр сотрудников по отделу")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Данные
        self.departments = [
            {"name": "Бухгалтерия", "room": 101},
            {"name": "IT-отдел", "room": 202},
            {"name": "Отдел кадров", "room": 103},
        ]
        self.employees = [
            {"surname": "Иванов", "firstname": "Иван", "position": "Бухгалтер", "room": 101},
            {"surname": "Петрова", "firstname": "Мария", "position": "Программист", "room": 202},
            {"surname": "Сидоров", "firstname": "Алексей", "position": "Специалист по кадрам", "room": 103},
            {"surname": "Козлова", "firstname": "Елена", "position": "Старший бухгалтер", "room": 101},
            {"surname": "Новиков", "firstname": "Дмитрий", "position": "Системный администратор", "room": 202},
        ]

        self.create_widgets()
        self.refresh_departments()   # для отображения в отдельном списке (опционально)
        self.show_all_employees()

    def create_widgets(self):
        # Панель фильтрации
        filter_frame = ttk.LabelFrame(self.root, text="Параметры отдела", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(filter_frame, text="Название отдела:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.dept_name_entry = ttk.Entry(filter_frame, width=20)
        self.dept_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(filter_frame, text="Номер кабинета:").grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.room_entry = ttk.Entry(filter_frame, width=10)
        self.room_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(filter_frame, text="Показать сотрудников", command=self.filter_employees).grid(row=0, column=4, padx=10, pady=5)
        ttk.Button(filter_frame, text="Сбросить фильтр", command=self.show_all_employees).grid(row=0, column=5, padx=5, pady=5)

        # Панель управления (добавление/удаление данных)
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(control_frame, text="Добавить отдел", command=self.add_department).pack(side="left", padx=2)
        ttk.Button(control_frame, text="Удалить отдел", command=self.delete_department).pack(side="left", padx=2)
        ttk.Button(control_frame, text="Добавить сотрудника", command=self.add_employee).pack(side="left", padx=2)
        ttk.Button(control_frame, text="Удалить сотрудника", command=self.delete_employee).pack(side="left", padx=2)

        # Таблица отделов (для наглядности)
        dept_frame = ttk.LabelFrame(self.root, text="Существующие отделы", padding=5)
        dept_frame.pack(fill="x", padx=10, pady=5)

        self.dept_tree = ttk.Treeview(dept_frame, columns=("room",), show="tree headings", height=4)
        self.dept_tree.heading("#0", text="Название отдела")
        self.dept_tree.heading("room", text="Кабинет")
        self.dept_tree.column("#0", width=200)
        self.dept_tree.column("room", width=100)
        self.dept_tree.pack(fill="x")

        # Таблица сотрудников
        emp_frame = ttk.LabelFrame(self.root, text="Сотрудники", padding=5)
        emp_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.emp_tree = ttk.Treeview(emp_frame, columns=("surname", "firstname", "position", "room"), show="headings")
        self.emp_tree.heading("surname", text="Фамилия")
        self.emp_tree.heading("firstname", text="Имя")
        self.emp_tree.heading("position", text="Должность")
        self.emp_tree.heading("room", text="Кабинет")
        self.emp_tree.column("surname", width=120)
        self.emp_tree.column("firstname", width=100)
        self.emp_tree.column("position", width=150)
        self.emp_tree.column("room", width=80)
        self.emp_tree.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(emp_frame, orient="vertical", command=self.emp_tree.yview)
        self.emp_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.status_label = ttk.Label(self.root, text="Введите название отдела и номер кабинета, нажмите 'Показать'", relief="sunken", anchor="w")
        self.status_label.pack(fill="x", padx=10, pady=5)

    def refresh_departments(self):
        for row in self.dept_tree.get_children():
            self.dept_tree.delete(row)
        for dept in self.departments:
            self.dept_tree.insert("", tk.END, text=dept["name"], values=(dept["room"],))

    def show_all_employees(self):
        """Показывает всех сотрудников (без фильтрации)."""
        for row in self.emp_tree.get_children():
            self.emp_tree.delete(row)
        for emp in self.employees:
            self.emp_tree.insert("", tk.END, values=(emp["surname"], emp["firstname"], emp["position"], emp["room"]))
        self.status_label.config(text="Показаны все сотрудники")

    def filter_employees(self):
        """Фильтрует сотрудников по введённому названию отдела и номеру кабинета."""
        dept_name = self.dept_name_entry.get().strip()
        room_str = self.room_entry.get().strip()
        if not dept_name or not room_str:
            messagebox.showwarning("Внимание", "Введите и название отдела, и номер кабинета")
            return
        try:
            room = int(room_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Номер кабинета должен быть целым числом")
            return
        # Проверяем, существует ли отдел с таким названием и кабинетом
        department = None
        for dept in self.departments:
            if dept["name"] == dept_name and dept["room"] == room:
                department = dept
                break
        if not department:
            messagebox.showerror("Ошибка", f"Отдел '{dept_name}' с кабинетом {room} не найден")
            # Очищаем таблицу сотрудников
            for row in self.emp_tree.get_children():
                self.emp_tree.delete(row)
            self.status_label.config(text=f"Отдел '{dept_name}' (каб.{room}) не найден")
            return
        # Показываем сотрудников с этим кабинетом
        filtered = [emp for emp in self.employees if emp["room"] == room]
        for row in self.emp_tree.get_children():
            self.emp_tree.delete(row)
        if not filtered:
            self.status_label.config(text=f"В отделе '{dept_name}' (каб.{room}) нет сотрудников")
        else:
            for emp in filtered:
                self.emp_tree.insert("", tk.END, values=(emp["surname"], emp["firstname"], emp["position"], emp["room"]))
            self.status_label.config(text=f"Показано {len(filtered)} сотрудников отдела '{dept_name}'")

    # ------------------ Управление данными (для удобства) ------------------
    def add_department(self):
        name = simpledialog.askstring("Добавить отдел", "Название отдела:")
        if not name:
            return
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
        self.refresh_departments()
        self.status_label.config(text=f"Добавлен отдел: {name}")

    def delete_department(self):
        selected = self.dept_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите отдел для удаления")
            return
        item = selected[0]
        dept_name = self.dept_tree.item(item, "text")
        self.departments = [d for d in self.departments if d["name"] != dept_name]
        self.refresh_departments()
        self.status_label.config(text=f"Удалён отдел: {dept_name}")

    def add_employee(self):
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
        self.show_all_employees()
        self.status_label.config(text=f"Добавлен сотрудник: {surname} {firstname}")

    def delete_employee(self):
        selected = self.emp_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите сотрудника для удаления")
            return
        item = selected[0]
        values = self.emp_tree.item(item, "values")
        surname, firstname, position, room = values
        room = int(room)
        self.employees = [e for e in self.employees if not (e["surname"] == surname and e["firstname"] == firstname and e["position"] == position and e["room"] == room)]
        self.show_all_employees()
        self.status_label.config(text=f"Удалён сотрудник: {surname} {firstname}")

if __name__ == "__main__":
    root = tk.Tk()
    app = OrgApp(root)
    root.mainloop()