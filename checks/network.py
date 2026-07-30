import platform
import subprocess
from utils.models import CheckResult

# High-availability public IP used to test external internet connectivity (Google Public DNS)
TARGET_IP = "8.8.8.8"

def run():
    system = platform.system().lower()

    # Set the ping count flag based on the OS (-n for Windows, -c for Unix-like systems)
    if "windows" in system:
        command = ["ping", "-n", "3", TARGET_IP]
    else:
        command = ["ping", "-c", "3", TARGET_IP]

    # Execute the ping command, safely capturing output while ignoring encoding errors
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        errors="ignore"

    )

    # returncode == 0 indicates the target host successfully responded
    if result.returncode == 0:
        return CheckResult(
            name="Network Connectivity",
            status="ok",
            message="Internet connection responding normally",
            suggestion=None,
        )
    else:
        return CheckResult(
            name="Network Connectivity",
            status="fail",
            message=f"Could not reach {TARGET_IP} (ping failed)",
            suggestion=[
                "1. Check if the network cable is connected (or Wi-Fi is on)",
                "2. Restart your router",
                "3. If it still fails, contact your internet provider"
            ]
        )
        
