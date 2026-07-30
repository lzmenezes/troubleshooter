import ipaddress
import platform
import subprocess
import re

from utils.models import CheckResult


def _get_local_ip_and_mask():
    """Get local IP address and subnet mask using ipconfig/ifconfig."""
    system = platform.system().lower()

    if "windows" in system:
        result = subprocess.run(["ipconfig"], capture_output=True, text=True, encoding="cp850")
        lines = result.stdout.splitlines()
        for i, line in enumerate(lines):
            if "IPv4" in line or "IP address" in line.lower():
                ip_match = re.search(r"([\d]{1,3}\.){3}[\d]{1,3}", line)
                if ip_match:
                    ip = ip_match.group()
                    # Look for subnet mask in next lines
                    for j in range(i, min(i + 5, len(lines))):
                        mask_match = re.search(r"([\d]{1,3}\.){3}[\d]{1,3}", lines[j])
                        if mask_match and "mask" in lines[j].lower():
                            return ip, mask_match.group()
                    return ip, "255.255.255.0"  # fallback
    else:  # linux/mac
        result = subprocess.run(["ip", "addr"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if "inet " in line and "127.0.0.1" not in line:
                parts = line.strip().split()
                cidr = parts[1]
                ip = cidr.split("/")[0]
                prefix = int(cidr.split("/")[1])
                mask = str(ipaddress.IPv4Network(f"0.0.0.0/{prefix}").netmask)
                return ip, mask

    return None, None


def run():
    ip, mask = _get_local_ip_and_mask()

    if not ip:
        return CheckResult(
            name="Subnet Configuration",
            status="fail",
            message="Could not detect your IP address and subnet mask",
            suggestion=[
                "1. Check if you have a valid network connection",
                "2. Run 'ipconfig' (Windows) or 'ip addr' (Linux) manually",
                "3. Contact your network administrator"
            ],
        )

    try:
        network = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
        return CheckResult(
            name="Subnet Configuration",
            status="ok",
            message=f"IP: {ip} | Mask: {mask} | Network: {network.network_address}/{network.prefixlen}",
            suggestion=None,
        )
    except ValueError as e:
        return CheckResult(
            name="Subnet Configuration",
            status="fail",
            message=f"Invalid network configuration: {e}",
            suggestion=[
                "1. Check your network settings",
                "2. Try renewing your IP (ipconfig /renew)"
            ]
        )

