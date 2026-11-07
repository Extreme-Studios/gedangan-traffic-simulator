"""Demand/projection contract. Missing rates never mean zero growth."""
from dataclasses import dataclass, field

@dataclass
class VehicleDemand:
    baseline_year: int = 2026
    od_matrix: list[dict] = field(default_factory=list)
    growth_rates: list[dict] = field(default_factory=list)

    def rate_for(self, year: int, vehicle_class: str, zone: str) -> float:
        matches = [r for r in self.growth_rates if (r['year'],r['vehicle_class_id'],r['zone_id']) == (year,vehicle_class,zone)]
        if len(matches) != 1 or matches[0].get('annual_rate') is None or not matches[0].get('provenance_id'):
            raise ValueError('Exactly one documented growth rate is required for year/class/zone.')
        rate = matches[0]['annual_rate']
        if not isinstance(rate, (int,float)) or isinstance(rate,bool) or not -1 <= rate:
            raise ValueError('Growth rate must be a finite fractional rate >= -1.')
        import math
        if not math.isfinite(rate):
            raise ValueError('Growth rate must be finite.')
        return rate
