import sys
from rich.console import Console
from rich.panel import Panel

from reachly_engine.cli.menu import CLIMenu
from reachly_engine.logger import get_logger

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


def run():
    console.print(
        Panel.fit(
            APP_BANNER,
            title="ReachlyEngine",
            border_style="cyan",
        )
    )

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
                sys.exit(0)

            else:
                console.print("[red]Invalid choice[/red]")

        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted. Returning to menu.[/yellow]")

