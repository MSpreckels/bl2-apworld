from BaseClasses import Region
from typing import Dict, List
from .Locations import BL2Location, location_table

region_list = [
    "Windshear Waste",
    "Southern Shelf",
    "Southern Shelf - Bay",
    "Three Horns - Divide",
    "Three Horns - Valley",
    "Bloodshot Ramparts",
    "Bloodshot Stronghold",
    "The Bunker",
    "Frostburn Canyon",
    "Southpaw Steam & Power",
    "The Dust",
    "Tundra Express",
    "The Fridge",
    "The Highlands",
    "The Highlands - Outwash",
    "Caustic Caverns",
    "Wildlife Exploitation Preserve",
    "Lynchwood",
    "Thousand Cuts",
    "Opportunity",
    "Eridium Blight",
    "Sawtooth Cauldron",
    "Arid Nexus - Boneyard",
    "Arid Nexus - Badlands",
    "Control Core Angel",
    "End of the Line",
    "Hero's Pass",
    "The Holy Spirits",
    "Ore Chasm",
    "Sanctuary",
    "Sanctuary Hole",
    "Terramorphous Peak",
    "Vault of the Warrior",
    "Friendship Gulag",
]

region_connections = {
    "Windshear Waste": ["Southern Shelf"],
    "Southern Shelf": ["Southern Shelf - Bay", "Three Horns - Divide"],
    "Southern Shelf - Bay": ["Southern Shelf"],
    "Three Horns - Divide": ["Southern Shelf", "Frostburn Canyon", "Sanctuary", "Sanctuary Hole", "Tundra Express"],
    "Three Horns - Valley": ["Three Horns - Divide", "Southpaw Steam & Power", "The Fridge", "Bloodshot Stronghold", "The Dust"],
    "Bloodshot Ramparts": ["Bloodshot Stronghold"],
    "Bloodshot Stronghold": ["Three Horns - Valley", "Bloodshot Ramparts"],
    "The Bunker": ["Thousand Cuts", "Control Core Angel"],
    "Frostburn Canyon": ["Three Horns - Divide"],
    "Southpaw Steam & Power": ["Three Horns - Valley"],
    "The Dust": ["Three Horns - Valley", "Friendship Gulag", "Eridium Blight", "Lynchwood", "The Highlands"],
    "Tundra Express": ["Three Horns - Divide", "End of the Line"],
    "The Fridge": ["Three Horns - Valley", "The Highlands - Outwash"],
    "The Highlands": ["The Highlands - Outwash", "The Dust", "The Holy Spirits", "Opportunity", "Thousand Cuts", "Wildlife Exploitation Preserve"],
    "The Highlands - Outwash": ["The Fridge", "The Highlands"],
    "Caustic Caverns": ["Sanctuary Hole"],
    "Wildlife Exploitation Preserve": ["The Highlands"],
    "Lynchwood": ["The Dust"],
    "Thousand Cuts": ["The Highlands", "Terramorphous Peak", "The Bunker"],
    "Opportunity": ["The Highlands"],
    "Eridium Blight": ["The Dust", "Sawtooth Cauldron", "Ore Chasm", "Hero's Pass", "Arid Nexus - Boneyard"],
    "Sawtooth Cauldron": ["Eridium Blight"],
    "Arid Nexus - Boneyard": ["Eridium Blight", "Arid Nexus - Badlands"],
    "Arid Nexus - Badlands": ["Arid Nexus - Boneyard"],
    "Control Core Angel": ["The Bunker"],
    "End of the Line": ["Tundra Express"],
    "Hero's Pass": ["Eridium Blight", "Vault of the Warrior"],
    "The Holy Spirits": ["The Highlands"],
    "Ore Chasm": ["Eridium Blight"],
    "Sanctuary": ["Three Horns - Divide"],
    "Sanctuary Hole": ["Three Horns - Divide", "Caustic Caverns"],
    "Terramorphous Peak": ["Thousand Cuts"],
    "Vault of the Warrior": ["Hero's Pass"],
    "Friendship Gulag": ["The Dust"]
}

def create_regions(world):
    regions: Dict[str, Region] = {
        "Menu": Region("Menu", world.player, world.multiworld),
    }

    for region in region_connections:
        regions[region] = Region(region, world.player, world.multiworld)

    for name, data in location_table.items():
        location = BL2Location(world.player, name, data.code, regions[data.region])
        regions[data.region].locations.append(location)

    for region in regions:
        world.multiworld.regions.append(regions[region])

    regions["Menu"].connect(regions["Southern Shelf"])

    for region in region_connections:
        for con in region_connections[region]:
            regions[region].connect(regions[con])

