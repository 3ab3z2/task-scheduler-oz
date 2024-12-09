import json
from datetime import datetime, timedelta
import curses

def create_task(task_id, description, due_date, priority, status="Pending"):
    return {
        "task_id": task_id,
        "description": description,
        "due_date": datetime.strptime(due_date, "%Y-%m-%d"),
        "priority": priority,
        "status": status
    }

def add_task(tasks, description, due_date, priority):
    task_id = len(tasks) + 1
    task = create_task(task_id, description, due_date, priority)
    return tasks + [task]

def update_task(tasks, task_id, description=None, due_date=None, priority=None, status=None):
    def update(t):
        if t["task_id"] == task_id:
            return {
                "task_id": t["task_id"],
                "description": description or t["description"],
                "due_date": datetime.strptime(due_date, "%Y-%m-%d") if due_date else t["due_date"],
                "priority": priority or t["priority"],
                "status": status or t["status"]
            }
        return t
    return list(map(update, tasks))

def delete_task(tasks, task_id):
    return [task for task in tasks if task["task_id"] != task_id]

def filter_tasks(tasks, **criteria):
    def matches(task):
        for key, value in criteria.items():
            if key == "due_date":
                value = datetime.strptime(value, "%Y-%m-%d")
            if task[key] != value:
                return False
        return True
    return list(filter(matches, tasks))

def sort_tasks(tasks, key):
    return sorted(tasks, key=lambda task: task[key])

def notify(tasks):
    notifications = []
    now = datetime.now()
    for task in tasks:
        if task["status"] == "Pending" and task["due_date"] < now:
            notifications.append(f"Task {task['task_id']} is overdue!")
        elif task["status"] == "Pending" and task["due_date"] - now <= timedelta(days=1):
            notifications.append(f"Task {task['task_id']} is nearing its deadline!")
    return notifications

def save_tasks(tasks, filename):
    with open(filename, "w") as file:
        json.dump([{
            "task_id": task["task_id"],
            "description": task["description"],
            "due_date": task["due_date"].strftime("%Y-%m-%d"),
            "priority": task["priority"],
            "status": task["status"]
        } for task in tasks], file)

def load_tasks(filename):
    with open(filename, "r") as file:
        tasks = json.load(file)
        return [{
            "task_id": task["task_id"],
            "description": task["description"],
            "due_date": datetime.strptime(task["due_date"], "%Y-%m-%d"),
            "priority": task["priority"],
            "status": task["status"]
        } for task in tasks]

def print_menu(stdscr):
    stdscr.clear()
    stdscr.addstr(1, 2, "Task Scheduler", curses.A_BOLD)
    stdscr.addstr(3, 2, "1. Add Task")
    stdscr.addstr(4, 2, "2. Update Task")
    stdscr.addstr(5, 2, "3. Delete Task")
    stdscr.addstr(6, 2, "4. View Tasks")
    stdscr.addstr(7, 2, "5. Save Tasks")
    stdscr.addstr(8, 2, "6. Load Tasks")
    stdscr.addstr(9, 2, "7. Exit")
    stdscr.refresh()

def get_input(stdscr, prompt, validation_func=None):
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, prompt)
        stdscr.refresh()
        curses.echo()
        input_str = stdscr.getstr(1, 0).decode("utf-8")
        curses.noecho()
        if validation_func:
            try:
                if validation_func(input_str):
                    return input_str
            except ValueError as e:
                stdscr.addstr(3, 0, str(e), curses.color_pair(4))
                stdscr.addstr(4, 0, "Please try again.", curses.color_pair(4))
                stdscr.refresh()
                stdscr.getch()
        else:
            return input_str

def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

def validate_int(input_str):
    if input_str.isdigit():
        return True
    else:
        raise ValueError("Invalid input. Please enter a number.")

def main(stdscr):
    tasks = []

    while True:
        print_menu(stdscr)
        choice = stdscr.getch()

        if choice == ord('1'):
            description = get_input(stdscr, "Enter description: ")
            due_date = get_input(stdscr, "Enter due date (YYYY-MM-DD): ", validate_date)
            priority = get_input(stdscr, "Enter priority: ", validate_int)
            tasks = add_task(tasks, description, due_date, priority)
        elif choice == ord('2'):
            task_id = int(get_input(stdscr, "Enter task ID to update: ", validate_int))
            description = get_input(stdscr, "Enter new description (leave blank to keep current): ")
            due_date = get_input(stdscr, "Enter new due date (YYYY-MM-DD, leave blank to keep current): ", validate_date) if get_input(stdscr, "Update due date? (y/n): ").lower() == 'y' else None
            priority = get_input(stdscr, "Enter new priority (leave blank to keep current): ")
            status = get_input(stdscr, "Enter new status (leave blank to keep current): ")
            tasks = update_task(tasks, task_id, description, due_date, priority, status)
        elif choice == ord('3'):
            task_id = int(get_input(stdscr, "Enter task ID to delete: ", validate_int))
            tasks = delete_task(tasks, task_id)
        elif choice == ord('4'):
            stdscr.clear()
            sorted_tasks = sort_tasks(tasks, "due_date")
            for idx, task in enumerate(sorted_tasks):
                color = curses.color_pair(3) if task["status"] == "Completed" else curses.color_pair(4) if task["due_date"] < datetime.now() else curses.color_pair(1)
                stdscr.addstr(idx + 1, 0, f"{task['task_id']}: {task['description']} - {task['due_date'].strftime('%Y-%m-%d')} - {task['priority']} - {task['status']}", color)
            stdscr.refresh()
            stdscr.getch()
        elif choice == ord('5'):
            filename = get_input(stdscr, "Enter filename to save tasks: ")
            save_tasks(tasks, filename)
        elif choice == ord('6'):
            filename = get_input(stdscr, "Enter filename to load tasks: ")
            tasks = load_tasks(filename)
        elif choice == ord('7'):
            break

curses.wrapper(main)
