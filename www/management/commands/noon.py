"""
Noon Commander Django Plugin

Run with:

    python manager.py noon PATH
"""
# this doesn't work on django or windows:
from __future__ import annotations
# use this in windows:
# from collections.abc import Iterable

from django.core.management.base import BaseCommand, CommandError

# You can import your models or utilities here
# from your_app.models import MyModel

import shutil
import subprocess
import os
# these two dont work on windows:
import pwd
import grp
import stat
from datetime import datetime
from pathlib import Path
from typing import Callable
from rich.traceback import Traceback
from textual import on
from textual.app import App, ComposeResult, Binding, SystemCommand
from textual.containers import Container, VerticalScroll, Horizontal
from textual.highlight import highlight
from textual.reactive import reactive, var
from textual.widgets import DirectoryTree, Footer, Header, Static, Label, Input, Button
from textual.screen import Screen, ModalScreen

"""

Confirm Modal 

"""
class ConfirmModal(ModalScreen[str]):
    """ A confirm modal for the delete operation. """

    file_path:str = ""
    callback: Callable[[str], None] = None

    def __init__(self, file_path: str, callback: Callable[[str], None]) -> None:
        super().__init__()
        self.file_path = file_path
        self.callback = callback

    def compose(self) -> ComposeResult:
        with Container():
            yield Label(f"Enter the path and filename to confirm: {self.file_path}")
            yield Input(type="text")
            with Horizontal():
                yield Button("Cancel", id="cancel", variant="error")
                yield Button("Ok", id="ok", variant="success")

    @on(Button.Pressed, "#ok")
    def do_it(self) -> None:
        value = self.query_one(Input).value
        if value == self.file_path:
            self.callback()
        else:
            self.notify("Path and file do not match", severity="error")
        self.app.pop_screen()

    def on_input_submitted(self) -> None:
        value = self.query_one(Input).value
        if value == self.file_path:
            self.callback()
        else:
            self.notify("Path and file do not match", severity="error")
        self.app.pop_screen()

    @on(Button.Pressed, "#cancel")
    def cancel(self) -> None:
        self.app.pop_screen()

"""

Prompt Modal

"""
class PromptModal(ModalScreen[str]):
    """ A prompt modal to input the path for the copy or move operations. """

    prompt_text: str = ""
    file_name: reactive[str | None] = reactive(None)

    def __init__(self, prompt_text: str, file_name: str) -> None:
        super().__init__()
        self.prompt_text = prompt_text
        self.file_name = str(file_name)

    def compose(self) -> ComposeResult:
        with Container():
            yield Label(self.prompt_text)
            yield Input(value=self.file_name, type="text")
            with Horizontal():
                yield Button("Cancel", id="cancel", variant="error")
                yield Button("Ok", id="ok", variant="success")

    @on(Button.Pressed, "#cancel")
    def cancel(self) -> None:
        self.app.pop_screen()
    
    @on(Button.Pressed, "#ok")
    def do_it(self) -> None:
        value = self.query_one(Input).value
        if self.file_name != "" and (value == self.file_name or value == ""):
            self.notify(f"Folder path can not be empty or equal to {self.file_name}", severity="error")
            self.app.pop_screen()
        else:
            self.dismiss(value)

    def on_input_submitted(self) -> None:
        value = self.query_one(Input).value
        if self.file_name != "" and (value == self.file_name or value == ""):
            self.notify(f"Folder path can not be empty or equal to {self.file_name}", severity="error")
            self.app.pop_screen()
        else:
            self.dismiss(value)

