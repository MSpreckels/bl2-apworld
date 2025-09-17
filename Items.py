import json
import os
from typing import Dict, NamedTuple, Optional, Set

from BaseClasses import Item, ItemClassification

from .shared.bl2_data import get_unlocks, BASE_ID

class BL2Item(Item):
    game: str = "Borderlands 2"

class BL2ItemData(NamedTuple):
    category: str
    code: int
    classification: ItemClassification = ItemClassification.filler
    max_quantity: int = 1

def get_items_by_category(category: str) -> Dict[str, BL2ItemData]:
    item_dict: Dict[str, BL2ItemData] = {}
    for name, data in item_table.items():
        if data.category == category:
            item_dict.setdefault(name, data)

    return item_dict

item_table: Dict[str, BL2ItemData] = {}

# Victory item (special case)
item_table["Victory"] = BL2ItemData("Victory", code=None, classification=ItemClassification.progression)

# Load items from unlocks section
for item_data in get_unlocks():
    # Map type to ItemClassification
    type_mapping = {
        "progression": ItemClassification.progression,
        "useful": ItemClassification.useful,
        "filler": ItemClassification.filler
    }
    
    classification = type_mapping.get(item_data["type"], ItemClassification.filler)
    code = item_data["full_id"]
    max_quantity = 1 if "count" not in item_data else item_data["count"]
    
    # Determine category based on type and name
    if item_data["type"] == "progression":
        category = "Progression"
    elif item_data["type"] == "useful":
        if item_data["name"].startswith("Fast Travel"):
            category = "FastTravel"
        else:
            category = "Useful"
    else:
        category = "Filler"
    
    item_table[item_data["name"]] = BL2ItemData(
        category=category,
        code=code,
        classification=classification,
        max_quantity=max_quantity
    )

item_name_groups: Dict[str, Set[str]] = {}
for item in item_table.keys():
    category = item_table[item].category
    if category not in item_name_groups.keys():
        item_name_groups[category] = set()
    item_name_groups[category].add(item)

item_name_to_id = {name: data.code for name, data in item_table.items()}

def create_item(world, name: str) -> BL2Item:
    data = item_table[name]
    return BL2Item(name, data.classification, data.code, world.player)