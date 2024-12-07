import os
from tkinter import Tk, Button, Label, Frame, Toplevel, Entry, BooleanVar, Checkbutton, messagebox, Canvas, Scrollbar

# TaskRecord class to represent a single task
class TaskRecord:
    def __init__(self, task_id, title, description, deadline, completed):
        self.id = task_id
        self.title = title
        self.description = description
        self.deadline = deadline
        self.completed = completed

# Ensure tasks folder exists
def ensure_tasks_folder():
    folder_path = "tasks/"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

# Save task to file
def save_task_to_file(task):
    folder_path = ensure_tasks_folder()
    file_name = f"{folder_path}{task.id}.txt"
    with open(file_name, "w") as file:
        file.write(f"{task.title}\n")
        file.write(f"{task.description}\n")
        file.write(f"{task.deadline}\n")
        file.write(f"{str(task.completed)}\n")

# Load tasks from files
def load_tasks():
    folder_path = ensure_tasks_folder()
    tasks = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "r") as file:
                title = file.readline().strip()
                description = file.readline().strip()
                deadline = file.readline().strip()
                completed = file.readline().strip() == "True"
                task_id = int(file_name[:-4])
                tasks.append(TaskRecord(task_id, title, description, deadline, completed))
    return tasks

# TaskManager class to manage tasks
class TaskManager:
    def __init__(self):
        self.tasks = load_tasks()

    def save_all_tasks(self):
        for task in self.tasks:
            save_task_to_file(task)

    def remove_task(self, task_id):
        self.tasks = [task for task in self.tasks if task.id != task_id]
        folder_path = ensure_tasks_folder()
        file_name = f"{folder_path}{task_id}.txt"
        if os.path.exists(file_name):
            os.remove(file_name)

# UI: View Tasks with Delete Buttons
def view_tasks_ui(manager):
    def delete_task(task_id):
        manager.remove_task(task_id)
        messagebox.showinfo("Success", "Task deleted successfully!")
        view_window.destroy()
        view_tasks_ui(manager)

    view_window = Toplevel()
    view_window.title("View Tasks")
    view_window.geometry("500x400")
    view_window.configure(bg="#E3E4FA")

    Label(view_window, text="Tasks List", font=("Helvetica", 16), bg="#E3E4FA").pack(pady=10)

    container = Frame(view_window)
    container.pack(fill="both", expand=True)

    canvas = Canvas(container, bg="#E3E4FA", highlightthickness=0)
    scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="#E3E4FA")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for task in manager.tasks:
        frame = Frame(scrollable_frame, bg="#E3E4FA", pady=5)
        frame.pack(fill="x", padx=10)

        Label(
            frame,
            text=f"ID: {task.id}\nTitle: {task.title}\nDescription: {task.description}\nDeadline: {task.deadline}\nCompleted: {'Yes' if task.completed else 'No'}",
            justify="left",
            bg="#E3E4FA",
            anchor="w",
        ).pack(anchor="w", pady=5)

        # Delete button
        delete_button = Button(frame, text="Delete", command=lambda task_id=task.id: delete_task(task_id), bg="#FF0000", fg="#000000")
        delete_button.pack(side="right", padx=10)

        Label(frame, text="-" * 50, bg="#E3E4FA").pack(anchor="w")

# UI: Complete tasks
def view_tasks_with_checkboxes(manager):
    def save_changes():
        for index, var in enumerate(checkbox_vars):
            manager.tasks[index].completed = var.get()
        manager.save_all_tasks()
        messagebox.showinfo("Success", "Tasks updated successfully!")
        view_window.destroy()

    view_window = Toplevel()
    view_window.title("Tasks with Checkboxes")
    view_window.geometry("500x400")
    view_window.configure(bg="#E3E4FA")

    Label(view_window, text="Tasks List with Completion", font=("Helvetica", 16), bg="#E3E4FA").pack(pady=10)

    checkbox_vars = []

    for task in manager.tasks:
        frame = Frame(view_window, bg="#E3E4FA")
        frame.pack(anchor="w", padx=10, pady=5)

        var = BooleanVar(value=task.completed)
        checkbox_vars.append(var)

        Checkbutton(
            frame, text=f"{task.id}: {task.title} (Deadline: {task.deadline})", variable=var, bg="#E3E4FA"
        ).pack(side="left", anchor="w")

    Button(view_window, text="Save Changes", command=save_changes, bg="#7F4E52", fg="#E3E4FA").pack(pady=15)

