import os

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

    def save_all_tasks(self):
        for task in self.tasks:
            save_task_to_file(task)

    def remove_task(self, task_id):
        self.tasks = [task for task in self.tasks if task.id != task_id]
        folder_path = ensure_tasks_folder()
        file_name = f"{folder_path}{task_id}.txt"
        if os.path.exists(file_name):
            os.remove(file_name)

    def add_task(self, title, description, deadline):
        task_id = max([task.id for task in self.tasks], default=0) + 1
        new_task = TaskRecord(task_id, title, description, deadline, False)
        self.tasks.append(new_task)
        save_task_to_file(new_task)
        return new_task
