# ============================================
# cli/parser.py
# Argument parsing for Task Manager CLI
# This is what reads user commands!
# Example: python main.py project create "My Project"
# ============================================

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
from cli.commands import (
    create_project, list_projects, view_project, delete_project,
    create_task, list_tasks, complete_task, delete_task, update_task_status
)


def create_parser():
    # ── Main parser ──
    # This is the root of all commands!
    parser = argparse.ArgumentParser(
        prog="task-manager",
        description="Task Manager CLI — Manage your projects and tasks!",
        epilog="Example: python main.py project create 'My Project'"
    )

    # ── Subparsers ──
    # Subparsers allow different commands
    # like: python main.py project ...
    #       python main.py task ...
    subparsers = parser.add_subparsers(
        title="commands",
        description="Available commands",
        dest="command"
    )

    # ════════════════════════════════════════
    # PROJECT COMMANDS
    # ════════════════════════════════════════
    project_parser = subparsers.add_parser(
        "project",
        help="Manage projects"
    )

    project_subparsers = project_parser.add_subparsers(
        dest="project_command"
    )

    # ── project create ──
    # python main.py project create "My Project"
    project_create = project_subparsers.add_parser(
        "create",
        help="Create a new project"
    )
    project_create.add_argument(
        "name",
        type=str,
        help="Project name"
    )
    project_create.add_argument(
        "--description", "-d",
        type=str,
        help="Project description (optional)",
        default=None
    )
    project_create.set_defaults(func=create_project)

    # ── project list ──
    # python main.py project list
    project_list = project_subparsers.add_parser(
        "list",
        help="List all projects"
    )
    project_list.set_defaults(func=list_projects)

    # ── project view ──
    # python main.py project view 1
    project_view = project_subparsers.add_parser(
        "view",
        help="View project details"
    )
    project_view.add_argument(
        "id",
        type=int,
        help="Project ID"
    )
    project_view.set_defaults(func=view_project)

    # ── project delete ──
    # python main.py project delete 1
    project_delete = project_subparsers.add_parser(
        "delete",
        help="Delete a project"
    )
    project_delete.add_argument(
        "id",
        type=int,
        help="Project ID"
    )
    project_delete.set_defaults(func=delete_project)

    # ════════════════════════════════════════
    # TASK COMMANDS
    # ════════════════════════════════════════
    task_parser = subparsers.add_parser(
        "task",
        help="Manage tasks"
    )

    task_subparsers = task_parser.add_subparsers(
        dest="task_command"
    )

    # ── task create ──
    # python main.py task create "Build Login" 1 --priority high
    task_create = task_subparsers.add_parser(
        "create",
        help="Create a new task"
    )
    task_create.add_argument(
        "title",
        type=str,
        help="Task title"
    )
    task_create.add_argument(
        "project_id",
        type=int,
        help="Project ID"
    )
    task_create.add_argument(
        "--description", "-d",
        type=str,
        help="Task description (optional)",
        default=None
    )
    task_create.add_argument(
        "--priority", "-p",
        type=str,
        help="Task priority (low/medium/high)",
        default="medium",
        choices=["low", "medium", "high"]
    )
    task_create.add_argument(
        "--due-date",
        type=str,
        help="Due date (YYYY-MM-DD)",
        default=None,
        dest="due_date"
    )
    task_create.set_defaults(func=create_task)

    # ── task list ──
    # python main.py task list
    # python main.py task list --project-id 1
    task_list = task_subparsers.add_parser(
        "list",
        help="List all tasks"
    )
    task_list.add_argument(
        "--project-id",
        type=int,
        help="Filter by project ID (optional)",
        default=None,
        dest="project_id"
    )
    task_list.set_defaults(func=list_tasks)

    # ── task complete ──
    # python main.py task complete 1
    task_complete = task_subparsers.add_parser(
        "complete",
        help="Mark task as completed"
    )
    task_complete.add_argument(
        "id",
        type=int,
        help="Task ID"
    )
    task_complete.set_defaults(func=complete_task)

    # ── task delete ──
    # python main.py task delete 1
    task_delete = task_subparsers.add_parser(
        "delete",
        help="Delete a task"
    )
    task_delete.add_argument(
        "id",
        type=int,
        help="Task ID"
    )
    task_delete.set_defaults(func=delete_task)

    # ── task status ──
    # python main.py task status 1 in_progress
    task_status = task_subparsers.add_parser(
        "status",
        help="Update task status"
    )
    task_status.add_argument(
        "id",
        type=int,
        help="Task ID"
    )
    task_status.add_argument(
        "status",
        type=str,
        help="New status",
        choices=["todo", "in_progress", "completed", "cancelled"]
    )
    task_status.set_defaults(func=update_task_status)

    return parser