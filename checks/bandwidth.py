import subprocess
import platform
import statistics

from utils.models import CheckResult

TARGET_IP = "8.8.8.8"
PING_COUNT = 10
JITTER_THRESHOLD_MS = 30


def run():
    param = "-n" if platform.system().lower() == "windows" else "-c"
    cmd = ["ping", param, str(PING_COUNT), TARGET_IP]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        lines = result.stdout.splitlines()
        latencies = []

        for line in lines:
            if "time=" in line or "tempo=" in line:
                parts = line.replace("ms", "").split()
                for p in parts:
                    if p.startswith("time=") or p.startswith("tempo="):
                        val = p.split("=")[1]
                        latencies.append(float(val))

    except Exception as e:
        return CheckResult(
            name="Bandwidth Quality",
            status="fail",
            message=f"Error running ping test: {e}",
            suggestion=["Check your network connection and try again"],
        )

    if not latencies:
        return CheckResult(
            name="Bandwidth Quality",
            status="fail",
            message="Could not measure latency. Target might be blocking ICMP packets",
            suggestion=["Try a different target host", "Check firewall settings"],
        )

    avg_latency = statistics.mean(latencies)
    jitter = statistics.stdev(latencies) if len(latencies) > 1 else 0.0
    packets_lost = PING_COUNT - len(latencies)

    summary = (
        f"Avg latency: {avg_latency:.2f}ms | "
        f"Jitter: {jitter:.2f}ms | "
        f"Packets: {len(latencies)}/{PING_COUNT}"
    )

    if jitter > JITTER_THRESHOLD_MS or packets_lost > 0:
        return CheckResult(
            name="Bandwidth Quality",
            status="fail",
            message=summary,
            suggestion=[
                "Check for network congestion or interference",
                "Reduce the number of active devices on your network",
                "If using Wi-Fi, try moving closer to the router or using a wired connection",
            ],
        )

    return CheckResult(
        name="Bandwidth Quality",
        status="ok",
        message=summary,
        suggestion=None,
    )
