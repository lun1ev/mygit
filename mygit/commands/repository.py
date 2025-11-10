"""
Repository management commands (init, clone)
"""
import os
from ..colors import Colors


class RepositoryCommands:
    """Repository management commands"""

    def start_new_project(self, wrapper):
        """Start new project: init + add + commit"""
        wrapper.print_header("NEW PROJECT")

        if wrapper.is_git_repo():
            wrapper.print_error("This is already a Git repository!")
            return

        # Initialize
        wrapper.print_info("Initializing Git repository...")
        if not wrapper.run_command("git init"):
            return

        # Create .gitignore if it doesn't exist
        if not os.path.exists(".gitignore"):
            wrapper.print_info("Creating basic .gitignore...")
            with open(".gitignore", "w") as f:
                f.write("# Python\n")
                f.write("__pycache__/\n")
                f.write("*.py[cod]\n")
                f.write("*$py.class\n")
                f.write(".venv/\n")
                f.write("venv/\n")
                f.write("ENV/\n")
                f.write("\n# IDE\n")
                f.write(".vscode/\n")
                f.write(".idea/\n")
                f.write("\n# OS\n")
                f.write(".DS_Store\n")
                f.write("Thumbs.db\n")

        # Add all files
        wrapper.print_info("Adding files...")
        if not wrapper.run_command("git add ."):
            return

        # First commit
        wrapper.print_info("Creating initial commit...")
        if wrapper.run_command('git commit -m "Initial commit"'):
            wrapper.print_success("Project initialized!")
            wrapper.print_info("Don't forget to add remote: git remote add origin <URL>")

    def clone_repo(self, wrapper):
        """Clone repository"""
        wrapper.print_header("CLONE REPOSITORY")

        print(f"{Colors.BOLD}Enter repository URL:{Colors.ENDC}")
        url = input(f"{Colors.CYAN}> {Colors.ENDC}").strip()

        if not url:
            wrapper.print_error("URL cannot be empty!")
            return

        print()
        wrapper.print_info(f"Cloning {url}...")
        if wrapper.run_command(f"git clone {url}"):
            wrapper.print_success("Repository cloned successfully!")
