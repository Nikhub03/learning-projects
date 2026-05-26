import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# ------------------ Исходные данные ------------------
departments = [
    {"name": "Бухгалтерия", "room": 101},
    {"name": "IT-отдел", "room": 202},
    {"name": "Отдел кадров", "room": 103},
]

employees = [
    {"surname": "Иванов", "firstname": "Иван", "position": "Бухгалтер", "room": 101},
    {"surname": "Петрова", "firstname": "Мария", "position": "Программист", "room": 202},
    {"surname": "Сидоров", "firstname": "Алексей", "position": "Специалист по кадрам", "room": 103},
    {"surname": "Козлова", "firstname": "Елена", "position": "Старший бухгалтер", "room": 101},
    {"surname": "Новиков", "firstname": "Дмитрий", "position": "Системный администратор", "room": 202},
]

# ------------------ GUI приложения ------------------
class OrgApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Отделы и сотрудники")
        self.root.geometry("800x500")
        self.root.resizable(True, True)

        self.current_department = None   # выбранный отдел

        self.create_widgets()
        self.refresh_departments()
        self.refresh_employees()

    def create_widgets(self):
        # Панель с кнопками управления (опционально)
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(control_frame, text="Добавить отдел", command=self.add_department).pack(side="left", padx=2)
        ttk.Button(control_frame, text="Удалить отдел", command=self.delete_department).pack(side="left", padx=2)
        ttk.Button(control_frame, text="Добавить сотрудника", command=self.add_employee).pack(side="left", padx=2)
        ttk.Button(control_frame, text="Удалить сотрудника", command=self.delete_employee).pack(side="left", padx=2)

        # Таблица отделов
        dept_frame = ttk.LabelFrame(self.root, text="Отделы", padding=5)
        dept_frame.pack(fill="x", padx=10, pady=5)

        self.dept_tree = ttk.Treeview(dept_frame, columns=("room",), show="tree headings", height=5)
        self.dept_tree.heading("#0", text="Название отдела")
        self.dept_tree.heading("room", text="Кабинет")
        self.dept_tree.column("#0", width=200)
        self.dept_tree.column("room", width=100)
        self.dept_tree.pack(fill="x")

        # Привязываем событие выбора отдела
        self.dept_tree.bind("<<TreeviewSelect>>", self.on_department_selected)

        # Таблица сотрудников
        emp_frame = ttk.LabelFrame(self.root, text="Сотрудники (фильтр по кабинету выбранного отдела)", padding=5)
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

        # Скроллбар для сотрудников (опционально)
        scrollbar = ttk.Scrollbar(emp_frame, orient="vertical", command=self.emp_tree.yview)
        self.emp_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def refresh_departments(self):
        """Обновляет таблицу отделов."""
        for row in self.dept_tree.get_children():
            self.dept_tree.delete(row)
        for dept in departments:
            self.dept_tree.insert("", tk.END, text=dept["name"], values=(dept["room"],))

    def refresh_employees(self, filter_room=None):
        """Обновляет таблицу сотрудников. Если filter_room задан, показывает только сотрудников с этим кабинетом."""
        for row in self.emp_tree.get_children():
            self.emp_tree.delete(row)
        for emp in employees:
            if filter_room is not None and emp["room"] != filter_room:
                continue
            self.emp_tree.insert("", tk.END, values=(emp["surname"], emp["firstname"], emp["position"], emp["room"]))

    def on_department_selected(self, event):
        """Обработчик выбора отдела: фильтруем сотрудников по кабинету."""
        selected = self.dept_tree.selection()
        if not selected:
            return
        item = selected[0]
        dept_name = self.dept_tree.item(item, "text")
        # Находим кабинет выбранного отдела
        for dept in departments:
            if dept["name"] == dept_name:
                self.current_department = dept
                self.refresh_employees(filter_room=dept["room"])
                break

    # ------------------ Дополнительные методы для управления данными ------------------
    def add_department(self):
        name = simpledialog.askstring("Добавить отдел", "Введите название отдела:")
        if not name:
            return
        # Проверка на уникальность имени
        if any(d["name"] == name for d in departments):
            messagebox.showerror("Ошибка", "Отдел с таким названием уже существует")
            return
        room_str = simpledialog.askstring("Добавить отдел", "Введите номер кабинета:")
        if not room_str:
            return
        try:
            room = int(room_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Номер кабинета должен быть целым числом")
            return
        departments.append({"name": name, "room": room})
        self.refresh_departments()

    def delete_department(self):
        selected = self.dept_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите отдел для удаления")
            return
        item = selected[0]
        dept_name = self.dept_tree.item(item, "text")
        # Удаляем отдел
        for i, dept in enumerate(departments):
            if dept["name"] == dept_name:
                del departments[i]
                break
        # Очищаем фильтр сотрудников, если удалённый отдел был выбран
        if self.current_department and self.current_department["name"] == dept_name:
            self.current_department = None
            self.refresh_employees()
        else:
            self.refresh_employees(filter_room=self.current_department["room"] if self.current_department else None)
        self.refresh_departments()

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
        employees.append({"surname": surname, "firstname": firstname, "position": position, "room": room})
        # Обновляем таблицу с учётом текущего фильтра
        filter_room = self.current_department["room"] if self.current_department else None
        self.refresh_employees(filter_room)

    def delete_employee(self):
        selected = self.emp_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите сотрудника для удаления")
            return
        item = selected[0]
        values = self.emp_tree.item(item, "values")
        # Ищем сотрудника по фамилии, имени, должности и кабинету (не идеально, но для демонстрации)
        surname, firstname, position, room = values
        room = int(room)
        for i, emp in enumerate(employees):
            if emp["surname"] == surname and emp["firstname"] == firstname and emp["position"] == position and emp["room"] == room:
                del employees[i]
                break
        filter_room = self.current_department["room"] if self.current_department else None
        self.refresh_employees(filter_room)

if __name__ == "__main__":
    root = tk.Tk()
    app = OrgApp(root)
    root.mainloop()