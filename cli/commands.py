# ============================================
# cli/commands.py
# All CLI commands for Task Manager
# ============================================

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.project_service import ProjectService
from services.task_service import TaskService
from utils.formatter import (
    format_projects_table,
    format_tasks_table,
    print_project_details,
    print_task_details,
    print_success,
    print_error,
    print_warning,
    print_info
)

# Create service instances
project_service = ProjectService()
task_service = TaskService()


# ── Project Commands ──────────────────────

def create_project(args):
    # Create new project
    # args.name        → project name
    # args.description → project description (optional)
    description = args.description if hasattr(args, 'description') else None
    project = project_service.create_project(args.name, description)
    if project:
        print_project_details(project)


def list_projects(args):
    # List all projects in table format
    projects = project_service.get_all_projects()
    if projects:
        print_info(f"Total projects: {len(projects)}")
        format_projects_table(projects)


def view_project(args):
    # View single project details
    project = project_service.get_project(args.id)
    if project:
        print_project_details(project)


def delete_project(args):
    # Delete project by id
    project_service.delete_project(args.id)


# ── Task Commands ─────────────────────────

def create_task(args):
    # Create new task
    description = args.description if hasattr(args, 'description') else None
    due_date = args.due_date if hasattr(args, 'due_date') else None
    priority = args.priority if hasattr(args, 'priority') else "medium"

    task = task_service.create_task(
        title=args.title,
        project_id=args.project_id,
        description=description,
        priority=priority,
        due_date=due_date
    )
    if task:
        print_task_details(task)


def list_tasks(args):
    # List all tasks or tasks for specific project
    if hasattr(args, 'project_id') and args.project_id:
        tasks = task_service.get_tasks_by_project(args.project_id)
        print_info(f"Tasks for project {args.project_id}:")
    else:
        tasks = task_service.get_all_tasks()
        print_info(f"Total tasks: {len(tasks)}")

    if tasks:
        format_tasks_table(tasks)


def complete_task(args):
    # Mark task as completed
    result = task_service.complete_task(args.id)
    if result:
        print_success(f"Task {args.id} marked as completed!")


def delete_task(args):
    # Delete task by id
    task_service.delete_task(args.id)


def update_task_status(args):
    # Update task status
    result = task_service.update_status(args.id, args.status)
    if result:
        print_success(f"Task {args.id} status updated to '{args.status}'!")