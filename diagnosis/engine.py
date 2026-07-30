from utils.models import Diagnosis

def _rule_subnet_issue(results):
    """Checks for local subnet or IP configuration mismatch issues."""
    if results["subnet"].status == "fail":
        return Diagnosis(
            summary="Subnet Configuration Issue",
            root_cause=[
                "Your device's IP address or subnet mask does not match the local network scheme, preventing proper routing.",
                "Renew DHCP lease (Win): ipconfig /renew",
                "Renew DHCP lease (Linux/Mac): sudo dhclient -r && sudo dhclient"
            ],
            affected_checks=["subnet"],
        )
    return None


def _rule_gateway_down(results):
    """Checks if the local network gateway or router is unreachable."""
    if results["gateway"].status == "fail":
        return Diagnosis(
            summary="Gateway Unreachable",
            root_cause=[
                "Unable to communicate with the local router (default gateway). Physical or Wi-Fi link appears disconnected.",
                "Check interface status (Win): ipconfig /all",
                "Check interface status (Linux/Mac): ip a or ifconfig",
                "Verify Wi-Fi connection / reconnect physical network cable."
            ],
            affected_checks=["gateway"],
        )
    return None


def _rule_isp_issue(results):
    """Checks if the router is reachable but internet connection is down (ISP issue)."""
    if results["gateway"].status == "ok" and results["network"].status == "fail":
        return Diagnosis(
            summary="Internet Service Provider (ISP) Outage",
            root_cause=[
                "Local connection to the router is healthy, but outbound internet access is failing.",
                "Trace route to external host (Win): tracert 8.8.8.8",
                "Trace route to external host (Linux/Mac): traceroute 8.8.8.8"
            ],
            affected_checks=["gateway", "network"],
        )
    return None


def _rule_bandwidth_issue(results):
    """Checks for network latency, high jitter, or packet loss issues."""
    if results["bandwidth"].status == "fail":
        return Diagnosis(
            summary="Poor Connection Quality",
            root_cause=[
                f"Connection is operational but unstable: {results['bandwidth'].message}.",
                "Inspect active connections (Win): netstat -ano",
                "Inspect active connections (Linux/Mac): ss -tulpn"
            ],
            affected_checks=["bandwidth"],
        )
    return None


def _rule_dns_issue(results):
    """Checks if general network works but domain resolution fails."""
    if results["network"].status == "ok" and results["dns"].status == "fail":
        return Diagnosis(
            summary="DNS Resolution Failure",
            root_cause=[
                "Internet IP connectivity works, but domain name resolution fails.",
                "Check active DNS configuration (Win): ipconfig /all",
                "Test against Google DNS: nslookup google.com 8.8.8.8",
                "Flush DNS cache (Win): ipconfig /flushdns"
            ],
            affected_checks=["dns"],
        )
    return None


RULES = [
    _rule_subnet_issue,
    _rule_gateway_down,
    _rule_isp_issue,
    _rule_bandwidth_issue,
    _rule_dns_issue
]


def diagnose(results):
    for rule in RULES:
        diagnosis = rule(results)
        if diagnosis:
            return diagnosis

    return Diagnosis(
        summary="No issues detected",
        root_cause=None,
        affected_checks=[],
    )