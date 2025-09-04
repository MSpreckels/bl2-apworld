from typing import Dict, NamedTuple, Optional, Set

from BaseClasses import Item, ItemClassification


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

item_table: Dict[str, BL2ItemData] = { 
    "Victory": BL2ItemData("VIC", code = 333_0000, classification = ItemClassification.progression, ),
    "Main Quest": BL2ItemData("Quest", code = 333_0000, classification = ItemClassification.progression, max_quantity = 18),
    "Skillpoint": BL2ItemData("Item", code = 333_0001, classification = ItemClassification.filler, max_quantity = 35),
    # "Skillpoint Fill": BL2ItemData("Filler", code = 333_0001, classification = ItemClassification.filler, max_quantity = 100),
}

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