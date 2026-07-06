# ============================================
# db/database.py
# Database connection and table creation
# ============================================

# Fix import issue — tells Python where to find other modules
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# sqlite3 → built into Python, no installation needed!
# Used to connect and work with SQLite database
import sqlite3

# DB_PATH → location of database file (from settings.py)
# Example: "task_manager.db" in project root
from config.settings import DB_PATH


def get_connection():
    # ── Opens and returns database connection ──
    # Call this function every time we need to talk to database!

    # sqlite3.connect() → opens database file
    # DB_PATH           → where database file is stored
    # check_same_thread → allows multiple parts of program to use same connection
    connection = sqlite3.connect(DB_PATH, check_same_thread=False)

    # row_factory → controls how data is returned
    # Without row_factory → returns tuple → (1, "Build Website", "active") 😕
    # With row_factory    → returns dict  → {"id": 1, "name": "Build Website"} ✅
    connection.row_factory = sqlite3.Row

    # Return connection so other functions can use it!
    return connection


def create_tables():
    # ── Creates all tables if they don't exist ──

    # Step 1 — Open database (like opening a notebook)
    connection = get_connection()

    # Step 2 — Get cursor (like getting a pen to write)
    # cursor → tool to execute SQL queries
    # Without cursor → can't run any SQL!
    cursor = connection.cursor()

    # ── Create projects table ──
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            -- IF NOT EXISTS → only create if doesn't exist
            -- safe to run multiple times! ✅

            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            -- id          → unique identifier for each project
            -- INTEGER     → number type
            -- PRIMARY KEY → must be unique
            -- AUTOINCREMENT → DB sets 1, 2, 3... automatically!

            name        TEXT NOT NULL,
            -- name     → project name
            -- TEXT     → string type
            -- NOT NULL → must have value, cannot be empty!

            description TEXT,
            -- description → optional, can be empty (no NOT NULL)

            status      TEXT NOT NULL DEFAULT 'active',
            -- NOT NULL → must have value
            -- DEFAULT  → if not provided, use 'active'

            created_at  TEXT NOT NULL
            -- stores date as text → "2026-07-04"
        )
    """)

    # ── Create tasks table ──
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            -- same as projects — auto assigned by DB

            title       TEXT NOT NULL,
            -- task title — must have value

            description TEXT,
            -- optional — can be empty

            priority    TEXT NOT NULL DEFAULT 'medium',
            -- default priority is medium

            status      TEXT NOT NULL DEFAULT 'todo',
            -- default status is todo

            due_date    TEXT,
            -- optional — can be empty

            project_id  INTEGER NOT NULL,
            -- links task to a project
            -- must have value — every task needs a project!

            created_at  TEXT NOT NULL,
            -- stores date as text

            FOREIGN KEY (project_id) REFERENCES projects (id)
            -- FOREIGN KEY  → creates link between tables
            -- project_id   → column in tasks table
            -- REFERENCES   → points to
            -- projects(id) → id in projects table
            -- Means: project_id MUST match existing project id!
            -- Can't create task for non-existent project! ✅
        )
    """)

    # Step 3 — Save all changes to database
    # Like Ctrl+S for database! 💾
    # Without commit → changes are lost!
    connection.commit()

    # Step 4 — Close database connection
    # Always close after done!
    # Like closing notebook after writing!
    connection.close()

    print("Database tables created successfully! ✅")


def init_db():
    # ── Initialize database ──
    # This is what main.py calls when app starts!
    # Simple entry point that calls create_tables()
    create_tables()


# ── Main guard ──
# if __name__ == "__main__" means:
# Run directly  → python db/database.py → init_db() runs ✅
# Imported      → from db.database import get_connection → init_db() does NOT run ✅
if __name__ == "__main__":
    init_db()