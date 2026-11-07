"""Scenario definitions are versioned and separate from baseline data."""
from dataclasses import dataclass, field

@dataclass
class ScenarioManager:
    scenarios: list[dict] = field(default_factory=list)

    def apply(self, scenario_id: str):
        raise NotImplementedError('Infrastructure alternatives require the M08 scenario engine.')
