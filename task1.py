import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title('To-Do List')
        self.tasks = []

        # Create task list
        self.task_list = tk.Listbox(self.root, width=50, height=15, font=('Arial', 12))
        self.task_list.pack(pady=10)

        # Create entry fields for new tasks
        self.new_task_entry = tk.Entry(self.root, width=50, font=('Arial', 12))
        self.new_task_entry.pack()

        # Priority
        self.priority_var = tk.StringVar()
        self.priority_var.set('Low')
        priority_label = tk.Label(self.root, text='Priority:', font=('Arial', 12))
        priority_label.pack()
        self.priority_menu = tk.OptionMenu(self.root, self.priority_var, 'Low', 'Medium', 'High')
        self.priority_menu.pack()

        # Due Date
        self.due_date_var = tk.StringVar()
        due_date_label = tk.Label(self.root, text='Due Date (YYYY-MM-DD):', font=('Arial', 12))
        due_date_label.pack()
        self.due_date_entry = tk.Entry(self.root, width=50, font=('Arial', 12), textvariable=self.due_date_var)
        self.due_date_entry.pack()

        # Add buttons
        add_button = tk.Button(self.root, text='Add Task', width=12, command=self.add_task)
        add_button.pack(pady=5)

        remove_button = tk.Button(self.root, text='Remove Task', width=12, command=self.remove_task)
        remove_button.pack()

        save_button = tk.Button(self.root, text='Save Tasks', width=12, command=self.save_tasks)
        save_button.pack()

        load_button = tk.Button(self.root, text='Load Tasks', width=12, command=self.load_tasks)
        load_button.pack()

        # List view
        self.view_var = tk.StringVar()
        self.view_var.set('All')
        view_label = tk.Label(self.root, text='View:', font=('Arial', 12))
        view_label.pack()
        self.view_menu = tk.OptionMenu(self.root, self.view_var, 'All', 'High Priority', 'Overdue')
        self.view_menu.pack()

    def add_task(self):
        task = self.new_task_entry.get()
        priority = self.priority_var.get()
        due_date_str = self.due_date_var.get()

        if task:
            self.tasks.append({'task': task, 'priority': priority, 'due_date': due_date_str})
            self.update_task_list()
            self.save_tasks()  # Save tasks immediately after adding a new task
            self.clear_entry_fields()
        else:
           messagebox.showwarning('Warning', 'Please enter a task!')

    def remove_task(self):
        try:
            index = self.task_list.curselection()[0]
            del self.tasks[index]
            self.update_task_list()
        except IndexError:
            messagebox.showwarning('Warning', 'Please select a task to remove!')

    def save_tasks(self):
        with open('tasks.txt', 'w') as f:
            for task in self.tasks:
                f.write(f"{task['task']},{task['priority']},{task['due_date']}\n")

    def load_tasks(self):
        try:
            with open('tasks.txt', 'r') as f:
                self.tasks = []
                for line in f.readlines():
                    task_data = line.strip().split(',')
                    self.tasks.append({'task': task_data[0], 'priority': task_data[1], 'due_date': task_data[2]})
                self.update_task_list()
        except FileNotFoundError:
            messagebox.showwarning('Warning', 'No saved tasks found!')

    def update_task_list(self):
        self.task_list.delete(0, tk.END)
        view_option = self.view_var.get()
        today = datetime.today().strftime('%Y-%m-%d')

        for task in self.tasks:
            if view_option == 'All' or (view_option == 'High Priority' and task['priority'] == 'High') or \
                (  view_option == 'Overdue' and task['due_date'] < today):
                formatted_task = f"{task['task']} - Priority: {task['priority']} - Due Date: {task['due_date']}"
                self.task_list.insert(tk.END, formatted_task)


    def clear_entry_fields(self):
        self.new_task_entry.delete(0, tk.END)
        self.priority_var.set('Low')
        self.due_date_var.set('')

def main():
    root = tk.Tk()
    todo_app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
