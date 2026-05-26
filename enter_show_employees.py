import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class OrgApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Отделы и сотрудники (отображение по Enter)")
        self.root.geometry("800x550")
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

        self.current_department = None   # выбранный отдел

        self.create_widgets()
        self.refresh_departments()
        self.refresh_employees()

        # Привязываем клавишу Enter во всём окне
        self.root.bind("<Return>", self.on_enter_pressed)

    def create_widgets(self):
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(control_frame, text="Добавить отдел", command=self.add_department).pack(side="left", padx=2)
        ttk.Button(control_frame, text="Удалить отдел", command=self.delete_department).pack(side="left", padx=2)
        ttk.Button(control_frame, text="Добавить сотрудника", command=self.add_employee).pack(side="left", padx=2)
        ttk.Button(control_frame, text="Удалить сотрудника", command=self.delete_employee).pack(side="left", padx=2)

        # Подсказка
        hint_label = ttk.Label(control_frame, text="Выберите отдел и нажмите Enter", foreground="blue")
        hint_label.pack(side="right", padx=10)

        # Таблица отделов
        dept_frame = ttk.LabelFrame(self.root, text="Отделы", padding=5)
        dept_frame.pack(fill="x", padx=10, pady=5)

        self.dept_tree = ttk.Treeview(dept_frame, columns=("room",), show="tree headings", height=5)
        self.dept_tree.heading("#0", text="Название отдела")
        self.dept_tree.heading("room", text="Кабинет")
        self.dept_tree.column("#0", width=200)
        self.dept_tree.column("room", width=100)
        self.dept_tree.pack(fill="x")
        self.dept_tree.bind("<<TreeviewSelect>>", self.on_department_selected)

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

        self.status_label = ttk.Label(self.root, text="Готово. Выберите отдел и нажмите Enter.", relief="sunken", anchor="w")
        self.status_label.pack(fill="x", padx=10, pady=5)

    def refresh_departments(self):
        for row in self.dept_tree.get_children():
            self.dept_tree.delete(row)
        for dept in self.departments:
            self.dept_tree.insert("", tk.END, text=dept["name"], values=(dept["room"],))

    def refresh_employees(self):
        for row in self.emp_tree.get_children():
            self.emp_tree.delete(row)
        for emp in self.employees:
            self.emp_tree.insert("", tk.END, values=(emp["surname"], emp["firstname"], emp["position"], emp["room"]))

    def on_department_selected(self, event):
        selected = self.dept_tree.selection()
        if not selected:
            self.current_department = None
            self.status_label.config(text="Отдел не выбран")
            return
        item = selected[0]
        dept_name = self.dept_tree.item(item, "text")
        for dept in self.departments:
            if dept["name"] == dept_name:
                self.current_department = dept
                self.status_label.config(text=f"Выбран отдел: {dept_name} (каб. {dept['room']})")
                break

    def on_enter_pressed(self, event):
        """Обработчик нажатия Enter: показывает сотрудников выбранного отдела."""
        if not self.current_department:
            messagebox.showwarning("Внимание", "Сначала выберите отдел в таблице отделов")
            return
        room = self.current_department["room"]
        # Находим всех сотрудников с таким кабинетом
        employees_in_room = [emp for emp in self.employees if emp["room"] == room]
        if not employees_in_room:
            messagebox.showinfo("Информация", f"В отделе '{self.current_department['name']}' (кабинет {room}) нет сотрудников")
            return
        # Формируем строку с ФИО
        names = "\n".join([f"{emp['surname']} {emp['firstname']}" for emp in employees_in_room])
        messagebox.showinfo(f"Сотрудники отдела '{self.current_department['name']}'", names)

    # ------------------ Дополнительные методы для управления ------------------
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
        if self.current_department and self.current_department["name"] == dept_name:
            self.current_department = None
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
        self.refresh_employees()
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
        self.refresh_employees()
        self.status_label.config(text=f"Удалён сотрудник: {surname} {firstname}")

if __name__ == "__main__":
    root = tk.Tk()
    app = OrgApp(root)
    root.mainloop()