"""Network contract: no synthetic geography is loaded as Gedangan."""
from dataclasses import dataclass, field

@dataclass
class TrafficNetwork:
    nodes: list[dict] = field(default_factory=list)
    edges: list[dict] = field(default_factory=list)
    lanes: list[dict] = field(default_factory=list)
    junctions: list[dict] = field(default_factory=list)

    def require_verified(self):
        if not self.nodes or not self.edges or not self.lanes or not self.junctions:
            raise ValueError('Network incomplete; geographic verification required in later milestones.')
        if any(record.get('calibration_status') != 'verified' for records in (self.nodes,self.edges,self.lanes,self.junctions) for record in records):
            raise ValueError('Unverified network records cannot be used as a verified baseline.')
