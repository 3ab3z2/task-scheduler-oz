import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from functional import add_task, update_task, delete_task, filter_tasks, sort_tasks, notify, save_tasks, load_tasks

# Global task list
tasks = []

def refresh_task_list(tree):
    for row in tree.get_children():
        tree.delete(row)
    for task in tasks:
        tree.insert("", "end", values=(
            task["task_id"],
            task["description"],
            task["due_date"].strftime("%Y-%m-%d"),
            task["priority"],
            task["status"]
        ))

def add_task_gui():
    def save():
        global tasks
        description = desc_entry.get()
        due_date = date_entry.get()
        priority = priority_combo.get()
        tasks = add_task(tasks, description, due_date, priority)
        refresh_task_list(tree)
        add_window.destroy()

    add_window = tk.Toplevel(root)
    add_window.title("Add Task")
    add_window.configure(bg="#ecc19c")

    tk.Label(add_window, text="Description:", bg="#ecc19c", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5)
    desc_entry = tk.Entry(add_window, width=30)
    desc_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(add_window, text="Due Date (YYYY-MM-DD):", bg="#ecc19c", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5)
    date_entry = tk.Entry(add_window, width=30)
    date_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(add_window, text="Priority:", bg="#ecc19c", font=("Arial", 10)).grid(row=2, column=0, padx=5, pady=5)
    priority_combo = ttk.Combobox(add_window, values=["Low", "Medium", "High"], width=27)
    priority_combo.grid(row=2, column=1, padx=5, pady=5)

    tk.Button(add_window, text="Save", command=save, bg="#1e847f", fg="white", font=("Arial", 10, "bold")).grid(row=3, columnspan=2, pady=10)

def update_task_gui():
    def save():
        global tasks
        task_id = int(task_id_entry.get())
        description = desc_entry.get() or None
        due_date = date_entry.get() or None
        priority = priority_combo.get() or None
        status = status_combo.get() or None
        tasks = update_task(tasks, task_id, description, due_date, priority, status)
        refresh_task_list(tree)
        update_window.destroy()

    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Update Task", "No task selected!")
        return
    task_id = tree.item(selected)["values"][0]

    update_window = tk.Toplevel(root)
    update_window.title("Update Task")
    update_window.configure(bg="#ecc19c")

    tk.Label(update_window, text="Task ID:", bg="#ecc19c", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5)
    task_id_entry = tk.Entry(update_window, width=30)
    task_id_entry.insert(0, task_id)
    task_id_entry.config(state="readonly")
    task_id_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(update_window, text="Description:", bg="#ecc19c", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5)
    desc_entry = tk.Entry(update_window, width=30)
    desc_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(update_window, text="Due Date (YYYY-MM-DD):", bg="#ecc19c", font=("Arial", 10)).grid(row=2, column=0, padx=5, pady=5)
    date_entry = tk.Entry(update_window, width=30)
    date_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(update_window, text="Priority:", bg="#ecc19c", font=("Arial", 10)).grid(row=3, column=0, padx=5, pady=5)
    priority_combo = ttk.Combobox(update_window, values=["Low", "Medium", "High"], width=27)
    priority_combo.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(update_window, text="Status:", bg="#ecc19c", font=("Arial", 10)).grid(row=4, column=0, padx=5, pady=5)
    status_combo = ttk.Combobox(update_window, values=["Pending", "Completed"], width=27)
    status_combo.grid(row=4, column=1, padx=5, pady=5)

    tk.Button(update_window, text="Save", command=save, bg="#1e847f", fg="white", font=("Arial", 10, "bold")).grid(row=5, columnspan=2, pady=10)

def delete_task_gui():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Delete Task", "No task selected!")
        return
    task_id = tree.item(selected)["values"][0]
    global tasks
    tasks = delete_task(tasks, task_id)
    refresh_task_list(tree)


def filter_tasks_gui():
    def apply_filter():
        global tasks
        key = filter_key_combo.get()
        value = filter_value_entry.get()
        filtered = filter_tasks(tasks, **{key: value})

        display_filtered_tasks(filtered)

        filter_window.destroy()

    def display_filtered_tasks(filtered_tasks):
        if filtered_tasks:
            result_window = tk.Toplevel(root)
            result_window.title("Filtered Tasks")
            result_window.configure(bg="#ecc19c")

            columns = ("task_id", "description", "due_date", "priority", "status")
            tree = ttk.Treeview(result_window, columns=columns, show="headings")
            tree.heading("task_id", text="Task ID")
            tree.heading("description", text="Description")
            tree.heading("due_date", text="Due Date")
            tree.heading("priority", text="Priority")
            tree.heading("status", text="Status")
            tree.grid(row=0, column=0, padx=5, pady=5)

            for task in filtered_tasks:
                tree.insert("", "end", values=(
                    task["task_id"],
                    task["description"],
                    task["due_date"].strftime("%Y-%m-%d"),
                    task["priority"],
                    task["status"]
                ))
        else:
            messagebox.showinfo("No Tasks", "No tasks match your filter criteria!")

    filter_window = tk.Toplevel(root)
    filter_window.title("Filter Tasks")
    filter_window.configure(bg="#ecc19c")

    tk.Label(filter_window, text="Filter Key:", bg="#ecc19c", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5)
    filter_key_combo = ttk.Combobox(filter_window, values=["description", "due_date", "priority", "status"], width=27)
    filter_key_combo.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(filter_window, text="Filter Value:", bg="#ecc19c", font=("Arial", 10)).grid(row=1, column=0, padx=5,pady=5)
    filter_value_entry = tk.Entry(filter_window, width=30)
    filter_value_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Button(filter_window, text="Apply", command=apply_filter, bg="#1e847f", fg="white",
              font=("Arial", 10, "bold")).grid(row=2, columnspan=2, pady=10)


