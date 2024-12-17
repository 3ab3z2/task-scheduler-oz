import json
from datetime import datetime, timedelta
import curses
import re

# Function to create a task dictionary
def create_task(task_id, description, due_date, priority, status="Pending"):
    return {
        "task_id": task_id,
        "description": description,
        "due_date": datetime.strptime(due_date, "%Y-%m-%d"),
        "priority": priority,
        "status": status
    }

# Recursive function to append an item to a list (Tail recursion)
def append(lst, item):
    if not lst:
        return [item]
    return [lst[0]] + append(lst[1:], item)

# Recursive function to apply a function to each item in a list (Tail recursion) (First-class function example)
def map(func, lst):
    if not lst:
        return []
    return [func(lst[0])] + map(func, lst[1:])

# Recursive function to filter items in a list based on a function (Tail recursion) (Firt-class function example)
def filter(func, lst):
    if not lst:
        return []
    if func(lst[0]):
        return [lst[0]] + filter(func, lst[1:])
    return filter(func, lst[1:])

# Recursive function to apply a function to each item in a list without returning a new list (Tail recursion) (First-class function example)
def for_each(func, lst):
    if not lst:
        return
    func(lst[0])
    for_each(func, lst[1:])

# Function to clear the curses screen
def clear(stdscr):
    stdscr.clear()

# Function to add a string to the curses screen
def addstr(stdscr, y, x, string, attr=0):
    stdscr.addstr(y, x, string, attr)

# Function to refresh the curses screen
def refresh(stdscr):
    stdscr.refresh()

# Function to validate integer input using regular expressions
def validate_int(input_str):
    if re.fullmatch(r'\d+', input_str):
        return True
    else:
        raise ValueError("Invalid input. Please enter a number.")

# Function to validate date input using regular expressions
def validate_date(date_str):
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            raise ValueError("Invalid date format. Please use YYYY-MM-DD.")
    else:
        raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

# Function to get input from the user with optional validation
def get_input(stdscr, prompt, validation_func=None):
    while True:
        clear(stdscr)
        addstr(stdscr, 0, 0, prompt)
        refresh(stdscr)
        curses.echo()
        input_str = stdscr.getstr(1, 0).decode("utf-8")
        curses.noecho()
        if validation_func:
            try:
                if validation_func(input_str):
                    return input_str
            except ValueError as e:
                addstr(stdscr, 3, 0, str(e), curses.color_pair(4))
                addstr(stdscr, 4, 0, "Please try again.", curses.color_pair(4))
                refresh(stdscr)
                stdscr.getch()
        else:
            return input_str

# Function to print the menu using curses
def print_menu(stdscr, overdue_count):
    clear(stdscr)
    addstr(stdscr, 1, 2, "Task Scheduler", curses.A_BOLD)
    addstr(stdscr, 3, 2, "1. Add Task")
    addstr(stdscr, 4, 2, "2. Update Task")
    addstr(stdscr, 5, 2, "3. Delete Task")
    addstr(stdscr, 6, 2, "4. View Tasks")
    if overdue_count > 0:
        addstr(stdscr, 6, 16, f"({overdue_count})", curses.color_pair(4))
    addstr(stdscr, 7, 2, "5. Save Tasks")
    addstr(stdscr, 8, 2, "6. Load Tasks")
    addstr(stdscr, 9, 2, "7. Exit")
    refresh(stdscr)

# Function to add a task to the list of tasks
def add_task(tasks, description, due_date, priority):
    task_id = len(tasks) + 1
    task = create_task(task_id, description, due_date, priority)
    return append(tasks, task)

# Function to update a task in the list of tasks
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
    return map(update, tasks)

# Function to delete a task from the list of tasks
def delete_task(tasks, task_id):
    def filter_task(task):
        return task["task_id"] != task_id
    return filter(filter_task, tasks)

# Function to filter tasks based on given criteria
def filter_tasks(tasks, **criteria):
    def matches(task):
        for key, value in criteria.items():
            if key == "due_date":
                value = datetime.strptime(value, "%Y-%m-%d")
            if task[key] != value:
                return False
        return True
    return filter(matches, tasks)

