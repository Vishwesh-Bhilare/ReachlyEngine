from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm

from reachly_engine.cli.prompts import ask_linkedin_url, pause
from reachly_engine.cli.render import (
    render_info,
    render_error,
    render_multi_channel,
)
from reachly_engine.app import ReachlyApp
from reachly_engine.logger import get_logger

logger = get_logger("cli")
console = Console()


class CLIMenu:
    def __init__(self):
        self.app = ReachlyApp()

    # ---------------- Menu ----------------

    def show_main(self) -> str:
        table = Table(title="ReachlyEngine", show_header=False, box=None)
        table.add_row("1.", "Add LinkedIn profile (analyze & store persona)")
        table.add_row("2.", "Generate outreach messages (from stored personas)")
        table.add_row("3.", "View stored personas")
        table.add_row("4.", "Exit")

        console.print(table)
        return console.input("\nSelect option [1-4]: ").strip()

    # ---------------- Actions ----------------

    def add_linkedin_profile(self):
        url = ask_linkedin_url()
        if not url:
            render_error("No URL provided.")
            return

        profile_text = self.app.ingest_linkedin(url)

        render_info(
            "Profile Ingested",
            f"Profile fetched successfully.\n\nPreview:\n{profile_text[:600]}...",
        )

        persona = self.app.analyze_persona(profile_text)

        prospect_id = self.app.save_persona_only(
            persona=persona,
            raw_profile=profile_text,
            source="linkedin",
        )

        render_info(
            "Persona Stored",
            f"Persona analyzed and saved.\n\nID: {prospect_id}\n\nSummary:\n{persona.summary}",
        )

        if Confirm.ask("Generate outreach messages now?", default=False):
            self.generate_for_prospect(prospect_id)

        pause()

    def generate_outreach(self):
        prospects = self.app.memory.list_prospects()
        if not prospects:
            render_error("No stored personas available.")
            return

        table = Table(title="Stored Personas")
        table.add_column("ID", justify="right")
        table.add_column("Name")
        table.add_column("Role")
        table.add_column("Company")

        for p in prospects:
            table.add_row(
                str(p["id"]),
                p.get("name") or "—",
                p.get("role") or "—",
                p.get("company") or "—",
            )

        console.print(table)

        choice = Prompt.ask("Enter persona ID to generate outreach")
        if not choice.isdigit():
            render_error("Invalid ID.")
            return

        self.generate_for_prospect(int(choice))
        pause()

    def generate_for_prospect(self, prospect_id: int):
        prospect = self.app.memory.get_prospect(prospect_id)
        if not prospect:
            render_error("Persona not found.")
            return

        persona_block = f"""
SUMMARY:
{prospect['summary']}

STYLE:
{prospect['style']}
""".strip()

        messages = self.app.generate_messages(persona_block)

        for channel, content in messages.items():
            self.app.memory.save_message(prospect_id, channel, content)

        render_multi_channel(messages)

    def view_personas(self):
        prospects = self.app.memory.list_prospects()
        if not prospects:
            render_info("Personas", "No stored personas.")
            return

        table = Table(title="Stored Personas")
        table.add_column("ID", justify="right")
        table.add_column("Name")
        table.add_column("Role")
        table.add_column("Company")
        table.add_column("Industry")
        table.add_column("Created")

        for p in prospects:
            table.add_row(
                str(p["id"]),
                p.get("name") or "—",
                p.get("role") or "—",
                p.get("company") or "—",
                p.get("industry") or "—",
                p["created_at"],
            )

        console.print(table)
        pause()

