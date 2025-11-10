"""
Status and information commands
"""
from ..colors import Colors


class StatusCommands:
    """Status and information commands"""

    def show_status(self, wrapper):
        """Show repository status"""
        if not wrapper.is_git_repo():
            wrapper.print_error("This is not a Git repository!")
            return

        branch = wrapper.get_current_branch()
        status = wrapper.get_repo_status()

        wrapper.print_info(f"Current branch: {Colors.BOLD}{branch}{Colors.ENDC}")

        if status:
            print(f"\n{Colors.WARNING}Changes:{Colors.ENDC}")
            print(status)
        else:
            wrapper.print_success("No changes (working tree clean)")
