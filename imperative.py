import json
from datetime import datetime, timedelta
import curses

class Task:
    def __init__(self, task_id, description, due_date, priority, status="Pending"):
        self.task_id = task_id
        self.description = description
        self.due_date = datetime.strptime(due_date, "%Y-%m-%d")
        self.priority = priority
        self.status = status

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "description": self.description,
            "due_date": self.due_date.strftime("%Y-%m-%d"),
            "priority": self.priority,
            "status": self.status
        }

class TaskScheduler:
    def __init__(self):
        self.tasks = []

    def add_task(self, description, due_date, priority):
        task_id = len(self.tasks) + 1
        task = Task(task_id, description, due_date, priority)
        self.tasks.append(task)

    def update_task(self, task_id, description=None, due_date=None, priority=None, status=None):
        for task in self.tasks:
            if task.task_id == task_id:
                if description:
                    task.description = description
                if due_date:
                    task.due_date = datetime.strptime(due_date, "%Y-%m-%d")
                if priority:
                    task.priority = priority
                if status:
                    task.status = status
                break

    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task.task_id != task_id]

    def filter_tasks(self, **criteria):
        filtered_tasks = self.tasks
        if "status" in criteria:
            filtered_tasks = [task for task in filtered_tasks if task.status == criteria["status"]]
        if "priority" in criteria:
            filtered_tasks = [task for task in filtered_tasks if task.priority == criteria["priority"]]
        if "due_date" in criteria:
            filtered_tasks = [task for task in filtered_tasks if task.due_date == datetime.strptime(criteria["due_date"], "%Y-%m-%d")]
        return filtered_tasks

    def sort_tasks(self, key):
        return sorted(self.tasks, key=lambda task: getattr(task, key))

    def notify(self):
        notifications = []
        now = datetime.now()
        for task in self.tasks:
            if task.status == "Pending" and task.due_date < now:
                notifications.append(f"Task {task.task_id} is overdue!")
            elif task.status == "Pending" and task.due_date - now <= timedelta(days=1):
                notifications.append(f"Task {task.task_id} is nearing its deadline!")
        return notifications

    def save_tasks(self, filename):
        with open(filename, "w") as file:
            json.dump([task.to_dict() for task in self.tasks], file)

    def load_tasks(self, filename):
        with open(filename, "r") as file:
            tasks = json.load(file)
            self.tasks = [Task(**task) for task in tasks]

def main(stdscr):
    scheduler = TaskScheduler()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)

    def print_menu():
        stdscr.clear()
        stdscr.attron(curses.color_pair(1))
        stdscr.border(0)
        stdscr.addstr(1, 2, "Task Scheduler", curses.A_BOLD)
        stdscr.attroff(curses.color_pair(1))
        stdscr.addstr(3, 2, "1. Add Task")
        stdscr.addstr(4, 2, "2. Update Task")
        stdscr.addstr(5, 2, "3. Delete Task")
        stdscr.addstr(6, 2, "4. View Tasks")
        stdscr.addstr(7, 2, "5. Save Tasks")
        stdscr.addstr(8, 2, "6. Load Tasks")
        stdscr.addstr(9, 2, "7. Exit")
        stdscr.refresh()

    def get_input(prompt, validation_func=None):
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
                    stdscr.addstr(2, 0, str(e), curses.color_pair(4))
                    stdscr.addstr(3, 0, "Please try again.", curses.color_pair(4))
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

    while True:
        print_menu()
        choice = stdscr.getch()

        if choice == ord('1'):
            description = get_input("Enter description: ")
            due_date = get_input("Enter due date (YYYY-MM-DD): ", validate_date)
            priority = get_input("Enter priority: ")
            scheduler.add_task(description, due_date, priority)
        elif choice == ord('2'):
            task_id = int(get_input("Enter task ID to update: ", validate_int))
            description = get_input("Enter new description (leave blank to keep current): ")
            due_date = get_input("Enter new due date (YYYY-MM-DD, leave blank to keep current): ", validate_date) if get_input("Update due date? (y/n): ").lower() == 'y' else None
            priority = get_input("Enter new priority (leave blank to keep current): ")
            status = get_input("Enter new status (leave blank to keep current): ")
            scheduler.update_task(task_id, description, due_date, priority, status)
        elif choice == ord('3'):
            task_id = int(get_input("Enter task ID to delete: ", validate_int))
            scheduler.delete_task(task_id)
        elif choice == ord('4'):
            stdscr.clear()
            tasks = scheduler.sort_tasks("due_date")
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(0, 0, "Tasks:")
            stdscr.attroff(curses.color_pair(2))
            for idx, task in enumerate(tasks):
                color = curses.color_pair(3) if task.status == "Completed" else curses.color_pair(4) if task.due_date < datetime.now() else curses.color_pair(1)
                stdscr.addstr(idx + 1, 0, f"{task.task_id}: {task.description} - {task.due_date.strftime('%Y-%m-%d')} - {task.priority} - {task.status}", color)
            stdscr.refresh()
            stdscr.getch()
        elif choice == ord('5'):
            filename = get_input("Enter filename to save tasks: ")
            scheduler.save_tasks(filename)
        elif choice == ord('6'):
            filename = get_input("Enter filename to load tasks: ")
            scheduler.load_tasks(filename)
        elif choice == ord('7'):
            break

curses.wrapper(main)