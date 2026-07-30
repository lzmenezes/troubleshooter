import platform
import re
import socket
import subprocess
from utils.models import CheckResult


def _get_gateway_ip():
    """Attempts to discover the local network's default gateway IP address."""
    system = platform.system().lower()

    # Query routing table on Windows using ipconfig
    if "windows" in system:
        result = subprocess.run(
            ["ipconfig"], capture_output=True, text=True, errors="ignore"
        )
        match = re.search(r"Gateway[^\r\n:]*:\s*([\d\.]+)", result.stdout)
        if match:
            return match.group(1)

    # Query routing table on Unix-like systems (Linux/macOS)
    else:
        result = subprocess.run(
            ["ip", "route"], capture_output=True, text=True, errors="ignore"
        )
        match = re.search(r"default via ([\d\.]+)", result.stdout)
        if match:
            return match.group(1)

    return None


def _responds_to_ping(ip):
    """Pings the target IP address to test ICMP reachability."""
    system = platform.system().lower()
    flag = "-n" if "windows" in system else "-c"

    result = subprocess.run(
        ["ping", flag, "3", ip], capture_output=True, text=True, errors="ignore"
    )
    return result.returncode == 0


def _responds_on_port_80(ip, timeout=3):
    """Attempts a socket TCP connection to port 80 (router web interface fallback)."""
    try:
        with socket.create_connection((ip, 80), timeout=timeout):
            return True
    except OSError:
        return False


def run():
    """Runs the full gateway reachability check."""
    gateway_ip = _get_gateway_ip()

    # Fail early if no default gateway interface IP could be identified
    if not gateway_ip:
        return CheckResult(
            name="Gateway",
            status="fail",
            message="Network interface disconnected or router IP unavailable",
            suggestion=[
                "1. Check if the Ethernet cable (Cat5e/Cat6) is plugged in",
                "2. Ensure Wi-Fi or Ethernet adapter is enabled",
                "3. Verify if your router is turned on",
            ],
        )

    # Test connectivity via ICMP ping or HTTP port 80
    ping_ok = _responds_to_ping(gateway_ip)
    port_ok = _responds_on_port_80(gateway_ip)

    if ping_ok or port_ok:
        return CheckResult(
            name="Gateway",
            status="ok",
            message=f"Router --> {gateway_ip} is reachable",
            suggestion=None,
        )
    else:
        return CheckResult(
            name="Gateway",
            status="fail",
            message=f"Router --> {gateway_ip} detected but unresponsive to ping/HTTP",
            suggestion=[
                "1. Check if local firewall or ICMP blocking is enabled on the router",
                "2. Try accessing the router admin page directly in a browser",
                "3. Restart the router to clear hung network processes",
            ],
        )