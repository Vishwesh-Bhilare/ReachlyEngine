import sys
from rich.console import Console
from rich.panel import Panel

from reachly_engine.cli.menu import CLIMenu
from reachly_engine.logger import get_logger
from reachly_engine.auth.store import load_linkedin_cookie
from reachly_engine.auth.linkedin_auth import authenticate_linkedin

console = Console()
logger = get_logger("main")

APP_BANNER = """
██████╗ ███████╗ █████╗  ██████╗██╗  ██╗██╗     ██╗   ██╗
██╔══██╗██╔════╝██╔══██╗██╔════╝██║  ██║██║     ╚██╗ ██╔╝
██████╔╝█████╗  ███████║██║     ███████║██║      ╚████╔╝
██╔══██╗██╔══╝  ██╔══██║██║     ██╔══██║██║       ╚██╔╝
██║  ██║███████╗██║  ██║╚██████╗██║  ██║███████╗   ██║
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝   ╚═╝
Offline LLM-Powered Outreach Engine
"""


def ensure_linkedin_authenticated() -> None:
    """
    Hard gate: LinkedIn authentication is required before using ReachlyEngine.
    """
    cookie = load_linkedin_cookie()
    if cookie:
        logger.info("LinkedIn authentication already present")
        return

    console.print(
        Panel.fit(
            "LinkedIn authentication is required to use ReachlyEngine.\n\n"
            "You will be redirected to LinkedIn in your browser.\n"
            "After logging in, paste your cookies into the terminal.",
            title="Authentication Required",
            border_style="yellow",
        )
    )

    authenticate_linkedin()

    if not load_linkedin_cookie():
        console.print(
            "[red]LinkedIn authentication failed. Exiting.[/red]"
        )
        sys.exit(1)

    logger.info("LinkedIn authentication completed successfully")


def run() -> None:
    console.print(
        Panel.fit(
            APP_BANNER,
            title="ReachlyEngine",
            border_style="cyan",
        )
    )

    # 🔐 Mandatory LinkedIn auth check (once per run)
    ensure_linkedin_authenticated()

    menu = CLIMenu()

    while True:
        choice = menu.show_main()

        try:
            if choice == "1":
                menu.add_linkedin_profile()

            elif choice == "2":
                menu.generate_outreach()

            elif choice == "3":
                menu.view_personas()

            elif choice == "4":
                menu.generate_followups()

            elif choice == "5":
                sys.exit(0)

            else:
                console.print("[red]Invalid choice[/red]")

        except KeyboardInterrupt:
            console.print(
                "\n[yellow]Interrupted. Returning to menu.[/yellow]"
            )

if __name__ == "__main__":
    run()