# # UI: Delete Task
# def delete_task_ui(manager):
#     def delete_task():
#         try:
#             task_id = int(task_id_entry.get())
#             manager.remove_task(task_id)
#             messagebox.showinfo("Success", "Task deleted successfully!")
#             delete_window.destroy()
#         except ValueError:
#             messagebox.showerror("Error", "Invalid Task ID!")
#
#     delete_window = Toplevel()
#     delete_window.title("Delete Task")
#     delete_window.geometry("300x150")
#     delete_window.configure(bg="#f9f9f9")
#
#     Label(delete_window, text="Task ID to Delete:", bg="#f9f9f9").pack(pady=10)
#     task_id_entry = Entry(delete_window, width=30)
#     task_id_entry.pack()
#
#     Button(delete_window, text="Delete Task", command=delete_task, bg="#f44336", fg="white").pack(pady=15)

# UI: Add Task
def add_task_ui(manager):
    def save_task():
        title = title_entry.get()
        description = description_entry.get()
        deadline = deadline_entry.get()
        if title and description and deadline:
            task_id = max([task.id for task in manager.tasks], default=0) + 1
            new_task = TaskRecord(task_id, title, description, deadline, False)
            manager.tasks.append(new_task)
            save_task_to_file(new_task)
            messagebox.showinfo("Success", "Task added successfully!")
            add_window.destroy()
        else:
            messagebox.showerror("Error", "All fields are required!")

    add_window = Toplevel()
    add_window.title("Add Task")
    add_window.geometry("350x300")
    add_window.configure(bg="#f9f9f9")

    Label(add_window, text="Add New Task", font=("Helvetica", 16), bg="#f9f9f9").pack(pady=10)

    Label(add_window, text="Title:", bg="#f9f9f9").pack(pady=5)
    title_entry = Entry(add_window, width=30)
    title_entry.pack()

    Label(add_window, text="Description:", bg="#f9f9f9").pack(pady=5)
    description_entry = Entry(add_window, width=30)
    description_entry.pack()

    Label(add_window, text="Deadline:", bg="#f9f9f9").pack(pady=5)
    deadline_entry = Entry(add_window, width=30)
    deadline_entry.pack()

    Button(add_window, text="Save Task", command=save_task, bg="#E799A3", fg="#000000").pack(pady=15)

# Main Application
def run_app():
    manager = TaskManager()
    root = Tk()
    root.title("Task Manager")
    root.geometry("600x600")
    root.configure(bg="#E3E4FA")

    Label(root, text="Task Manager", font=("Helvetica", 18, "bold"), bg="#E3E4FA").pack(pady=15)

    button_frame = Frame(root, bg="#E3E4FA")
    button_frame.pack(pady=150)

    Button(button_frame, text="Add Task", command=lambda: add_task_ui(manager), width=20, bg="#E799A3", fg="#000000", font=("Helvetica", 14, "bold")).pack(pady=10)
    Button(button_frame, text="View Tasks", command=lambda: view_tasks_ui(manager), width=20, bg="#806D7E", fg="#000000", font=("Helvetica", 14, "bold")).pack(pady=10)
    Button(button_frame, text="Complete Tasks", command=lambda: view_tasks_with_checkboxes(manager), width=20, bg="#7F4E52", fg="#000000", font=("Helvetica", 14, "bold")).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    run_app()
