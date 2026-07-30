from rich.console import Console

console = Console()

def show_menu():
    """MENU OPTIONS"""
    console.print("\n[bold blue]What would you like to analyze?[/bold blue]")
    console.print("\n[cyan]1.[/cyan] [cyan]Full Diagnosis (recommended)[/cyan]")
    console.print("[cyan]2.[/cyan] [cyan]Network Connectivity[/cyan]")
    console.print("[cyan]3.[/cyan] [cyan]Gateway[/cyan]")
    console.print("[cyan]4.[/cyan] [cyan]DNS[/cyan]")
    console.print("[cyan]5.[/cyan] [cyan]Subnet Configuration[/cyan]")
    console.print("[cyan]6.[/cyan] [cyan]Bandwidth Test[/cyan]")
    console.print("[dim cyan]0.[/dim cyan] [dim cyan]Exit[/dim cyan]")
    
    choice = console.input("\n[cyan]>[/cyan] ")
    return choice

