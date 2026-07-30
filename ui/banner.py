from rich.console import Console
from rich.table import Table

console = Console()


def show_banner():
    try:
        import pyfiglet
        art_title = pyfiglet.figlet_format("Troubleshooter", font="slant")
        art_version = pyfiglet.figlet_format("v1.0.0", font="slant")
        
        top_grid = Table.grid(padding=2)
        top_grid.add_column()
        top_grid.add_column()
        
        top_grid.add_row(
            f"[bold bright_magenta]{art_title}[/bold bright_magenta]",
            f"[bold bright_magenta]{art_version}[/bold bright_magenta]"
        )
    except ImportError:
        """Fallback banner displayed when pyfiglet is not installed."""
        top_grid = Table.grid(padding=2)
        top_grid.add_column()
        top_grid.add_row("[bold bright_magenta]╔══════════════════════════════╗[/bold bright_magenta]")
        top_grid.add_row("[bold bright_magenta]║     TROUBLESHOOTER v1.0.0    ║[/bold bright_magenta]")
        top_grid.add_row("[bold bright_magenta]╚══════════════════════════════╝[/bold bright_magenta]")
    
    bottom_grid = Table.grid(padding=2)
    bottom_grid.add_column()
    bottom_grid.add_column()
    
    bottom_grid.add_row(
        "[bold cyan]  Developed By RootGuy[/bold cyan]",
        "[blue]| https://github.com/lzmenezes[/blue]"
    )
    
    main_grid = Table.grid(padding=0)
    main_grid.add_column()
    main_grid.add_row(top_grid)
    main_grid.add_row(bottom_grid)
    main_grid.add_row()
    
    console.print(main_grid)




