import os
from tkinter import Tk, Button, Label, Frame, Toplevel, Entry, Listbox, Scrollbar, messagebox
from tkinter import ttk


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
                task_id = int(file_name[:-4])  # Remove .txt to get the task ID
                tasks.append(TaskRecord(task_id, title, description, deadline, completed))
    return tasks


# TaskManager class to manage tasks
class TaskManager:
    def __init__(self):
        self.tasks = load_tasks()

    def add_task(self, title, description, deadline):
        task_id = max([task.id for task in self.tasks], default=0) + 1
        new_task = TaskRecord(task_id, title, description, deadline, False)
        self.tasks.append(new_task)
        save_task_to_file(new_task)

    def remove_task(self, task_id):
        self.tasks = [task for task in self.tasks if task.id != task_id]
        folder_path = ensure_tasks_folder()
        file_name = f"{folder_path}{task_id}.txt"
        if os.path.exists(file_name):
            os.remove(file_name)

    def mark_task_complete(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                task.completed = True
                save_task_to_file(task)

    def edit_task(self, task_id, new_title, new_description, new_deadline):
        for task in self.tasks:
            if task.id == task_id:
                task.title = new_title
                task.description = new_description
                task.deadline = new_deadline
                save_task_to_file(task)


# UI: View Tasks in a new window
def view_tasks_ui(manager):
    tasks = manager.tasks
    task_list = [(f"{task.id}: {task.title} (Completed: {task.completed})") for task in tasks]

    # Create a new window
    view_window = Toplevel()
    view_window.title("View Tasks")
    view_window.geometry("500x400")
    view_window.configure(bg="#f9f9f9")

    Label(view_window, text="Tasks List", font=("Helvetica", 16), bg="#f9f9f9").pack(pady=10)

    frame = Frame(view_window)
    frame.pack(fill="both", expand=True)

    scrollbar = Scrollbar(frame, orient="vertical")
    listbox = Listbox(frame, yscrollcommand=scrollbar.set, font=("Arial", 12), width=50, height=15)

    for item in task_list:
        listbox.insert("end", item)

    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side="right", fill="y")
    listbox.pack(side="left", fill="both", expand=True)


# UI: Add Task
def add_task_ui(manager):
    def save_task():
        title = title_entry.get()
        description = description_entry.get()
        deadline = deadline_entry.get()
        if title and description and deadline:
            manager.add_task(title, description, deadline)
            messagebox.showinfo("Success", "Task added successfully!")
            add_window.destroy()
        else:
            messagebox.showerror("Error", "All fields are required!")

    # Create a new window
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

    Button(add_window, text="Save Task", command=save_task, bg="#4caf50", fg="white").pack(pady=15)


# UI: Remove Task
def remove_task_ui(manager):
    def delete_task():
        try:
            task_id = int(task_id_entry.get())
            manager.remove_task(task_id)
            messagebox.showinfo("Success", "Task removed successfully!")
            remove_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid Task ID!")

    # Create a new window
    remove_window = Toplevel()
    remove_window.title("Remove Task")
    remove_window.geometry("300x150")
    remove_window.configure(bg="#f9f9f9")

    Label(remove_window, text="Task ID:", bg="#f9f9f9").pack(pady=10)
    task_id_entry = Entry(remove_window, width=30)
    task_id_entry.pack()

    Button(remove_window, text="Delete Task", command=delete_task, bg="#f44336", fg="white").pack(pady=15)


# UI: Mark Task Complete
def mark_complete_ui(manager):
    def mark_complete():
        try:
            task_id = int(task_id_entry.get())
            manager.mark_task_complete(task_id)
            messagebox.showinfo("Success", "Task marked as complete!")
            complete_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid Task ID!")

    # Create a new window
    complete_window = Toplevel()
    complete_window.title("Mark Task Complete")
    complete_window.geometry("300x150")
    complete_window.configure(bg="#f9f9f9")

    Label(complete_window, text="Task ID:", bg="#f9f9f9").pack(pady=10)
    task_id_entry = Entry(complete_window, width=30)
    task_id_entry.pack()

    Button(complete_window, text="Mark Complete", command=mark_complete, bg="#2196f3", fg="white").pack(pady=15)


# Run Task Manager UI
def run_tui():
    manager = TaskManager()
    root = Tk()
    root.title("Task Manager")
    root.geometry("400x400")
    root.configure(bg="#ffffff")

    header = Label(root, text="Task Manager", font=("Helvetica", 18, "bold"), bg="#ffffff")
    header.pack(pady=15)

    Button(root, text="Add Task", command=lambda: add_task_ui(manager), width=25, bg="#4caf50", fg="white").pack(pady=5)
    Button(root, text="Remove Task", command=lambda: remove_task_ui(manager), width=25, bg="#f44336", fg="white").pack(pady=5)
    Button(root, text="Mark Complete", command=lambda: mark_complete_ui(manager), width=25, bg="#2196f3", fg="white").pack(pady=5)
    Button(root, text="View Tasks", command=lambda: view_tasks_ui(manager), width=25, bg="#ff9800", fg="white").pack(pady=5)

    root.mainloop()


# Start the application
if __name__ == "__main__":
    run_tui()
