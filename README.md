# Task Manager CLI 🚀

A command-line based Task and Project Management Tool built with Python.
Manage your projects and tasks directly from the terminal — like a mini Jira/Linear!

## 🛠️ Tech Stack

- **Language:** Python 3.14
- **Database:** SQLite
- **Libraries:** colorama, tabulate
- **Architecture:** Clean 5-layer architecture

## 📁 Project Structure

    task-manager-cli/
    ├── main.py                   # Entry point
    ├── requirements.txt          # Dependencies
    ├── config/
    │   └── settings.py           # Central configuration
    ├── models/
    │   ├── task.py               # Task model
    │   └── project.py            # Project model
    ├── db/
    │   ├── database.py           # Database connection
    │   └── repository.py         # CRUD operations
    ├── services/
    │   ├── task_service.py       # Task business logic
    │   └── project_service.py    # Project business logic
    ├── cli/
    │   ├── commands.py           # CLI commands
    │   └── parser.py             # Argument parsing
    └── utils/
        ├── formatter.py          # Output formatting
        └── exceptions.py         # Custom exceptions

## ⚙️ Installation

    # Clone the repository
    git clone https://github.com/kuldeep07-spec/task-manager-cli.git

    # Go into project folder
    cd task-manager-cli

    # Install dependencies
    pip install -r requirements.txt

## 🚀 Usage

### Project Commands

    # Create a project
    python main.py project create "My Project" --description "Description"

    # List all projects
    python main.py project list

    # View project details
    python main.py project view 1

    # Delete a project
    python main.py project delete 1

### Task Commands

    # Create a task
    python main.py task create "Build Login" 1 --priority high

    # List all tasks
    python main.py task list

    # List tasks by project
    python main.py task list --project-id 1

    # Complete a task
    python main.py task complete 1

    # Update task status
    python main.py task status 1 in_progress

    # Delete a task
    python main.py task delete 1

## 💡 Concepts Used

- Object Oriented Programming (OOP)
- Dataclasses and Type Hints
- Abstract Classes
- Access Modifiers and @property
- Inheritance and super()
- SQLite Database
- Repository Pattern
- Service Layer Architecture
- Custom Exceptions

## 👨‍💻 Author

**Kuldeep Singh**
GitHub: https://github.com/kuldeep07-spec

## 📄 License

This project is open source and available under the MIT License.