from dataclasses import dataclass


@dataclass
class HealthStatus:
    name: str
    healthy: bool
    message: str