# Troubleshooter

A CLI tool that smartly diagnoses network issues.

```
  ______                 __    __          __                __           
 /_  __/________  __  __/ /_  / /__  _____/ /_  ____  ____  / /____  _____
  / / / ___/ __ \/ / / / __ \/ / _ \/ ___/ __ \/ __ \/ __ \/ __/ _ \/ ___/
 / / / /  / /_/ / /_/ / /_/ / /  __(__  ) / / / /_/ / /_/ / /_/  __/ /    
/_/ /_/   \____/\__,_/_.___/_/\___/____/_/ /_/\____/\____/\__/\___/_/     
                                                                          

       ___  ____   ____ 
 _   _<  / / __ \ / __ \
| | / / / / / / // / / /
| |/ / /_/ /_/ // /_/ / 
|___/_/(_)____(_)____/
 
```

---

## Quick Start

```bash
git clone https://github.com/lzmenezes/troubleshooter.git
cd troubleshooter
python -m venv .venv && source .venv/bin/activate
pip install rich pyfiglet
python troubleshooter.py
```

---

## Checks

| Check | Description |
|---|---|
| Network | Pings 8.8.8.8 to verify internet connectivity |
| Gateway | Detects router IP and tests reachability |
| DNS | Resolves a domain to validate DNS is working |
| Subnet | Validates IP address and subnet mask configuration |
| Bandwidth | Measures latency, jitter, and packet loss (10 pings) |

### Diagnosis Engine

Correlates all check results to determine the root cause:

- Subnet failed -> Subnet configuration issue
- Gateway failed -> Router unreachable
- Gateway OK + Network failed -> ISP outage
- Network OK + DNS failed -> DNS resolution failure
- Bandwidth failed -> Unstable connection (high jitter or packet loss)

---

## Project Structure

```
troubleshooter/
  troubleshooter.py       Entry point and menu loop
  checks/
    network.py            External connectivity check
    gateway.py            Router reachability check
    dns.py                DNS resolution check
    subnet.py             IP/subnet validation
    bandwidth.py          Latency, jitter and packet loss test
  core/
    registry.py           Central check registry
    runner.py             Full diagnosis pipeline
  diagnosis/
    engine.py             Rule-based diagnosis engine
  ui/
    banner.py             ASCII art splash screen
    menu.py               Interactive menu
    output.py             Formatted results display
  utils/
    models.py             CheckResult and Diagnosis data models
```

---

## Adding a New Check

1. Create `checks/foo.py` with a `run()` function returning `CheckResult`
2. Register it in `core/registry.py` by adding to the `CHECKS` dict
3. Optionally add a diagnosis rule in `diagnosis/engine.py`

---

## Contributing!

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/my-check`
3. Commit your changes: `git commit -m 'feat: add my check'`
4. Push to the branch: `git push origin feat/my-check`
5. Open a Pull Request

---

## License

Copyright (c) 2025 Luiz Menezes. All rights reserved.

---

## Author

Luiz Menezes -- [github.com/lzmenezes](https://github.com/lzmenezes)
