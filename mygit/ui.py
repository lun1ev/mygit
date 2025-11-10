"""
User interface and menu system
"""
import os
import sys
from .colors import Colors
from .git_wrapper import GitWrapper
from .commands import SyncCommands, RepositoryCommands, StatusCommands, NavigationCommands


class UI:
    """Main UI class"""

    def __init__(self):
        self.wrapper = GitWrapper()
        self.sync_cmd = SyncCommands()
        self.repo_cmd = RepositoryCommands()
        self.status_cmd = StatusCommands()
        self.nav_cmd = NavigationCommands()

    def show_menu(self):
        """Show main menu"""
        self.wrapper.print_header("MyGit - Git Wrapper")

        # Show current directory and status
        cwd = os.getcwd()
        print(f"{Colors.BOLD}Current directory:{Colors.ENDC} {cwd}")

        if self.wrapper.is_git_repo():
            branch = self.wrapper.get_current_branch()
            print(f"{Colors.BOLD}Git repository:{Colors.ENDC} {Colors.GREEN}✓{Colors.ENDC} (branch: {branch})")
        else:
            print(f"{Colors.BOLD}Git repository:{Colors.ENDC} {Colors.FAIL}✗{Colors.ENDC}")

        print(f"\n{Colors.BOLD}Choose action:{Colors.ENDC}")
        print(f"  {Colors.CYAN}1.{Colors.ENDC} 🚀 Full sync (add + commit + push)")
        print(f"  {Colors.CYAN}2.{Colors.ENDC} 💾 Just commit (add + commit)")
        print(f"  {Colors.CYAN}3.{Colors.ENDC} 🆕 Start new project (init + commit)")
        print(f"  {Colors.CYAN}4.{Colors.ENDC} 📥 Clone repository")
        print(f"  {Colors.CYAN}5.{Colors.ENDC} 🔄 Pull changes")
        print(f"  {Colors.CYAN}6.{Colors.ENDC} ↩️  Reset changes")
        print(f"  {Colors.CYAN}7.{Colors.ENDC} 📊 Show status")
        print(f"  {Colors.CYAN}8.{Colors.ENDC} 📁 Navigate to directory")
        print(f"  {Colors.CYAN}0.{Colors.ENDC} 🚪 Exit")

    def run(self):
        """Run interactive menu"""
        actions = {
            "1": lambda: self.sync_cmd.full_sync(self.wrapper),
            "2": lambda: self.sync_cmd.just_commit(self.wrapper),
            "3": lambda: self.repo_cmd.start_new_project(self.wrapper),
            "4": lambda: self.repo_cmd.clone_repo(self.wrapper),
            "5": lambda: self.sync_cmd.pull_changes(self.wrapper),
            "6": lambda: self.sync_cmd.reset_changes(self.wrapper),
            "7": lambda: self.status_cmd.show_status(self.wrapper),
            "8": lambda: self.nav_cmd.navigate(self.wrapper),
        }

        while True:
            self.show_menu()
            choice = input(f"\n{Colors.CYAN}Your choice: {Colors.ENDC}").strip()

            if choice == "0":
                self.wrapper.print_success("Goodbye!")
                break
            elif choice in actions:
                print()
                actions[choice]()
                input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")
            else:
                self.wrapper.print_error("Invalid choice! Try again.")
                input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")


def main():
    """Main entry point"""
    try:
        ui = UI()
        ui.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Interrupted by user{Colors.ENDC}")
        sys.exit(0)
