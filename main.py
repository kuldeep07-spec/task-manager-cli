# ============================================
# main.py
# Entry point for Task Manager CLI
# Run: python main.py --help
# ============================================

import sys
import os

from db.database import init_db
from cli.parser import create_parser
from utils.formatter import print_error, print_info
from colorama import Fore, Style, init

# Initialize colorama for Windows
init(autoreset=True)


def print_banner():
    # ── Print welcome banner ──
    print(f"""
{Fore.CYAN}
╔══════════════════════════════════════════╗
║         TASK MANAGER CLI  v1.0.0         ║
║     Manage your projects and tasks!      ║
╚══════════════════════════════════════════╝
{Style.RESET_ALL}""")


def main():
    # ── Main entry point ──

    # Step 1 — Print banner
    print_banner()

    # Step 2 — Initialize database
    # Creates tables if they don't exist!
    init_db()

    # Step 3 — Create argument parser
    parser = create_parser()

    # Step 4 — Parse user arguments
    args = parser.parse_args()

    # Step 5 — Execute command
    # If user typed a valid command → run it!
    # If no command typed → show help!
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()