from rich.console import Console
from rich.prompt import Prompt, Confirm

console = Console()


def ask_linkedin_url() -> str:
    return Prompt.ask(
        "Enter LinkedIn profile URL",
        default="",
        show_default=False
    ).strip()


def ask_raw_profile_text() -> str:
    console.print("\nPaste profile text below. End input with an empty line:\n")

    lines = []
    while True:
        line = input()
        if not line.strip():
            break
        lines.append(line)

    return "\n".join(lines).strip()


def ask_confirm(message: str) -> bool:
    return Confirm.ask(message)


def pause():
    input("\nPress Enter to continue...")

