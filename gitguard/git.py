import subprocess


def run_git(*args):
    """Run a Git command and return its output."""

    result = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())

    return result.stdout.strip()


def is_git_repository():
    """Return True if the current directory is inside a Git repository."""

    try:
        run_git("rev-parse", "--is-inside-work-tree")
        return True
    except RuntimeError:
        return False


def get_changed_files():
    """Return files currently changed in the Git working tree."""

    output = run_git("status", "--porcelain")

    if not output:
        return []

    return output.splitlines()


def commit(message):
    """Stage all changes and create a Git commit."""

    run_git("add", "-A")
    return run_git("commit", "-m", message)