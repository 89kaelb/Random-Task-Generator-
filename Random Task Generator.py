import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

# Предопределённые задачи с типами
PREDEFINED_TASKS = [
    {"name": "Прочитать статью", "type": "учеба"},
    {"name": "Сделать зарядку", "type": "спорт"},
    {"name": "Написать отчет", "type": "работа"},
    {"name": "Посмотреть лекцию", "type": "учеба"},
    {"name": "Пробежать 3 км", "type": "спорт"},
    {"name": "Провести созвон", "type": "работа"},
]

HISTORY_FILE = "tasks.json"

class TaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных задач")
        self.root.geometry("500x400")

        # Загрузка истории
        self.history = self.load_history()

        # --- Виджеты ---
        # Фильтр по типу
        self.filter_var = tk.StringVar(value="все")
        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=5, fill=tk.X)

        tk.Label(filter_frame, text="Фильтр по типу:").pack(side=tk.LEFT)
        ttk.Combobox(filter_frame, textvariable=self.filter_var,
                     values=["все", "учеба", "спорт", "работа"], state="readonly").pack(side=tk.LEFT, padx=5)

        # Кнопка генерации
        tk.Button(root, text="Сгенерировать задачу", command=self.generate_task).pack(pady=10)

        # Текущая задача
        self.current_task_label = tk.Label(root, text="", font=("Arial", 14), wraplength=400)
        self.current_task_label.pack(pady=10)

        # История задач
        tk.Label(root, text="История задач:").pack()
        self.history_listbox = tk.Listbox(root, width=60, height=12)
        self.history_listbox.pack(pady=5)

        # Кнопки управления историей
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Очистить историю", command=self.clear_history).pack(side=tk.LEFT, padx=5)

    def generate_task(self):
        task_type = self.filter_var.get()
        
        if task_type == "все":
            pool = PREDEFINED_TASKS
        else:
            pool = [t for t in PREDEFINED_TASKS if t["type"] == task_type]
        
        if not pool:
            messagebox.showwarning("Нет задач", "В выбранной категории нет задач.")
            return

        task = random.choice(pool)
        
        # Отображение текущей задачи
        self.current_task_label.config(text=f"Задача: {task['name']} (тип: {task['type']})")
        
        # Добавление в историю
        self.history.append(task)
        self.save_history()
        
        # Обновление списка истории
        self.update_history_list()

    def update_history_list(self):
        self.history_listbox.delete(0, tk.END)
        for task in self.history:
            self.history_listbox.insert(tk.END, f"{task['name']} (тип: {task['type']})")

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_history(self):
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def clear_history(self):
        if messagebox.askyesno("Подтвердить", "Очистить всю историю?"):
            self.history = []
            self.save_history()
            self.update_history_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGeneratorApp(root)
    root.mainloop()
