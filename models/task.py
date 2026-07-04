# ============================================
# models/task.py
# Task model for Task Manager CLI
# ============================================

# sys and os are used to fix import issue
# When running from project root, Python needs to know where to find other modules
import sys
import os

# __file__ → current file location (models/task.py)
# os.path.abspath → gets full absolute path
# os.path.dirname → goes up one folder
# doing dirname twice → goes up two folders to project root
# sys.path.append → tells Python "look here for modules too!"
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# dataclass → decorator that auto generates __init__ and __repr__
# field     → used for complex default values like lists or lambda functions
from dataclasses import dataclass, field

# Optional → value can be that type OR None
# Example: Optional[str] → can be string or None
from typing import Optional

# datetime → used to get current date and time
from datetime import datetime

# Importing constants from our settings file
# VALID_PRIORITIES    → ["low", "medium", "high"]
# VALID_TASK_STATUSES → ["todo", "in_progress", "completed", "cancelled"]
# DATE_FORMAT         → "%Y-%m-%d" (2026-07-04 format)
from config.settings import VALID_PRIORITIES, VALID_TASK_STATUSES, DATE_FORMAT


# @dataclass automatically generates:
# 1. __init__ method → no need to write manually!
# 2. __repr__ method → no need to write manually!
@dataclass
class Task:

    # ── Required Fields ───────────────────
    # Must provide these when creating a Task object
    title: str          # task title — must be string
    project_id: int     # which project this task belongs to — must be integer
                        # int because IDs are sequential numbers (1, 2, 3...)

    # ── Optional Fields ───────────────────
    # These have default values — not required when creating object
    description: Optional[str] = None  # task description — can be string or None
    priority: str = "medium"           # default priority is medium
    status: str = "todo"               # default status is todo
    due_date: Optional[str] = None     # due date — can be string or None

    # ── Auto Generated Fields ─────────────
    id: Optional[int] = None           # database will set this automatically
                                       # None when first created
                                       # integer after saved to database

    created_at: str = field(
        # default_factory → runs fresh for EACH new object
        # lambda → mini function with no name
        # datetime.now() → gets current date and time
        # .strftime(DATE_FORMAT) → formats as "2026-07-04"
        # Why lambda? → so each task gets its OWN timestamp
        #               not shared like [] would be!
        default_factory=lambda: datetime.now().strftime(DATE_FORMAT)
    )

    # ── Validation ────────────────────────
    def __post_init__(self):
        # __post_init__ runs automatically AFTER @dataclass sets all fields
        # Perfect place for validation!
        # Cannot use __init__ here — @dataclass already owns it!

        # Check if priority is valid
        # if not valid → print message and set default
        if self.priority not in VALID_PRIORITIES:
            print(f"Invalid priority! Setting to 'medium'")
            self.priority = "medium"

        # Check if status is valid
        # if not valid → print message and set default
        if self.status not in VALID_TASK_STATUSES:
            print(f"Invalid status! Setting to 'todo'")
            self.status = "todo"

    # ── Properties ────────────────────────
    # @property → used for computed/derived values
    #             calculated from other attributes
    #             accessed like attribute — no () needed!
    #             task.is_completed not task.is_completed()

    @property
    def is_completed(self) -> bool:
        # -> bool means returns True or False
        # checks if status is "completed"
        # True if completed, False otherwise
        return self.status == "completed"

    @property
    def is_high_priority(self) -> bool:
        # checks if priority is "high"
        # True if high, False otherwise
        return self.priority == "high"

    # ── Methods ───────────────────────────
    # Regular methods — they DO something (action)
    # No @property because they change data, not just check it

    def mark_complete(self) -> None:
        # -> None means returns nothing
        # changes status to completed
        self.status = "completed"
        print(f"Task '{self.title}' marked as completed! ✅")

    def mark_in_progress(self) -> None:
        # changes status to in_progress
        self.status = "in_progress"
        print(f"Task '{self.title}' is now in progress! 🔄")

    def __str__(self) -> str:
        # Called automatically when you print(task)
        # Returns clean readable string for users
        # Using () to split long string across multiple lines
        return (
            f"Task: {self.title}\n"
            f"Status: {self.status} | Priority: {self.priority}\n"
            f"Created: {self.created_at}"
        )


# ============================================
# Testing — remove this when project is complete
# ============================================

# Create a valid task — all required fields provided
task1 = Task(title="Build Login", project_id=1, priority="high")
print(task1)    # calls __str__ automatically
print()         # empty line for readability

# Create task with invalid priority
# __post_init__ will catch this and set to "medium"
task2 = Task(title="Fix Bug", project_id=1, priority="wrong")
print(task2)
print()

# Test @property — accessed like attribute, no ()
print(f"Is task1 completed? {task1.is_completed}")      # False
print(f"Is task1 high priority? {task1.is_high_priority}")  # True
print()

# Test methods — mark task as complete
task1.mark_complete()
print(f"Is task1 completed now? {task1.is_completed}")  # True