"""Automatic demo mix. Angkot uses the inherited delivery van physical envelope."""
import copy
import xml.etree.ElementTree as ET
from functools import lru_cache
from .m14_vehicles import registry as parent_registry
from .m15_network import catalog, route as parent_route
from .m04_demand import activate

MIX = {"motorcycle": 65, "car": 22, "angkot": 6, "light_truck": 4,
       "heavy_truck": 2, "trailer": 1}
LABELS = {"motorcycle": "Motor", "car": "Mobil", "angkot": "Angkot",
          "light_truck": "Truk ringan", "heavy_truck": "Truk berat", "trailer": "Trailer"}


def registry():
    vehicles = parent_registry()
    angkot = copy.deepcopy(next(v for v in vehicles if v["id"] == "pickup_van"))
    angkot.update(id="angkot", label="Angkot", source_type_id="pickup_van",
                  provenance="Assumed angkot represented with inherited delivery van dimensions and access permissions.")
    vehicles.append(angkot)
    return vehicles


@lru_cache(maxsize=512)
def route(vehicle, approach, turn):
    return parent_route("pickup_van" if vehicle == "angkot" else vehicle, approach, turn)


def types_element():
    root = ET.Element("routes", {
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xsi:noNamespaceSchemaLocation": str(activate() / "data/xsd/routes_file.xsd"),
    })
    for vehicle in registry():
        ET.SubElement(root, "vType", id=vehicle["id"],
                      **{key: str(value) for key, value in vehicle["parameters"].items()})
    return root
