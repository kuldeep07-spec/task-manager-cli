# ============================================
# services/task_service.py
# Business logic for Task operations
# ============================================

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.task import Task
from db.repository import TaskRepository, ProjectRepository
from config.settings import VALID_PRIORITIES, VALID_TASK_STATUSES


class TaskService:
    # ── All business logic for Task ──

    def __init__(self):
        # Create repository instances
        self.task_repo = TaskRepository()
        self.project_repo = ProjectRepository()

    def create_task(self, title: str, project_id: int,
                    description: str = None,
                    priority: str = "medium",
                    due_date: str = None) -> Task:
        # ── Create new task ──

        # Validate title — must not be empty!
        if not title or title.strip() == "":
            print("Task title cannot be empty!")
            return None

        # Validate project exists!
        # Can't create task for non-existent project!
        project = self.project_repo.get_by_id(project_id)
        if project is None:
            print(f"Project with id {project_id} not found!")
            return None

        # Validate priority
        if priority not in VALID_PRIORITIES:
            print(f"Invalid priority! Setting to 'medium'")
            priority = "medium"

        # Create Task object
        task = Task(
            title=title,
            project_id=project_id,
            description=description,
            priority=priority,
            due_date=due_date
        )

        # Save to database via repository
        return self.task_repo.create(task)

    def get_all_tasks(self) -> list:
        # ── Get all tasks ──
        tasks = self.task_repo.get_all()

        if not tasks:
            print("No tasks found!")
            return []

        return tasks

    def get_tasks_by_project(self, project_id: int) -> list:
        # ── Get all tasks for specific project ──
        tasks = self.task_repo.get_by_project(project_id)

        if not tasks:
            print(f"No tasks found for project {project_id}!")
            return []

        return tasks

    def get_task(self, task_id: int) -> Task:
        # ── Get single task by id ──
        return self.task_repo.get_by_id(task_id)

    def update_status(self, task_id: int, status: str) -> bool:
        # ── Update task status ──

        # Validate status
        if status not in VALID_TASK_STATUSES:
            print(f"Invalid status! Choose from {VALID_TASK_STATUSES}")
            return False

        # Check task exists
        task = self.task_repo.get_by_id(task_id)
        if task is None:
            return False

        return self.task_repo.update_status(task_id, status)

    def complete_task(self, task_id: int) -> bool:
        # ── Mark task as completed ──
        return self.update_status(task_id, "completed")

    def delete_task(self, task_id: int) -> bool:
        # ── Delete task ──

        # Check task exists first
        task = self.task_repo.get_by_id(task_id)
        if task is None:
            print(f"Task with id {task_id} not found!")
            return False

        return self.task_repo.delete(task_id)


# ============================================
# Testing — remove when project is complete
# ============================================
if __name__ == "__main__":
    from db.database import init_db
    init_db()

    from services.project_service import ProjectService
    project_service = ProjectService()
    task_service = TaskService()

    # Create project first
    project = project_service.create_project("Build Website", "Company website")
    print()

    # Create tasks
    t1 = task_service.create_task("Build Login", project.id, priority="high")
    t2 = task_service.create_task("Build Dashboard", project.id, priority="medium")
    t3 = task_service.create_task("Write Tests", project.id, priority="low")
    print()

    # Get all tasks
    tasks = task_service.get_all_tasks()
    print(f"Total tasks: {len(tasks)}")
    for t in tasks:
        print(f"  → {t.title} | {t.status} | {t.priority}")
    print()

    # Complete a task
    task_service.complete_task(t1.id)
    print()

    # Delete a task
    task_service.delete_task(t3.id)
    print()

    # Get tasks by project
    tasks = task_service.get_tasks_by_project(project.id)
    print(f"Remaining tasks: {len(tasks)}")
    for t in tasks:
        print(f"  → {t.title} | {t.status}")