from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text

console = Console()


def render_message_block(title: str, content: str, style: str = "cyan"):
    panel = Panel(
        Text(content, overflow="fold"),
        title=title,
        border_style=style,
        padding=(1, 2),
    )
    console.print(panel)


def render_multi_channel(messages: dict):
    """
    messages = {
        "Email": "...",
        "WhatsApp": "...",
        "LinkedIn DM": "...",
        "Instagram DM": "..."
    }
    """
    panels = []

    for channel, text in messages.items():
        panels.append(
            Panel(
                Text(text, overflow="fold"),
                title=channel,
                border_style="green",
                padding=(1, 2),
            )
        )

    console.print(Columns(panels, equal=True, expand=True))


def render_info(title: str, content: str):
    console.print(
        Panel(
            content,
            title=title,
            border_style="blue",
        )
    )


def render_error(message: str):
    console.print(
        Panel(
            message,
            title="Error",
            border_style="red",
        )
    )

