"""
Directory navigation commands
"""
import os
from ..colors import Colors


class NavigationCommands:
    """Directory navigation commands"""

    def navigate(self, wrapper):
        """Navigate to a directory"""
        wrapper.print_header("NAVIGATE TO DIRECTORY")

        home = os.path.expanduser("~")
        cwd = os.getcwd()

        print(f"{Colors.BOLD}Current directory:{Colors.ENDC} {cwd}\n")

        # Show quick links
        print(f"{Colors.BOLD}Quick links:{Colors.ENDC}")
        quick_links = {
            "1": ("~/personal", os.path.join(home, "personal")),
            "2": ("~/university", os.path.join(home, "university")),
            "3": ("~/ (Home)", home),
            "4": ("~/Documents", os.path.join(home, "Documents")),
        }

        for key, (name, path) in quick_links.items():
            exists = os.path.isdir(path)
            status = f"{Colors.GREEN}✓{Colors.ENDC}" if exists else f"{Colors.FAIL}✗{Colors.ENDC}"
            print(f"  {Colors.CYAN}{key}.{Colors.ENDC} {name} {status}")

        # Show subdirectories of current directory
        print(f"\n{Colors.BOLD}Subdirectories in current directory:{Colors.ENDC}")
        try:
            subdirs = [d for d in os.listdir(cwd)
                      if os.path.isdir(os.path.join(cwd, d)) and not d.startswith('.')]
            if subdirs:
                for i, subdir in enumerate(subdirs[:10], 5):  # Show max 10 subdirs
                    full_path = os.path.join(cwd, subdir)
                    is_git = os.path.isdir(os.path.join(full_path, '.git'))
                    git_mark = f"{Colors.GREEN}[git]{Colors.ENDC}" if is_git else ""
                    print(f"  {Colors.CYAN}{i}.{Colors.ENDC} {subdir}/ {git_mark}")
            else:
                print(f"  {Colors.WARNING}No subdirectories{Colors.ENDC}")
        except PermissionError:
            wrapper.print_error("Permission denied to list directory")

        print(f"\n{Colors.BOLD}Options:{Colors.ENDC}")
        print(f"  {Colors.CYAN}c.{Colors.ENDC} Enter custom path")
        print(f"  {Colors.CYAN}..{Colors.ENDC} Go to parent directory")
        print(f"  {Colors.CYAN}0.{Colors.ENDC} Cancel")

        choice = input(f"\n{Colors.CYAN}Your choice: {Colors.ENDC}").strip()

        target_path = None

        if choice == "0":
            wrapper.print_info("Cancelled")
            return
        elif choice == "..":
            target_path = os.path.dirname(cwd)
        elif choice == "c":
            print(f"\n{Colors.BOLD}Enter directory path (can use ~ for home):{Colors.ENDC}")
            custom_path = input(f"{Colors.CYAN}> {Colors.ENDC}").strip()
            if custom_path:
                target_path = os.path.expanduser(custom_path)
        elif choice in quick_links:
            target_path = quick_links[choice][1]
        elif choice.isdigit():
            idx = int(choice) - 5
            if 0 <= idx < len(subdirs[:10]):
                target_path = os.path.join(cwd, subdirs[idx])

        if target_path:
            if os.path.isdir(target_path):
                try:
                    os.chdir(target_path)
                    wrapper.print_success(f"Changed to: {os.getcwd()}")
                except Exception as e:
                    wrapper.print_error(f"Failed to change directory: {e}")
            else:
                wrapper.print_error(f"Directory does not exist: {target_path}")
        else:
            wrapper.print_error("Invalid choice!")
