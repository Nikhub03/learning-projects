import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class OrgApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Фильтр сотрудников по отделу (ComboBox)")
        self.root.geometry("800x500")
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

        self.current_room = None  # кабинет выбранного отдела

        self.create_widgets()
        self.refresh_department_combobox()
        self.show_all_employees()  # по умолчанию показываем всех

    def create_widgets(self):
        # Панель выбора отдела
        filter_frame = ttk.LabelFrame(self.root, text="Выберите отдел", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(filter_frame, text="Отдел:").pack(side="left", padx=5)
        self.dept_combo = ttk.Combobox(filter_frame, state="readonly", width=30)
        self.dept_combo.pack(side="left", padx=5)
        self.dept_combo.bind("<<ComboboxSelected>>", self.on_department_selected)

        # Кнопка "Показать всех" (дополнительно)
        ttk.Button(filter_frame, text="Показать всех сотрудников", command=self.show_all_employees).pack(side="left", padx=10)

        # Панель управления (добавление/удаление данных)
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(control_frame, text="Добавить отдел", command=self.add_department).pack(side="left", padx=2)
        ttk.Button(control_frame, text="Удалить отдел", command=self.delete_department).pack(side="left", padx=2)
        ttk.Button(control_frame, text="Добавить сотрудника", command=self.add_employee).pack(side="left", padx=2)
        ttk.Button(control_frame, text="Удалить сотрудника", command=self.delete_employee).pack(side="left", padx=2)

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

        # Строка статуса
        self.status_label = ttk.Label(self.root, text="Выберите отдел из списка", relief="sunken", anchor="w")
        self.status_label.pack(fill="x", padx=10, pady=5)

    def refresh_department_combobox(self):
        """Обновляет список отделов в выпадающем списке."""
        names = [dept["name"] for dept in self.departments]
        self.dept_combo['values'] = names
        if names:
            self.dept_combo.set(names[0])
            self.current_room = self.departments[0]["room"]
        else:
            self.dept_combo.set('')
            self.current_room = None

    def on_department_selected(self, event=None):
        """Обработчик выбора отдела: фильтрует сотрудников по кабинету."""
        selected_name = self.dept_combo.get()
        if not selected_name:
            return
        # Находим отдел по названию
        for dept in self.departments:
            if dept["name"] == selected_name:
                self.current_room = dept["room"]
                break
        else:
            self.current_room = None
        self.filter_employees_by_room()

    def filter_employees_by_room(self):
        """Показывает сотрудников, чей кабинет равен self.current_room."""
        for row in self.emp_tree.get_children():
            self.emp_tree.delete(row)
        if self.current_room is None:
            self.status_label.config(text="Отдел не выбран")
            return
        filtered = [emp for emp in self.employees if emp["room"] == self.current_room]
        if not filtered:
            self.status_label.config(text=f"В выбранном отделе (каб.{self.current_room}) нет сотрудников")
        else:
            for emp in filtered:
                self.emp_tree.insert("", tk.END, values=(emp["surname"], emp["firstname"], emp["position"], emp["room"]))
            self.status_label.config(text=f"Показано {len(filtered)} сотрудников (каб.{self.current_room})")

    def show_all_employees(self):
        """Отображает всех сотрудников (сброс фильтра)."""
        for row in self.emp_tree.get_children():
            self.emp_tree.delete(row)
        for emp in self.employees:
            self.emp_tree.insert("", tk.END, values=(emp["surname"], emp["firstname"], emp["position"], emp["room"]))
        self.status_label.config(text="Показаны все сотрудники")
        # Также можно сбросить выбор в комбобоксе (необязательно)
        # self.dept_combo.set('')

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
        self.refresh_department_combobox()
        self.status_label.config(text=f"Добавлен отдел: {name}")

    def delete_department(self):
        if not self.dept_combo.get():
            messagebox.showwarning("Внимание", "Нет отделов для удаления")
            return
        selected_name = self.dept_combo.get()
        self.departments = [d for d in self.departments if d["name"] != selected_name]
        self.refresh_department_combobox()
        # Если удалённый отдел был выбран – показываем всех сотрудников
        self.show_all_employees()
        self.status_label.config(text=f"Удалён отдел: {selected_name}")

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
        # Обновляем отображение в зависимости от текущего режима
        if self.dept_combo.get() and self.current_room is not None:
            self.filter_employees_by_room()
        else:
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
        # Обновляем отображение
        if self.dept_combo.get() and self.current_room is not None:
            self.filter_employees_by_room()
        else:
            self.show_all_employees()
        self.status_label.config(text=f"Удалён сотрудник: {surname} {firstname}")

if __name__ == "__main__":
    root = tk.Tk()
    app = OrgApp(root)
    root.mainloop()