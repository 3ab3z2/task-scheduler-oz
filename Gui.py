from tkinter import Tk, Button, Label, Frame, Toplevel, Entry, BooleanVar, Checkbutton, messagebox, Canvas, Scrollbar
from tasksplanner import TaskManager

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
    view_window.configure(bg="#E7A1B0")

    Label(view_window, text="Tasks List", font=("Helvetica", 16), bg="#E7A1B0", fg="white").pack(pady=10)

    container = Frame(view_window, bg="#7E354D")
    container.pack(fill="both", expand=True)

    canvas = Canvas(container, bg="#E7A1B0", highlightthickness=0)
    scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="#E7A1B0")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for task in manager.tasks:
        frame = Frame(scrollable_frame, bg="#E7A1B0", pady=5)
        frame.pack(fill="x", padx=10)

        Label(
            frame,
            text=f"ID: {task.id}\nTitle: {task.title}\nDescription: {task.description}\nDeadline: {task.deadline}\nCompleted: {'Yes' if task.completed else 'No'}",
            justify="left",
            bg="#E7A1B0",
            anchor="w",
            fg="#7E354D"
        ).pack(anchor="w", pady=5)

    
        delete_button = Button(frame, text="Delete", command=lambda task_id=task.id: delete_task(task_id), bg="#7F4E52", fg="white")
        delete_button.pack(side="right", padx=10)

        Label(frame, text="-" * 50, bg="#E7A1B0").pack(anchor="w")

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
    view_window.configure(bg="#E7A1B0")

    Label(view_window, text="Tasks List with Completion", font=("Helvetica", 16), bg="#E7A1B0", fg="white").pack(pady=10)

    checkbox_vars = []

    for task in manager.tasks:
        frame = Frame(view_window, bg="#E7A1B0")
        frame.pack(anchor="w", padx=10, pady=5)

        var = BooleanVar(value=task.completed)
        checkbox_vars.append(var)

        Checkbutton(
            frame, text=f"{task.id}: {task.title} (Deadline: {task.deadline})", variable=var, bg="#E7A1B0", fg="#7E354D"
        ).pack(side="left", anchor="w")

    Button(view_window, text="Save Changes", command=save_changes, bg="#7F4E52", fg="white").pack(pady=15)

# UI: Add Task
def add_task_ui(manager):
    def save_task():
        title = title_entry.get()
        description = description_entry.get()
        deadline = deadline_entry.get()
        if title and description and deadline:
            task_id = max([task.id for task in manager.tasks], default=0) + 1
            new_task = manager.add_task(title, description, deadline)
            messagebox.showinfo("Success", "Task added successfully!")
            add_window.destroy()
        else:
            messagebox.showerror("Error", "All fields are required!")

    add_window = Toplevel()
    add_window.title("Add Task")
    add_window.geometry("350x300")
    add_window.configure(bg="#E7A1B0") 

    Label(add_window, text="Add New Task", font=("Helvetica", 16), bg="#E7A1B0", fg="white").pack(pady=10)

    Label(add_window, text="Title:", bg="#E7A1B0", fg="#7E354D").pack(pady=5)
    title_entry = Entry(add_window, width=30)
    title_entry.pack()

    Label(add_window, text="Description:", bg="#E7A1B0", fg="#7E354D").pack(pady=5)
    description_entry = Entry(add_window, width=30)
    description_entry.pack()

    Label(add_window, text="Deadline:", bg="#E7A1B0", fg="#7E354D").pack(pady=5)
    deadline_entry = Entry(add_window, width=30)
    deadline_entry.pack()

    Button(add_window, text="Save Task", command=save_task, bg="#7F4E52", fg="white").pack(pady=15)

# Main Application Window
def run_app():
    root = Tk()
    root.title("Task Manager")
    root.geometry("500x500")
    root.configure(bg="#7E354D")

    button_frame = Frame(root, bg="#7E354D")
    button_frame.pack(pady=30)

    Button(button_frame, text="Add Task", command=lambda: add_task_ui(manager), width=20, bg="#7F4E52", fg="white", font=("Helvetica", 14)).pack(pady=5)
    Button(button_frame, text="View Tasks", command=lambda: view_tasks_ui(manager), width=20, bg="#7F4E52", fg="white", font=("Helvetica", 14)).pack(pady=5)
    Button(button_frame, text="Complete Tasks", command=lambda: view_tasks_with_checkboxes(manager), width=20, bg="#7F4E52", fg="white", font=("Helvetica", 14)).pack(pady=5)
    exit_button = Button(root, text="Exit", command=root.quit, width=20, bg="#7F4E52", fg="white",font=("Helvetica", 14))
    exit_button.pack(pady=20)

    manager = TaskManager() 

    root.mainloop()
