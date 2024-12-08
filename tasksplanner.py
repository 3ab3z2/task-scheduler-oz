import os


# Function to check if the folder exists
def check_folder_exists(folder_path):
    try:
        os.listdir(folder_path)
        return True
    except FileNotFoundError:
        return False


# Function to create the folder if it doesn't exist
def ensure_tasks_folder():
    folder_path = "tasks/"
    if not check_folder_exists(folder_path):
        os.makedirs(folder_path)
    return folder_path


# Function to save a task to a file
def save_task_to_file(task_id, title, description, deadline, completed):
    folder_path = ensure_tasks_folder()
    file_name = f"{folder_path}{task_id}.txt"
    with open(file_name, "w") as file:
        file.write(f"{title}\n")
        file.write(f"{description}\n")
        file.write(f"{deadline}\n")
        file.write(f"{str(completed)}\n")


# Function to load all tasks from the folder
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
                tasks.append((task_id, title, description, deadline, completed))
    return tasks


# Function to remove a task
def remove_task(task_id):
    folder_path = ensure_tasks_folder()
    file_name = f"{folder_path}{task_id}.txt"

    if os.path.exists(file_name):
        os.remove(file_name) 
        print(f"Task with ID {task_id} has been removed.")
    else:
        print(f"File for task ID {task_id} not found.")


# Function to display all tasks
def view_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
    else:
        for task in tasks:
            print(
                f"ID: {task[0]}, Title: {task[1]}, Description: {task[2]}, Deadline: {task[3]}, Completed: {'Yes' if task[4] else 'No'}")


# Function to add a new task
def add_task(tasks):
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    deadline = input("Enter task deadline: ")
    if title and description and deadline:
        task_id = max([task[0] for task in tasks], default=0) + 1
        tasks.append((task_id, title, description, deadline, False)) 
        save_task_to_file(task_id, title, description, deadline, False)
        print("Task added successfully!")
    else:
        print("All fields are required!")
    return tasks


# Function to update the completion status of a task
def update_task_completion(tasks):
    for task in tasks:
        print(f"Task ID: {task[0]} - Title: {task[1]} - Completed: {'Yes' if task[4] else 'No'}")

    task_id = int(input("Enter task ID to mark as completed: "))
    tasks = [
        (task[0], task[1], task[2], task[3], True) if task[0] == task_id else task
        for task in tasks
    ]
    save_task_to_file(task_id, task[1], task[2], task[3], True)
    print("Task marked as completed.")
    return tasks


# Function to run the task manager application
def run_app():
    tasks = load_tasks() 
    while True:
        print("\nTask Manager")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task Completion")
        print("4. Delete Task")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            tasks = add_task(tasks) 
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            tasks = update_task_completion(tasks) 
        elif choice == "4":
            task_id_to_remove = int(input("Enter the task ID to delete: "))
            remove_task(task_id_to_remove) 
            tasks = load_tasks() 
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    run_app()