"""

Main App

"""
class NoonCommander(App):
    """Textual Noon Commander app."""

    # Styles
    CSS_PATH = "noon.tcss"

    # Keybindings
    BINDINGS = [
        ("f1", "show_help", "Help"),
        ("f2", "new_file", "New File"),
        ("f3", "view_file", "View File"),
        ("f4", "edit_file", "Edit File"),

        ("f5", "copy_file", "Copy File"),
        ("f6", "move_file", "Move File"),
        ("f7", "make_dir", "New Dir"),
        ("f8", "delete_file", "Delete File"),

        ("f9", "run_file", "Run File"),
        ("f10", "quit", "Quit"),

        Binding("ctrl+o", "open_terminal", "Open Terminal", show=False),
        Binding("ctrl+b", "toggle_files", "Toggle Panel", show=False),
    ]

    # Properties
    show_tree = var(True)
    path: reactive[str | None] = reactive(None)
    folder: str = "."
    editor: str = "vim"

    """
    
    Init and Event Handlers

    """

    def get_system_commands(self, screen: Screen) -> Iterable[SystemCommand]:
        yield from super().get_system_commands(screen)  
        yield SystemCommand("1. Git Pull", "Git Pull on the Current Folder", self.git_pull)
        yield SystemCommand("2. Restart Apache", "Restart the Apache Service", self.restart_apache)
    
    def __init__(self, folder: str, nano: bool) -> None:
        super().__init__()
        self.folder = "./" if folder is None else folder
        self.editor = "nano" if nano else "vim"

    def compose(self) -> ComposeResult:
        """Compose our UI."""
        yield Header()
        with Container():
            yield DirectoryTree(self.folder, id="tree-view")
            with VerticalScroll(id="code-view"):
                yield Static(id="code", expand=True)
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(DirectoryTree).focus()

        header = self.query_one(Header)
        header.icon = ""

        # Set the default theme here
        self.theme = "ansi-dark"

        # Theme change handler
        def theme_change(_signal) -> None:
            """Force the syntax to use a different theme."""
            self.watch_path(self.path)

        self.theme_changed_signal.subscribe(self, theme_change)

    def on_directory_tree_directory_selected(self, event: DirectoryTree.DirectorySelected):
        """ folder selected """
        event.stop()
        self.folder = str(event.path)

    def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        """Called when the user click a file in the directory tree."""
        event.stop()
        self.path = str(event.path)

    """ 
    
    Watchers 
    
    """

    def watch_show_tree(self, show_tree: bool) -> None:
        """Called when show_tree is modified."""
        self.set_class(show_tree, "-show-tree")

    def watch_path(self, path: str | None) -> None:
        """Called when path changes."""
        code_view = self.query_one("#code", Static)
        if path is None:
            code_view.update("")
            return
        try:
            code = Path(path).read_text(encoding="utf-8")
            syntax = highlight(code, path=path)
        except Exception:
            # code_view.update(Traceback(theme="github-dark", width=None))
            self.sub_title = "Can not read this file type"
            code_view.update("")
        else:
            code_view.update(syntax)
            self.query_one("#code-view").scroll_home(animate=False)
            self.updateSubTitle(path)

    """ 
    
    Actions 
    
    """

    # Ctrl+b Toggle Panel
    def action_toggle_files(self) -> None:
        """Called in response to key binding."""
        self.show_tree = not self.show_tree

    # Ctrl+o Open Terminal
    def action_open_terminal(self) -> None:
        """ Open terminal """
        self.run_command(["bash"])
            

    """ FILES INFO VIEW EDIT """

    # F1 File Info
    def action_show_help(self) -> None:
        self.action_show_help_panel()

    # F2 New File
    def action_new_file(self) -> None:
        """ Create a new file """
        self.push_screen(PromptModal("Enter new file name:", self.folder), self.new_file)

    # F3 View File
    def action_view_file(self) -> None:
        """ View a file """
        with self.suspend():
            if self.editor == "nano":
                subprocess.run(["nano", self.path])
            else:
                subprocess.run(["vim", self.path])

        # refresh UI
        self.reload_tree()

    # F4 Edit File
    def action_edit_file(self) -> None:
        """ Edit a file """
        with self.suspend():
            if self.editor == "nano":
                subprocess.run(["nano", self.path])
            else:
                subprocess.run(["vim", "-c", "startinsert", self.path])

        # refresh UI
        self.reload_tree()

    """ FILES COPY MOVE DELETE """

    # F5 Copy File
    def action_copy_file(self) -> None:
        self.push_screen(PromptModal("Copy file to path:", self.path), self.copy_file)

    # F6 Move File
    def action_move_file(self) -> None:
        self.push_screen(PromptModal("Move file to path:", self.path), self.move_file)

    # F7 Make Dir
    def action_make_dir(self) -> None:
        self.push_screen(PromptModal("New folder name:", self.folder), self.make_dir)

    # F8 Delete File
    def action_delete_file(self) -> None:
        self.push_screen(ConfirmModal(self.path, self.del_file))

    """ TERMINAL  """

    # F9 Open Terminal
    def action_run_file(self) -> None:
        """ Run a file """
        self.push_screen(PromptModal("Run with the arguments:", ""), self.exec_file)

    """ Command """
    
    def git_pull(self) -> None: 
        self.run_command(["git", "pull"])
        
    def restart_apache(self) -> None: 
        self.run_command(["sudo", "/opt/bitnami/ctlscript.sh",  "restart", "apache"])
        
    """ 
    
    Helpers 
    
    """

    def updateSubTitle(self, path: str) -> None:
        # Get file size
        size = self.get_readable_size(path)

        # Get the stat information of the file
        file_stat = os.stat(path)

        # Get last modified
        readable_time = datetime.fromtimestamp(file_stat.st_mtime)
        
        # Permissions
        string_perms = stat.filemode(file_stat.st_mode)

        # Extract numeric UID and GID
        uid = file_stat.st_uid
        gid = file_stat.st_gid
        # Resolve numeric IDs to actual names
        owner_name = pwd.getpwuid(uid).pw_name
        group_name = grp.getgrgid(gid).gr_name

        self.sub_title =  f"{path} {string_perms} {owner_name} {group_name} {size} {readable_time}"

    def get_readable_size(self, path):
        size_bytes = os.path.getsize(path)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024

    def reload_tree(self) -> None:
        # refresh current file
        self.watch_path(self.path)

        # refresh tree
        tree = self.query_one(DirectoryTree)
        if tree.path:
            tree.reload()

    def new_file(self, result: str) -> None:
        with self.suspend():
            if self.editor == "nano":
                subprocess.run(["nano", result], cwd=self.folder)
            else:
                subprocess.run(["vim", result, "-c", "startinsert"], cwd=self.folder)

        # refresh UI
        self.reload_tree()

    def copy_file(self, result: str) -> None:
        try: 
            shutil.copy(self.path, result)

        except PermissionError:
            self.notify("Error: Permission denied.", severity="error")

        except IsADirectoryError:
            self.notify("Error: You provided a directory path where a file path was expected.", severity="error")

        except shutil.SameFileError:
            self.notify("Error: Source and destination represent the exact same file.", severity="error")

        except Exception as e:
            self.notify(f"An unexpected error occurred: {e.strerror}", severity="error")
        
        else:
            self.notify("File copied successfully", severity="success")
            # refresh UI
            self.reload_tree()

    def move_file(self, result: str) -> None:
        try: 
            shutil.move(self.path, result)

        except PermissionError:
            self.notify("Error: Permission denied.", severity="error")

        except IsADirectoryError:
            self.notify("Error: You provided a directory path where a file path was expected.", severity="error")

        except shutil.SameFileError:
           self.notify("Error: Source and destination represent the exact same file.", severity="error")

        except Exception as e:
            self.notify(f"An unexpected error occurred: {e.strerror}", severity="error")

        else:
            self.notify("File moved successfully", severity="success")
            # refresh UI
            self.reload_tree()

    def make_dir(self, result: str) -> None:
        target_path = Path(result)
        try:
            target_path.mkdir(parents=True, exist_ok=True)

        except PermissionError:
            self.notify(f"Error: Permission denied when trying to create '{target_path}'.", severity="error")

        except FileExistsError:
            self.notify(f"Error: '{target_path}' already exists as a file, not a directory.", severity="error")
        
        except FileNotFoundError:
            self.notify(f"Error: A parent directory could not be resolved.", severity="error")

        except OSError as e:
            self.notify(f"OS Error: {e}", severity="error")

        except Exception as e:
            self.notify(f"An unexpected error occurred: {e.strerror}", severity="error")

        else:
            self.notify("Folder created successfully", severity="success")
            # refresh UI
            self.reload_tree()
    
    def del_file(self) -> None:
        try:
            Path(self.path).unlink()

        except PermissionError as e:
            self.push_screen(ErrorModal(f"Error deleting file {e.strerror}"))

        else:
            self.notify("File deleted successfully", severity="success")
            # refresh UI
            self.reload_tree()

    def exec_file(self, result: str) -> None:
        args = result.split() 
        self.run_command([self.path] + args)

    def run_command(self, command) -> None:
        with self.suspend():
            try:
            
                subprocess.run(
                    command,
                    cwd=self.folder
                )

            except OSError as e:
                print(f"OS error: {e.strerror}. --- args: {command} --- cwd: {self.folder}")

            except subprocess.CalledProcessError as e:
                print(f"Command failed with exit code: {e.returncode}. --- args: {command} --- cwd: {self.folder}")

            except subprocess.TimeoutExpired:
                print(f"Command timed out. --- args: {command} --- cwd: {self.folder}")

            input("\nPress Enter to continue...")

        # refresh UI
        self.reload_tree()

class Command(BaseCommand):
    # This description shows up when running: python manage.py help my_custom_command
    help = "A brief description of what this custom command does."

    def add_arguments(self, parser):
        # 1. Positional argument (Required by default)
        parser.add_argument("folder", type=str, help="The working folder")

        # 2. Named/Optional argument (Flag)
        parser.add_argument(
            "--nano",
            action="store_true",
            help="Use nano instead of vim as the default editor",
        )

    def handle(self, *args, **options):
        # Retrieve values from options dictionary
        # name = options["name"]
        # is_what = options["what"]

        folder = options["folder"]
        nano = options["nano"]
        NoonCommander(folder, nano).run()
