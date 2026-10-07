from pathlib import Path

from .git import is_git_repository
from .watcher import start_watching


def main():
    """Start GitGuard."""

    repository = Path.cwd()

    if not is_git_repository():
        print("Error: current directory is not a Git repository.")
        return

    print("GitGuard is watching...")
    print(f"Repository: {repository}")
    print("Press Ctrl+C to stop.\n")

    start_watching(repository)