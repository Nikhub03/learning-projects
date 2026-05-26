import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from datetime import datetime

class CafeMenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Меню кафе")
        self.root.geometry("700x550")
        self.root.resizable(True, True)

        # Список блюд: каждый элемент - строка (название)
        self.dishes = [
            "Борщ",
            "Салат Цезарь",
            "Стейк из говядины",
            "Картофель фри",
            "Чизкейк",
            "Эспрессо",
            "Чай с лимоном"
        ]
        # Словарь для хранения переменных флажков
        self.check_vars = {}

        self.create_widgets()
        self.update_checkboxes()

    def create_widgets(self):
        # Верхняя панель с кнопками управления блюдами
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(control_frame, text="Добавить блюдо", command=self.add_dish).pack(side="left", padx=2)
        ttk.Button(control_frame, text="Удалить выбранное блюдо", command=self.delete_dish).pack(side="left", padx=2)

        # Рамка с флажками (с прокруткой)
        checkbox_frame = ttk.LabelFrame(self.root, text="Блюда (отметьте нужные)", padding=5)
        checkbox_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.canvas = tk.Canvas(checkbox_frame)
        scrollbar = ttk.Scrollbar(checkbox_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Кнопки действий
        action_frame = ttk.Frame(self.root)
        action_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(action_frame, text="Составить меню", command=self.compose_menu).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Сохранить меню в RTF", command=self.save_menu).pack(side="left", padx=5)

        # Область отображения RTF-документа (будем показывать текст)
        rtf_frame = ttk.LabelFrame(self.root, text="Сгенерированное меню (RTF)", padding=5)
        rtf_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.text_area = tk.Text(rtf_frame, wrap="word", font=("Arial", 10))
        self.text_area.pack(fill="both", expand=True)

        self.status_label = ttk.Label(self.root, text="Отметьте блюда, затем 'Составить меню'", relief="sunken", anchor="w")
        self.status_label.pack(fill="x", padx=10, pady=5)

    def update_checkboxes(self):
        """Обновляет список флажков в соответствии с self.dishes."""
        # Удаляем старые виджеты
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.check_vars.clear()

        # Создаём новые флажки
        for dish in self.dishes:
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(self.scrollable_frame, text=dish, variable=var)
            cb.pack(anchor="w", padx=5, pady=2)
            self.check_vars[dish] = var

    def add_dish(self):
        dish = simpledialog.askstring("Добавить блюдо", "Введите название блюда:")
        if dish and dish.strip():
            dish = dish.strip()
            if dish in self.dishes:
                messagebox.showwarning("Внимание", "Такое блюдо уже есть в списке")
                return
            self.dishes.append(dish)
            self.update_checkboxes()
            self.status_label.config(text=f"Добавлено блюдо: {dish}")

    def delete_dish(self):
        # Диалог выбора блюда для удаления
        if not self.dishes:
            messagebox.showinfo("Информация", "Список блюд пуст")
            return
        dish_to_delete = simpledialog.askstring("Удалить блюдо", "Введите точное название блюда для удаления:")
        if dish_to_delete and dish_to_delete in self.dishes:
            self.dishes.remove(dish_to_delete)
            self.update_checkboxes()
            self.status_label.config(text=f"Удалено блюдо: {dish_to_delete}")
        elif dish_to_delete:
            messagebox.showerror("Ошибка", f"Блюдо '{dish_to_delete}' не найдено")

    def get_selected_dishes(self):
        """Возвращает список выбранных блюд."""
        return [dish for dish, var in self.check_vars.items() if var.get()]

    def compose_menu(self):
        """Формирует и отображает RTF-меню на основе выбранных блюд."""
        selected = self.get_selected_dishes()
        if not selected:
            messagebox.showwarning("Внимание", "Не выбрано ни одного блюда")
            self.text_area.delete("1.0", tk.END)
            return

        # Формируем RTF-строку
        now = datetime.now().strftime("%d.%m.%Y %H:%M")
        rtf_lines = []
        rtf_lines.append(r"{\rtf1\ansi\deff0")
        rtf_lines.append(r"{\fonttbl{\f0 Arial;}}")
        rtf_lines.append(r"\f0\fs24")
        rtf_lines.append(r"\b Меню кафе\b0\par")
        rtf_lines.append(f"Сформировано: {now}\\par")
        rtf_lines.append(r"\par")
        for i, dish in enumerate(selected, 1):
            rtf_lines.append(f"{i}. {dish}\\par")
        rtf_lines.append(r"\par\i Приятного аппетита!\i0\par")
        rtf_lines.append("}")

        rtf_content = "\n".join(rtf_lines)

        # Отображаем в текстовом поле (как простой текст, но с элементами разметки)
        # Для наглядности покажем читаемый текст, а RTF-код можно посмотреть при сохранении.
        display_text = f"Меню кафе\nСформировано: {now}\n\n"
        for i, dish in enumerate(selected, 1):
            display_text += f"{i}. {dish}\n"
        display_text += "\nПриятного аппетита!"
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", display_text)
        self.status_label.config(text=f"Меню составлено, выбрано {len(selected)} блюд")

        # Сохраняем RTF в атрибуте для последующего сохранения
        self.current_rtf = rtf_content

    def save_menu(self):
        """Сохраняет текущее RTF-меню в файл."""
        if not hasattr(self, 'current_rtf') or not self.current_rtf:
            messagebox.showwarning("Внимание", "Сначала составьте меню (кнопка 'Составить меню')")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".rtf",
            filetypes=[("RTF documents", "*.rtf"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(self.current_rtf)
                messagebox.showinfo("Сохранено", f"Меню сохранено в файл:\n{file_path}")
                self.status_label.config(text=f"Меню сохранено: {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CafeMenuApp(root)
    root.mainloop()