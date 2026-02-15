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
from reachly_engine.email.redirect import open_gmail_compose
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
        table.add_row("2.", "Generate outreach messages")
        table.add_row("3.", "View stored personas")
        table.add_row("4.", "Generate follow-up messages")
        table.add_row("5.", "Exit")

        console.print(table)
        return console.input("\nSelect option [1-5]: ").strip()

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

        pause()

    def generate_outreach(self):
        prospects = self.app.memory.list_prospects()
        if not prospects:
            render_error("No stored personas available.")
            return

        table = Table(title="Stored Personas")
        table.add_column("ID", justify="right")
        table.add_column("Name")

        for p in prospects:
            table.add_row(str(p["id"]), p.get("name") or "—")

        console.print(table)

        pid = Prompt.ask("Enter persona ID")
        if not pid.isdigit():
            render_error("Invalid ID.")
            return

        prospect = self.app.memory.get_prospect(int(pid))
        if not prospect:
            render_error("Persona not found.")
            return

        persona_block = f"""
RECIPIENT NAME:
{prospect['name']}

PERSONA DETAILS:
SUMMARY:
{prospect['summary']}

STYLE:
{prospect['style']}
""".strip()

        messages = self.app.generate_messages(
            persona_block,
            role=prospect.get("role"),
            industry=prospect.get("industry"),
        )

        render_multi_channel(messages)

        for channel, content in messages.items():
            self.app.memory.save_message(int(pid), channel, content)

        if Confirm.ask("Redirect Email to Gmail?", default=False):
            subject = self._extract_subject(messages["Email"])
            open_gmail_compose(
                subject=subject,
                body=messages["Email"],
            )

        pause()

    def generate_followups(self):
        prospects = self.app.memory.list_prospects()
        if not prospects:
            render_error("No stored personas.")
            return

        table = Table(title="Select Persona")
        table.add_column("ID")
        table.add_column("Name")

        for p in prospects:
            table.add_row(str(p["id"]), p.get("name") or "—")

        console.print(table)

        pid = Prompt.ask("Enter persona ID")
        if not pid.isdigit():
            render_error("Invalid ID")
            return

        followup_num = int(
            Prompt.ask(
                "Follow-up number (1 = gentle, 2 = value-add, 3 = final)",
                choices=["1", "2", "3"],
            )
        )

        prospect = self.app.memory.get_prospect(int(pid))

        persona_block = f"""
RECIPIENT NAME:
{prospect['name']}

PERSONA DETAILS:
SUMMARY:
{prospect['summary']}

STYLE:
{prospect['style']}
""".strip()

        followups = self.app.generate_followups(
            prospect_id=int(pid),
            persona_block=persona_block,
            followup_number=followup_num,
        )

        render_multi_channel(followups)

        for channel, content in followups.items():
            self.app.memory.save_message(
                int(pid),
                f"{channel} Follow-up {followup_num}",
                content,
            )

        if Confirm.ask("Redirect Email Follow-up to Gmail?", default=False):
            open_gmail_compose(
                subject="Follow-up regarding our previous message",
                body=followups.get("Email", ""),
            )

        pause()

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

        for p in prospects:
            table.add_row(
                str(p["id"]),
                p.get("name") or "—",
                p.get("role") or "—",
                p.get("company") or "—",
            )

        console.print(table)
        pause()

    # ---------------- Helpers ----------------

    def _extract_subject(self, email_text: str) -> str:
        for line in email_text.splitlines():
            if line.lower().startswith("subject:"):
                return line.replace("Subject:", "").strip()
        return "Regarding our connection"

