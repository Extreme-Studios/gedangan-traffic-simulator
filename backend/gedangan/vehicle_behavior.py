"""Behavior calibration is separate from nominal vehicle class labels."""
from dataclasses import dataclass, field

VEHICLE_CLASSES = ('motorcycle','car','bus','truck','trailer','oversize_special')

@dataclass
class VehicleBehavior:
    parameters_by_class: dict = field(default_factory=dict)
    calibration_status: str = 'not_started'

    def require_calibrated(self):
        raise NotImplementedError('Vehicle dimensions, lane changing and car following require M04–M06 validation.')
