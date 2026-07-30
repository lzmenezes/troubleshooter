from dataclasses import dataclass, field

@dataclass
class CheckResult:
    name: str
    status: str
    message: str
    suggestion: list[str] | None = None


@dataclass
class Diagnosis:
    summary: str
    root_cause: str | list[str] | None = None
    affected_checks: list[str] = field(default_factory=list)