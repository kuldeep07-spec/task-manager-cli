# ============================================
# services/project_service.py
# Business logic for Project operations
# ============================================

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.project import Project
from db.repository import ProjectRepository
from config.settings import VALID_PROJECT_STATUSES


class ProjectService:
    # ── All business logic for Project ──

    def __init__(self):
        # Create repository instance
        # Service uses repository to talk to database!
        self.repo = ProjectRepository()

    def create_project(self, name: str, description: str = None) -> Project:
        # ── Create new project ──

        # Validate name — must not be empty!
        if not name or name.strip() == "":
            print("Project name cannot be empty!")
            return None

        # Create Project object
        project = Project(
            name=name,
            description=description
        )

        # Save to database via repository
        return self.repo.create(project)

    def get_all_projects(self) -> list:
        # ── Get all projects ──
        projects = self.repo.get_all()

        if not projects:
            print("No projects found!")
            return []

        return projects

    def get_project(self, project_id: int) -> Project:
        # ── Get single project by id ──
        return self.repo.get_by_id(project_id)

    def update_status(self, project_id: int, status: str) -> bool:
        # ── Update project status ──

        # Validate status
        if status not in VALID_PROJECT_STATUSES:
            print(f"Invalid status! Choose from {VALID_PROJECT_STATUSES}")
            return False

        # Get project first
        project = self.repo.get_by_id(project_id)
        if project is None:
            return False

        # Update status
        project.status = status
        print(f"Project '{project.name}' status updated to '{status}'! ✅")
        return True

    def delete_project(self, project_id: int) -> bool:
        # ── Delete project ──

        # Check project exists first
        project = self.repo.get_by_id(project_id)
        if project is None:
            print(f"Project with id {project_id} not found!")
            return False

        return self.repo.delete(project_id)


# ============================================
# Testing — remove when project is complete
# ============================================
if __name__ == "__main__":
    from db.database import init_db
    init_db()

    service = ProjectService()

    # Create projects
    p1 = service.create_project("Build Website", "Company website")
    p2 = service.create_project("Mobile App", "iOS and Android app")
    print()

    # Get all projects
    projects = service.get_all_projects()
    print(f"Total projects: {len(projects)}")
    for p in projects:
        print(f"  → {p.name} | {p.status}")
    print()

    # Update status
    service.update_status(p1.id, "completed")
    print()

    # Delete project
    service.delete_project(p2.id)