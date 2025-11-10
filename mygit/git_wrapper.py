"""
Core Git wrapper functionality
"""
import subprocess
import sys
from .colors import Colors


class GitWrapper:
    """Base class for Git operations"""

    def __init__(self):
        self.check_git_installed()

    def run_command(self, command, capture_output=False, check_error=True):
        """Execute a shell command"""
        try:
            if capture_output:
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    check=check_error
                )
                return result.stdout.strip()
            else:
                result = subprocess.run(command, shell=True, check=check_error)
                return result.returncode == 0
        except subprocess.CalledProcessError as e:
            if check_error:
                self.print_error(f"Command execution error: {e}")
            return None

    def check_git_installed(self):
        """Check if Git is installed"""
        result = self.run_command("git --version", capture_output=True, check_error=False)
        if result is None:
            self.print_error("Git is not installed! Please install Git and try again.")
            sys.exit(1)

    def is_git_repo(self):
        """Check if we're inside a Git repository"""
        result = self.run_command(
            "git rev-parse --is-inside-work-tree",
            capture_output=True,
            check_error=False
        )
        return result == "true"

    def get_current_branch(self):
        """Get current branch name"""
        return self.run_command("git branch --show-current", capture_output=True)

    def get_repo_status(self):
        """Get repository status"""
        return self.run_command("git status --short", capture_output=True)

    # Print utilities
    def print_header(self, text):
        """Print header"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

    def print_success(self, text):
        """Print success message"""
        print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

    def print_error(self, text):
        """Print error message"""
        print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

    def print_info(self, text):
        """Print info message"""
        print(f"{Colors.CYAN}ℹ {text}{Colors.ENDC}")

    def print_warning(self, text):
        """Print warning message"""
        print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")