# Function to sort tasks based on a given key
def sort_tasks(tasks, key):
    def quicksort(lst):
        if not lst:
            return []
        pivot = lst[0]
        less = [x for x in lst[1:] if x[key] <= pivot[key]]
        greater = [x for x in lst[1:] if x[key] > pivot[key]]
        return quicksort(less) + [pivot] + quicksort(greater)
    return quicksort(tasks)

# Function to notify about overdue or nearing deadline tasks
def notify(tasks):
    notifications = []
    now = datetime.now()
    def check_task(task):
        if task["status"] == "Pending" and task["due_date"] < now:
            notifications.append(f"Task {task['task_id']} is overdue!")
        elif task["status"] == "Pending" and task["due_date"] - now <= timedelta(days=1):
            notifications.append(f"Task {task['task_id']} is nearing its deadline!")
    for_each(check_task, tasks)
    return notifications

# Function to save tasks to a file
def save_tasks(tasks, filename):
    with open(filename, "w") as file:
        json.dump(map(lambda task: {
            "task_id": task["task_id"],
            "description": task["description"],
            "due_date": task["due_date"].strftime("%Y-%m-%d"),
            "priority": task["priority"],
            "status": task["status"]
        }, tasks), file)

# Function to load tasks from a file
def load_tasks(filename):
    with open(filename, "r") as file:
        tasks = json.load(file)
        return map(lambda task: {
            "task_id": task["task_id"],
            "description": task["description"],
            "due_date": datetime.strptime(task["due_date"], "%Y-%m-%d"),
            "priority": task["priority"],
            "status": task["status"]
        }, tasks)

# Main function to handle the task scheduler logic
def main(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)

    tasks = []

    def loop(tasks):
        overdue_count = len(filter(lambda t: t["status"] == "Pending" and t["due_date"] < datetime.now(), tasks))
        print_menu(stdscr, overdue_count)
        choice = stdscr.getch()

        if choice == ord('1'):
            description = get_input(stdscr, "Enter description: ")
            due_date = get_input(stdscr, "Enter due date (YYYY-MM-DD): ", validate_date)
            priority = get_input(stdscr, "Enter priority: ", validate_int)
            return loop(add_task(tasks, description, due_date, priority))
        elif choice == ord('2'):
            task_id = int(get_input(stdscr, "Enter task ID to update: ", validate_int))
            description = get_input(stdscr, "Enter new description (leave blank to keep current): ")
            due_date = get_input(stdscr, "Enter new due date (YYYY-MM-DD, leave blank to keep current): ", validate_date) if get_input(stdscr, "Update due date? (y/n): ").lower() == 'y' else None
            priority = get_input(stdscr, "Enter new priority (leave blank to keep current): ")
            status = get_input(stdscr, "Enter new status (leave blank to keep current): ")
            return loop(update_task(tasks, task_id, description, due_date, priority, status))
        elif choice == ord('3'):
            task_id = int(get_input(stdscr, "Enter task ID to delete: ", validate_int))
            return loop(delete_task(tasks, task_id))
        elif choice == ord('4'):
            clear(stdscr)
            sorted_tasks = sort_tasks(tasks, "due_date")
            now = datetime.now()
            for idx, task in enumerate(sorted_tasks):
                if task["status"] == "Completed":
                    color = curses.color_pair(3)
                elif task["due_date"] < now:
                    color = curses.color_pair(4)
                elif task["due_date"] - now <= timedelta(days=1):
                    color = curses.color_pair(2)
                else:
                    color = curses.color_pair(1)
                addstr(stdscr, idx + 1, 0, f"{task['task_id']}: {task['description']} - {task['due_date'].strftime('%Y-%m-%d')} - {task['priority']} - {task['status']}", color)
            refresh(stdscr)
            stdscr.getch()
            return loop(tasks)
        elif choice == ord('5'):
            filename = get_input(stdscr, "Enter filename to save tasks: ")
            save_tasks(tasks, filename)
            return loop(tasks)
        elif choice == ord('6'):
            filename = get_input(stdscr, "Enter filename to load tasks: ")
            return loop(load_tasks(filename))
        elif choice == ord('7'):
            return

    loop(tasks)

curses.wrapper(main)