try:
    from rich.console import Console

    console = Console()

except ImportError:
    print("Error: The 'rich' library is required to run this application.")
    print("Please install it using: pip install rich")
    exit(1)
    

from checks import network, gateway, dns, subnet, bandwidth
from core.runner import run_full_diagnosis
from ui.banner import show_banner
from ui.menu import show_menu
from ui.output import show_check_result, show_check_results, show_diagnosis_result



def _run_full():
    """Runs all network checks and displays both detailed results and diagnosis."""
    results, diagnosis = run_full_diagnosis()
    show_check_results(results)
    show_diagnosis_result(diagnosis)
        
def _run_network():
    """Runs only the basic network connectivity check."""
    show_check_result(network.run())

def _run_gateway():
    """Runs only the gateway reachability check."""
    show_check_result(gateway.run())

def _run_dns():
    """Runs only the DNS resolution check."""
    show_check_result(dns.run())

def _run_subnet():
    """Runs only the subnet configuration check."""
    show_check_result(subnet.run())

def _run_bandwidth():
    """Runs only the bandwidth performance test."""
    show_check_result(bandwidth.run())

ACTIONS = {
    "1": _run_full,
    "2": _run_network,
    "3": _run_gateway,
    "4": _run_dns,
    "5": _run_subnet,
    "6": _run_bandwidth
}

show_banner()

while True:
    option = show_menu()

    if option == "0":
        console.print("[bold red]Exiting...[/bold red]")
        break

    action = ACTIONS.get(option)

    if action:
        action()
    
    else:
        print("Invalid option, try again.")
        continue

    again = console.input("\n[cyan]Do you want to run another check? (y/n):[/cyan] ").strip().lower()
    if again != "y":
        console.print("[bold red]Exiting...[/bold red]")
        break

