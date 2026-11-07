"""Boundary for crossing closure events, schedules and station interactions."""
from dataclasses import dataclass, field

@dataclass
class RailwayInteraction:
    crossings: list[dict] = field(default_factory=list)
    closure_events: list[dict] = field(default_factory=list)

    def apply_events(self):
        raise NotImplementedError('Railway timing and spillback coupling are deferred to M05.')
