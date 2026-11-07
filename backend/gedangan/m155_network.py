"""Inherited legal graph on byte-identical frozen baseline; richer inspection only."""
from .m15_network import model,route,chain,DIRS
from .m15_network import catalog as inherited
from .m155_common import *
from functools import lru_cache
@lru_cache(maxsize=1)
def catalog():
 import copy
 v=copy.deepcopy(inherited());v.update(version='m155-existing-provisional-1',network_path=str(NETWORK.relative_to(ROOT)),network_sha256=sha(NETWORK),geospatial_acceptance='PARTIAL',watermark='PROVISIONAL GEDANGAN NETWORK — NOT FIELD CALIBRATED');return v
