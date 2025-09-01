from BaseClasses import MultiWorld, Region, Entrance, Location
from typing import Dict, NamedTuple, Optional, Set
import typing

class BL2Location(Location):
    game: str = "Borderlands 2"

class BL2LocationData(NamedTuple):
    region: str
    code: int
    category: str = "Boss"

location_table: Dict[str, BL2LocationData] = {
    "Kill Knuckle Dragger": BL2LocationData("Southern Shelf", 3333001, "Boss"),
    "Kill Boom": BL2LocationData("Southern Shelf", 3333002, "Boss"),
    "Kill Bewm": BL2LocationData("Southern Shelf", 3333003, "Boss"),
}

location_name_to_id = {name: data.code for name, data in location_table.items()}