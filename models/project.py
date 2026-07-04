# ============================================
# models/project.py
# Project model for Task Manager CLI
# ============================================

# sys and os are used to fix import issue
# When running from project root, Python needs to know where to find other modules
import sys
import os

# __file__ → current file location (models/project.py)
# os.path.abspath → gets full absolute path
# os.path.dirname → goes up one folder
# doing dirname twice → goes up two folders to project root
# sys.path.append → tells Python "look here for modules too!"
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# dataclass → decorator that auto generates __init__ and __repr__
# field     → used for complex default values like lambda functions
from dataclasses import dataclass, field

# Optional → value can be that type OR None
# List     → list of specific type (not used here but good to import)
from typing import Optional, List

# datetime → used to get current date and time
from datetime import datetime

# Importing constants from our settings file
# VALID_PROJECT_STATUSES → ["active", "on_hold", "completed"]
# DATE_FORMAT            → "%Y-%m-%d" (2026-07-04 format)
from config.settings import VALID_PROJECT_STATUSES, DATE_FORMAT


# @dataclass automatically generates:
# 1. __init__ method → no need to write manually!
# 2. __repr__ method → no need to write manually!
@dataclass
class Project:

    # ── Required Fields ───────────────────
    # Must provide when creating a Project object
    name: str               # project name — must be string

    # ── Optional Fields ───────────────────
    # These have default values — not required when creating object
    description: Optional[str] = None  # project description — can be string or None
    status: str = "active"             # default status is active

    # ── Auto Generated Fields ─────────────
    id: Optional[int] = None           # database will set this automatically
                                       # None when first created in code
                                       # integer after saved to database (1, 2, 3...)

    created_at: str = field(
        # default_factory → runs fresh for EACH new object
        # lambda → mini function with no name
        # datetime.now() → gets current date and time
        # .strftime(DATE_FORMAT) → formats as "2026-07-04"
        # Why lambda? → so each project gets its OWN timestamp!
        default_factory=lambda: datetime.now().strftime(DATE_FORMAT)
    )

    # ── Validation ────────────────────────
    def __post_init__(self):
        # runs automatically AFTER @dataclass sets all fields
        # perfect place for validation and formatting!

        # Check if status is valid
        # if not valid → print message and set default to "active"
        if self.status not in VALID_PROJECT_STATUSES:
            print(f"Invalid status! Setting to 'active'")
            self.status = "active"

        # Auto format name
        # strip()      → removes extra spaces from start and end
        # capitalize() → makes first letter uppercase
        # Example: "  build website  " → "Build website"
        self.name = self.name.strip().capitalize()

    # ── Properties ────────────────────────
    # @property → used for computed/derived values
    #             checking a STATE not doing an ACTION
    #             accessed like attribute — no () needed!
    #             project.is_active not project.is_active()

    @property
    def is_active(self) -> bool:
        # -> bool means returns True or False
        # checks if status is "active"
        # True if active, False otherwise
        return self.status == "active"

    @property
    def is_completed(self) -> bool:
        # checks if status is "completed"
        # True if completed, False otherwise
        return self.status == "completed"

    # ── Methods ───────────────────────────
    # Regular methods — they DO something (action)
    # No @property because they CHANGE data not just check it

    def mark_completed(self) -> None:
        # -> None means returns nothing
        # changes status to completed
        self.status = "completed"
        print(f"Project '{self.name}' marked as completed! ✅")

    def put_on_hold(self) -> None:
        # changes status to on_hold
        self.status = "on_hold"
        print(f"Project '{self.name}' put on hold! ⏸️")

    def activate(self) -> None:
        # changes status back to active
        self.status = "active"
        print(f"Project '{self.name}' activated! 🚀")

    def __str__(self) -> str:
        # Called automatically when you print(project)
        # Returns clean readable string for users
        # Using () to split long string across multiple lines
        return (
            f"Project: {self.name}\n"
            f"Status: {self.status}\n"
            f"Created: {self.created_at}"
        )
    
