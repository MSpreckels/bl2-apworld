from BaseClasses import Region
from typing import Dict, List
from .Locations import BL2Location, location_table

def create_regions(world):
    regions: Dict[str, Region] = {
        "Menu": Region("Menu", world.player, world.multiworld),
        "Southern Shelf": Region("Southern Shelf", world.player, world.multiworld)
    }

    for name, data in location_table.items():
        if data.region == "Southern Shelf":
            location = BL2Location(world.player, name, data.code, regions[data.region])
            regions[data.region].locations.append(location)

    for region in regions:
        world.multiworld.regions.append(regions[region])