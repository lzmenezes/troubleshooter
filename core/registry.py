from checks import network, gateway, dns, subnet, bandwidth

CHECKS = {
    "network": network.run,
    "gateway": gateway.run,
    "dns": dns.run,
    "subnet": subnet.run,
    "bandwidth":bandwidth.run
}

