# ============================================
# utils/formatter.py
# Display output nicely in terminal
# Uses tabulate for tables and colorama for colors
# ============================================

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tabulate import tabulate
from colorama import Fore, Style, init

# Initialize colorama — needed for Windows!
init(autoreset=True)

# autoreset=True → colors reset automatically after each print
# Without it → all text becomes colored! 😱


def print_success(message: str) -> None:
    # Print green success message
    print(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")


def print_error(message: str) -> None:
    # Print red error message
    print(f"{Fore.RED}❌ {message}{Style.RESET_ALL}")


def print_warning(message: str) -> None:
    # Print yellow warning message
    print(f"{Fore.YELLOW}⚠️  {message}{Style.RESET_ALL}")


def print_info(message: str) -> None:
    # Print blue info message
    print(f"{Fore.CYAN}ℹ️  {message}{Style.RESET_ALL}")


def format_projects_table(projects: list) -> None:
    # ── Display projects in clean table format ──

    if not projects:
        print_warning("No projects found!")
        return

    # Build table data
    # Each row = one project
    table_data = []
    for project in projects:
        table_data.append([
            project.id,
            project.name,
            project.status,
            project.created_at
        ])

    # tabulate() → converts list to clean table
    # headers    → column names
    # tablefmt   → table style
    print(tabulate(
        table_data,
        headers=["ID", "Name", "Status", "Created"],
        tablefmt="rounded_outline"
    ))


def format_tasks_table(tasks: list) -> None:
    # ── Display tasks in clean table format ──

    if not tasks:
        print_warning("No tasks found!")
        return

    table_data = []
    for task in tasks:
        # Color priority based on level
        if task.priority == "high":
            priority = f"{Fore.RED}{task.priority}{Style.RESET_ALL}"
        elif task.priority == "medium":
            priority = f"{Fore.YELLOW}{task.priority}{Style.RESET_ALL}"
        else:
            priority = f"{Fore.GREEN}{task.priority}{Style.RESET_ALL}"

        # Color status
        if task.status == "completed":
            status = f"{Fore.GREEN}{task.status}{Style.RESET_ALL}"
        elif task.status == "in_progress":
            status = f"{Fore.YELLOW}{task.status}{Style.RESET_ALL}"
        else:
            status = f"{Fore.WHITE}{task.status}{Style.RESET_ALL}"

        table_data.append([
            task.id,
            task.title,
            status,
            priority,
            task.project_id,
            task.created_at
        ])

    print(tabulate(
        table_data,
        headers=["ID", "Title", "Status", "Priority", "Project ID", "Created"],
        tablefmt="rounded_outline"
    ))


def print_project_details(project) -> None:
    # ── Display single project details ──
    print(f"\n{Fore.CYAN}{'='*40}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Project Details{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*40}{Style.RESET_ALL}")
    print(f"ID          : {project.id}")
    print(f"Name        : {project.name}")
    print(f"Status      : {project.status}")
    print(f"Description : {project.description or 'N/A'}")
    print(f"Created     : {project.created_at}")
    print(f"{Fore.CYAN}{'='*40}{Style.RESET_ALL}\n")


def print_task_details(task) -> None:
    # ── Display single task details ──
    print(f"\n{Fore.CYAN}{'='*40}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Task Details{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*40}{Style.RESET_ALL}")
    print(f"ID          : {task.id}")
    print(f"Title       : {task.title}")
    print(f"Status      : {task.status}")
    print(f"Priority    : {task.priority}")
    print(f"Project ID  : {task.project_id}")
    print(f"Description : {task.description or 'N/A'}")
    print(f"Due Date    : {task.due_date or 'N/A'}")
    print(f"Created     : {task.created_at}")
    print(f"{Fore.CYAN}{'='*40}{Style.RESET_ALL}\n")


# ============================================
# Testing — remove when project is complete
# ============================================
if __name__ == "__main__":
    from db.database import init_db
    from services.project_service import ProjectService
    from services.task_service import TaskService

    init_db()

    project_service = ProjectService()
    task_service = TaskService()

    # Create test data
    p1 = project_service.create_project("Build Website", "Company website")
    p2 = project_service.create_project("Mobile App", "iOS app")

    t1 = task_service.create_task("Build Login", p1.id, priority="high")
    t2 = task_service.create_task("Build Dashboard", p1.id, priority="medium")
    t3 = task_service.create_task("Write Tests", p1.id, priority="low")

    print("\n📋 All Projects:")
    projects = project_service.get_all_projects()
    format_projects_table(projects)

    print("\n📋 All Tasks:")
    tasks = task_service.get_all_tasks()
    format_tasks_table(tasks)

    print("\n📋 Project Details:")
    print_project_details(p1)

    print("\n📋 Task Details:")
    print_task_details(t1)

    print_success("Everything working!")
    print_error("This is an error message")
    print_warning("This is a warning")
    print_info("This is info")