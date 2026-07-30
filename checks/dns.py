import socket

from utils.models import CheckResult

TEST_HOSTNAME = "google.com"


def run():
    try:
        ip = socket.gethostbyname(TEST_HOSTNAME)
        return CheckResult(
            name="DNS Resolution",
            status="ok",
            message=f"DNS working normally: {TEST_HOSTNAME} --> {ip}",
            suggestion=None
        )
    except socket.gaierror:
        return CheckResult(
            name="DNS Resolution",
            status="fail",
            message=f"Could not resolve '{TEST_HOSTNAME}' to an IP address",
            suggestion=[
                "Change your DNS server to 8.8.8.8 in network settings",
                "Restart your browser",
                "If it still fails, restart your router"
            ],
        )