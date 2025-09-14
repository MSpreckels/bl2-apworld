from BaseClasses import Region
from typing import Dict, List
from .Locations import BL2Location
from .shared.bl2_data import *

def create_regions(world):
    regions: Dict[str, Region] = {
        "Menu": Region("Menu", world.player, world.multiworld),
    }

    for region in get_region_names():
        regions[region] = Region(region, world.player, world.multiworld)

    for data in get_all_locations():
        name = f"{data['action']} {data['name']}"
        location = BL2Location(world.player, name, data["full_id"], regions[data["region"]])
        regions[data["region"]].locations.append(location)
    
    for region in regions:
        world.multiworld.regions.append(regions[region])

    regions["Menu"].connect(regions["Windshear Waste"])

    connections = get_region_connections()
    for region in connections:
        for con in connections[region]:
            regions[region].connect(regions[con])