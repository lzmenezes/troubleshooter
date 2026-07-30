from rich.console import Console
from rich.table import Table
from utils.models import Diagnosis

console = Console()


def show_check_result(result):
    """Prints single check result details and optional suggestions."""
    color = "green" if result.status == "ok" else "red"

    console.print(f"\n[bold {color}][{result.status.upper()}][/bold {color}] {result.name}")
    console.print(f"  {result.message}")

    if result.suggestion:
        console.print("[bold purple]  Suggestions:[/bold purple]")
        for step in result.suggestion:
            console.print(f"    - {step}")

def show_check_results(results):
    """Displays a formatted table with all check results."""
    table = Table(
        title="Check Results",
        title_style="cyan",
        border_style="cyan"
    
    )

    table.add_column("Check", style="cyan")
    table.add_column("Status", style="white")
    table.add_column("Message", style="white")

    for result in results.values():
        status = "[bold green]OK[/bold green]" if result.status == "ok" else "[bold red]FAIL[/bold red]"

        table.add_row(
            result.name,
            status,
            result.message
        )
    console.print(table)

def show_diagnosis_result(diagnosis: Diagnosis):
    """Displays the final system diagnosis summary in a formatted table."""
    table = Table(
        title="Diagnosis",
        title_style="cyan",
        border_style="cyan",
    )

    table.add_column("Property", style="bold white")
    table.add_column("Details")

    if diagnosis.summary == "No issues detected":
        table.add_row("Status", "[bold green]No issues detected[/bold green]")
    else:
        if isinstance(diagnosis.root_cause, list):
            root_cause = "\n".join(diagnosis.root_cause) if diagnosis.root_cause else "N/A"
        else:
            root_cause = diagnosis.root_cause or "N/A"

        affected = ", ".join(diagnosis.affected_checks) if diagnosis.affected_checks else "None"

        table.add_row("Summary", f"[bold red]{diagnosis.summary}[/bold red]", style="cyan")
        table.add_row("Root Cause", root_cause, style="cyan")
        table.add_row("Affected Checks", affected, style="cyan")

    console.print(table)
