# ============================================
# config/settings.py
# Central configuration for Task Manager CLI
# ============================================

from pathlib import Path

# ── App Info ──────────────────────────────
APP_NAME = "Task Manager CLI"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "A CLI based task and project management tool"

# ── Database ──────────────────────────────
# Path(__file__) → current file location (settings.py)
# .parent        → goes up one folder (config/)
# .parent        → goes up again (task-manager-cli/) ← project root
# / "task_manager.db" → joins path correctly on any OS!
BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "task_manager.db"

# ── Task Settings ─────────────────────────
VALID_TASK_STATUSES = ["todo", "in_progress", "completed", "cancelled"]
VALID_PRIORITIES = ["low", "medium", "high"]

# ── Project Settings ──────────────────────
VALID_PROJECT_STATUSES = ["active", "on_hold", "completed"]

# ── Display Settings ──────────────────────
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"