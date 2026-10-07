def ask_for_confirmation(changed_files):
    """Ask the user whether the detected changes should be committed."""

    print("\nChanges detected:\n")

    for file in changed_files:
        print(f"  {file}")

    print()

    answer = input("Commit these changes? [y/N]: ").strip().lower()

    return answer == "y"
