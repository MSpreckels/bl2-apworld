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
    "Kill Knuckle Dragger": BL2LocationData("Windshear Waste", 3333001, "Boss"),
    "Kill Boom": BL2LocationData("Southern Shelf", 3333002, "Boss"),
    "Kill Bewm": BL2LocationData("Southern Shelf", 3333003, "Boss"),
    "Kill The Warrior": BL2LocationData("Vault of the Warrior", 3333004, "Boss"),
    "Discover Windshear Waste": BL2LocationData("Windshear Waste", 3340001, "Location"),
    "Discover Southern Shelf": BL2LocationData("Southern Shelf", 3340002, "Location"),
    "Discover Southern Shelf - Bay": BL2LocationData("Southern Shelf - Bay", 3340003, "Location"),
    "Discover Three Horns - Divide": BL2LocationData("Three Horns - Divide", 3340004, "Location"),
    "Discover Three Horns - Valley": BL2LocationData("Three Horns - Valley", 3340005, "Location"),
    "Discover Bloodshot Ramparts": BL2LocationData("Bloodshot Ramparts", 3340006, "Location"),
    "Discover Bloodshot Stronghold": BL2LocationData("Bloodshot Stronghold", 3340007, "Location"),
    "Discover The Bunker": BL2LocationData("The Bunker", 3340008, "Location"),
    "Discover Frostburn Canyon": BL2LocationData("Frostburn Canyon", 3340009, "Location"),
    "Discover Southpaw Steam & Power": BL2LocationData("Southpaw Steam & Power", 3340010, "Location"),
    "Discover The Dust": BL2LocationData("The Dust", 3340011, "Location"),
    "Discover Tundra Express": BL2LocationData("Tundra Express", 3340012, "Location"),
    "Discover The Fridge": BL2LocationData("The Fridge", 3340013, "Location"),
    "Discover The Highlands": BL2LocationData("The Highlands", 3340014, "Location"),
    "Discover The Highlands - Outwash": BL2LocationData("The Highlands - Outwash", 3340015, "Location"),
    "Discover Caustic Caverns": BL2LocationData("Caustic Caverns", 3340016, "Location"),
    "Discover Wildlife Exploitation Preserve": BL2LocationData("Wildlife Exploitation Preserve", 3340017, "Location"),
    "Discover Lynchwood": BL2LocationData("Lynchwood", 3340018, "Location"),
    "Discover Thousand Cuts": BL2LocationData("Thousand Cuts", 3340019, "Location"),
    "Discover Opportunity": BL2LocationData("Opportunity", 3340020, "Location"),
    "Discover Eridium Blight": BL2LocationData("Eridium Blight", 3340021, "Location"),
    "Discover Sawtooth Cauldron": BL2LocationData("Sawtooth Cauldron", 3340022, "Location"),
    "Discover Arid Nexus - Boneyard": BL2LocationData("Arid Nexus - Boneyard", 3340023, "Location"),
    "Discover Arid Nexus - Badlands": BL2LocationData("Arid Nexus - Badlands", 3340024, "Location"),
    "Discover Control Core Angel": BL2LocationData("Control Core Angel", 3340025, "Location"),
    "Discover End of the Line": BL2LocationData("End of the Line", 3340026, "Location"),
    "Discover Hero's Pass": BL2LocationData("Hero's Pass", 3340027, "Location"),
    "Discover The Holy Spirits": BL2LocationData("The Holy Spirits", 3340028, "Location"),
    "Discover Ore Chasm": BL2LocationData("Ore Chasm", 3340029, "Location"),
    "Discover Sanctuary": BL2LocationData("Sanctuary", 3340030, "Location"),
    "Discover Sanctuary Hole": BL2LocationData("Sanctuary Hole", 33400031, "Location"),
    "Discover Terramorphous Peak": BL2LocationData("Terramorphous Peak", 3340032, "Location"),
    "Discover Vault of the Warrior": BL2LocationData("Vault of the Warrior", 3340033, "Location"),
    "Discover Friendship Gulag": BL2LocationData("Friendship Gulag", 3340034, "Location"),
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in location_table.items() if data.code}
lookup_name_to_id: typing.Dict[str, int] = {item_name: data.code for item_name, data in location_table.items() if data.code}

location_name_to_id = {name: data.code for name, data in location_table.items()}