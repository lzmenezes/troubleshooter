from core.registry import CHECKS
from diagnosis.engine import diagnose


def run_full_diagnosis():
    results = {}

    for name, check_function in CHECKS.items():
        results[name] = check_function()

    diagnosis = diagnose(results)

    return results, diagnosis