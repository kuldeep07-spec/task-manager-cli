# ============================================
# db/repository.py
# All CRUD operations for database
# CRUD = Create, Read, Update, Delete
# Think of it like Excel operations:
# Create = add new row
# Read   = view rows
# Update = edit row
# Delete = remove row
# ============================================

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# get_connection → opens database connection
from db.database import get_connection

# Import our models — blueprint of data
from models.task import Task
from models.project import Project


# ============================================
# ProjectRepository — all database operations
# for Project
# ============================================
class ProjectRepository:

    def create(self, project: Project) -> Project:
        # ── Add new project to database ──
        # Like adding new row in Excel sheet!

        # Step 1 — Open database
        conn = get_connection()
        cursor = conn.cursor()  # cursor = pen to write SQL

        # Step 2 — Insert project into database
        # INSERT INTO → add new row to projects table
        # VALUES      → actual values to insert
        # ?           → placeholder for values (safe way!)
        #               Never use f-string in SQL — security risk!
        cursor.execute("""
            INSERT INTO projects (name, description, status, created_at)
            VALUES (?, ?, ?, ?)
        """, (project.name, project.description, project.status, project.created_at))

        # Step 3 — Get auto generated id from database
        # After INSERT → database assigns id automatically (1, 2, 3...)
        # lastrowid → gets that auto assigned id!
        project.id = cursor.lastrowid

        # Step 4 — Save changes and close
        # commit() → saves changes (like Ctrl+S) 💾
        # close()  → closes database connection
        conn.commit()
        conn.close()

        print(f"Project '{project.name}' created! ✅")
        return project  # return project with id now set!

    def get_all(self) -> list:
        # ── Get ALL projects from database ──
        # Like viewing all rows in Excel sheet!

        conn = get_connection()
        cursor = conn.cursor()

        # SELECT * → get all columns
        # FROM projects → from projects table
        cursor.execute("SELECT * FROM projects")

        # fetchall() → returns ALL rows as list
        rows = cursor.fetchall()
        conn.close()

        # Convert database rows to Project objects
        # row_factory makes rows act like dictionary
        # row["name"] → gets name column value
        projects = []
        for row in rows:
            project = Project(
                id=row["id"],
                name=row["name"],
                description=row["description"],
                status=row["status"],
                created_at=row["created_at"]
            )
            projects.append(project)  # add to list

        return projects  # return list of Project objects

    def get_by_id(self, project_id: int) -> Project:
        # ── Get ONE project by id ──
        # Like searching specific row in Excel!

        conn = get_connection()
        cursor = conn.cursor()

        # WHERE id = ? → filter by specific id
        # (project_id,) → tuple with one value
        #                  comma is important! ✅
        cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))

        # fetchone() → returns ONE row only
        row = cursor.fetchone()
        conn.close()

        # If no project found → return None
        if row is None:
            print(f"Project with id {project_id} not found!")
            return None

        # Convert row to Project object and return
        return Project(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            status=row["status"],
            created_at=row["created_at"]
        )

    def delete(self, project_id: int) -> bool:
        # ── Delete project by id ──
        # Like deleting a row in Excel!

        conn = get_connection()
        cursor = conn.cursor()

        # DELETE FROM → remove row from table
        # WHERE id = ? → only delete specific project
        cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))

        conn.commit()  # save changes!
        conn.close()

        print(f"Project deleted! ✅")
        return True  # return True = success


# ============================================
# TaskRepository — all database operations
# for Task
# ============================================
class TaskRepository:

    def create(self, task: Task) -> Task:
        # ── Add new task to database ──

        conn = get_connection()
        cursor = conn.cursor()

        # Insert task with all fields
        # project_id → links task to its project!
        cursor.execute("""
            INSERT INTO tasks (title, description, priority, status, due_date, project_id, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (task.title, task.description, task.priority,
              task.status, task.due_date, task.project_id, task.created_at))

        # Get auto generated id
        task.id = cursor.lastrowid

        conn.commit()
        conn.close()

        print(f"Task '{task.title}' created! ✅")
        return task

    def get_all(self) -> list:
        # ── Get ALL tasks from database ──

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tasks")
        rows = cursor.fetchall()
        conn.close()

        # Convert rows to Task objects
        tasks = []
        for row in rows:
            task = Task(
                id=row["id"],
                title=row["title"],
                description=row["description"],
                priority=row["priority"],
                status=row["status"],
                due_date=row["due_date"],
                project_id=row["project_id"],
                created_at=row["created_at"]
            )
            tasks.append(task)

        return tasks

    def get_by_project(self, project_id: int) -> list:
        # ── Get all tasks for specific project ──
        # Like filtering Excel by project column!

        conn = get_connection()
        cursor = conn.cursor()

        # WHERE project_id = ? → only tasks for this project
        cursor.execute("SELECT * FROM tasks WHERE project_id = ?", (project_id,))
        rows = cursor.fetchall()
        conn.close()

        # Convert rows to Task objects
        tasks = []
        for row in rows:
            task = Task(
                id=row["id"],
                title=row["title"],
                description=row["description"],
                priority=row["priority"],
                status=row["status"],
                due_date=row["due_date"],
                project_id=row["project_id"],
                created_at=row["created_at"]
            )
            tasks.append(task)

        return tasks

    def get_by_id(self, task_id: int) -> Task:
        # ── Get ONE task by id ──

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        conn.close()

        # If no task found → return None
        if row is None:
            print(f"Task with id {task_id} not found!")
            return None

        return Task(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            priority=row["priority"],
            status=row["status"],
            due_date=row["due_date"],
            project_id=row["project_id"],
            created_at=row["created_at"]
        )

    def update_status(self, task_id: int, status: str) -> bool:
        # ── Update task status ──
        # Like editing a cell in Excel!

        conn = get_connection()
        cursor = conn.cursor()

        # UPDATE → edit existing row
        # SET    → which column to change
        # WHERE  → which row to change
        cursor.execute("""
            UPDATE tasks SET status = ?
            WHERE id = ?
        """, (status, task_id))

        conn.commit()
        conn.close()

        print(f"Task status updated to '{status}'! ✅")
        return True

    def delete(self, task_id: int) -> bool:
        # ── Delete task by id ──

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()

        print(f"Task deleted! ✅")
        return True


