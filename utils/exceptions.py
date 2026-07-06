# ============================================
# utils/exceptions.py
# Custom exceptions for Task Manager CLI
# ============================================

# Why custom exceptions?
# Instead of generic errors like:
# "Error occurred" 😕
#
# We get specific errors like:
# "Project not found!" ✅
# "Invalid priority!" ✅
# Much easier to debug!


class TaskManagerException(Exception):
    # Base exception for all our custom exceptions
    # All other exceptions inherit from this!
    pass


class ProjectNotFoundException(TaskManagerException):
    # Raised when project is not found in database
    def __init__(self, project_id: int):
        self.project_id = project_id
        super().__init__(f"Project with id {project_id} not found!")


class TaskNotFoundException(TaskManagerException):
    # Raised when task is not found in database
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with id {task_id} not found!")


class InvalidPriorityException(TaskManagerException):
    # Raised when invalid priority is provided
    def __init__(self, priority: str):
        self.priority = priority
        super().__init__(f"Invalid priority '{priority}'! Choose from low/medium/high")


class InvalidStatusException(TaskManagerException):
    # Raised when invalid status is provided
    def __init__(self, status: str):
        self.status = status
        super().__init__(f"Invalid status '{status}'!")


class EmptyFieldException(TaskManagerException):
    # Raised when required field is empty
    def __init__(self, field: str):
        self.field = field
        super().__init__(f"'{field}' cannot be empty!")