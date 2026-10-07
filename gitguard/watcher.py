import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .git import commit, get_changed_files
from .prompt import ask_for_confirmation


class GitGuardHandler(FileSystemEventHandler):
    """Handle filesystem changes inside a Git repository."""

    def __init__(self, repository):
        self.repository = repository
        self.processing = False

    def on_any_event(self, event):
        if self.processing:
            return

        if event.is_directory:
            return

        # Ignore anything inside the .git directory.
        event_path = Path(event.src_path)

        if ".git" in event_path.parts:
            return

        # Give the editor/application time to finish writing.
        time.sleep(0.5)

        changed_files = get_changed_files()

        if not changed_files:
            return

        self.processing = True

        try:
            should_commit = ask_for_confirmation(changed_files)

            if should_commit:
                commit("Update project")
                print("\n✓ Changes committed.\n")
            else:
                print("\n→ Changes left uncommitted.\n")

        finally:
            self.processing = False


def start_watching(repository):
    """Start watching the repository for changes."""

    event_handler = GitGuardHandler(repository)

    observer = Observer()

    observer.schedule(
        event_handler,
        str(repository),
        recursive=True
    )

    observer.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()