def sort_tasks_gui():
    def apply_sort():
        global tasks
        key = sort_key_combo.get()
        tasks = sort_tasks(tasks, key)
        refresh_task_list(tree)
        sort_window.destroy()

    sort_window = tk.Toplevel(root)
    sort_window.title("Sort Tasks")
    sort_window.configure(bg="#ecc19c")

    tk.Label(sort_window, text="Sort Key:", bg="#ecc19c", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5)
    sort_key_combo = ttk.Combobox(sort_window, values=["task_id", "description", "due_date", "priority", "status"], width=27)
    sort_key_combo.grid(row=0, column=1, padx=5, pady=5)

    tk.Button(sort_window, text="Apply", command=apply_sort, bg="#1e847f", fg="white", font=("Arial", 10, "bold")).grid(row=1, columnspan=2, pady=10)

def save_tasks_gui():
    filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if filename:
        save_tasks(tasks, filename)

def load_tasks_gui():
    global tasks
    filename = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if filename:
        tasks = load_tasks(filename)
        refresh_task_list(tree)

def notify_tasks_gui():
    overdue_tasks = [task for task in tasks if task["due_date"] < datetime.now() and task["status"] != "Completed"]
    if overdue_tasks:
        overdue_task_list = "\n".join([f"Task ID: {task['task_id']}, Description: {task['description']}" for task in overdue_tasks])
        messagebox.showwarning("Overdue Tasks", f"The following tasks are overdue:\n\n{overdue_task_list}")
    else:
        messagebox.showinfo("No Overdue Tasks", "There are no overdue tasks!")


# Main window setup
root = tk.Tk()
root.title("Task Manager")
root.configure(bg="#ecc19c")

columns = ("task_id", "description", "due_date", "priority", "status")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("task_id", text="Task ID")
tree.heading("description", text="Description")
tree.heading("due_date", text="Due Date")
tree.heading("priority", text="Priority")
tree.heading("status", text="Status")
tree.grid(row=0, column=0, columnspan=4, padx=100, pady=100)

button_width = 12
button_height = 2

tk.Button(root, text="Add Task", command=add_task_gui, bg="#1e847f", fg="white", font=("Arial", 10, "bold"), width=button_width, height=button_height).grid(row=1, column=0, padx=5, pady=5)
tk.Button(root, text="Update Task", command=update_task_gui, bg="#1e847f", fg="white", font=("Arial", 10, "bold"), width=button_width, height=button_height).grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="Delete Task", command=delete_task_gui, bg="#1e847f", fg="white", font=("Arial", 10, "bold"), width=button_width, height=button_height).grid(row=1, column=2, padx=5, pady=5)
tk.Button(root, text="Notify Tasks", command=notify_tasks_gui, bg="#1e847f", fg="white", font=("Arial", 10, "bold"), width=button_width, height=button_height).grid(row=1, column=3, padx=5, pady=5)
tk.Button(root, text="Filter Tasks", command=filter_tasks_gui, bg="#1e847f", fg="white", font=("Arial", 10, "bold"), width=button_width, height=button_height).grid(row=2, column=0, padx=5, pady=5)
tk.Button(root, text="Sort Tasks", command=sort_tasks_gui, bg="#1e847f", fg="white", font=("Arial", 10, "bold"), width=button_width, height=button_height).grid(row=2, column=1, padx=5, pady=5)
tk.Button(root, text="Save Tasks", command=save_tasks_gui, bg="#1e847f", fg="white", font=("Arial", 10, "bold"), width=button_width, height=button_height).grid(row=2, column=2, padx=5, pady=5)
tk.Button(root, text="Load Tasks", command=load_tasks_gui, bg="#1e847f", fg="white", font=("Arial", 10, "bold"), width=button_width, height=button_height).grid(row=2, column=3, padx=5, pady=5)
tk.Button(root, text="Exit", command=root.quit, bg="#000000", fg="white", font=("Arial", 10, "bold"), width=button_width, height=button_height).grid(row=3, columnspan=4, pady=10)
root.mainloop()
