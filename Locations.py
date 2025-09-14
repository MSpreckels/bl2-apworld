from BaseClasses import MultiWorld, Region, Entrance, Location
from typing import Dict, NamedTuple, Optional, Set
import typing
from .shared.bl2_data import *

class BL2Location(Location):
    game: str = "Borderlands 2"

class BL2LocationData(NamedTuple):
    region: str
    code: int
    category: str = "Boss"
