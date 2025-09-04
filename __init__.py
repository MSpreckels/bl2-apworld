from worlds.AutoWorld import World
from worlds.LauncherComponents import Component, components, launch as launch_component, Type
from .Locations import location_name_to_id
from .Regions import create_regions
from .Rules import set_rules
from .Items import BL2Item, BL2ItemData, get_items_by_category, item_name_groups, item_name_to_id, create_item
from typing import List

def launch_client(*args: str):
    from .Client import launch
    launch_component(launch, name="BL2Client", args=args)

components.append(
    Component("Borderlands 2 Client", 
        func=launch_client,
        component_type=Type.CLIENT)
)

class BL2World(World):
    """
    Borderlands 2 is a first-person shooter action role-playing game with cooperative gameplay for up to four players.
    """
    
    game = "Borderlands 2"
    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id
    item_name_groups = item_name_groups
    fillers = {}
    fillers.update(get_items_by_category("Filler"))

    def generate_early(self):
        pass
    
    def create_regions(self):
        create_regions(self)
    
    def set_rules(self):
        set_rules(self)
    
    def create_items(self):
        item_pool: List[BL2Item] = []

        total_locations = len(self.multiworld.get_unfilled_locations(self.player))

        allstate = self.multiworld.get_all_state(False)
        print(self.multiworld.get_reachable_locations(allstate))

        self.get_location("Kill The Warrior").place_locked_item(create_item(self, "Victory"))

        # for i in range(18):
        #     item_pool.append(create_item(self, "Main Quest"))

        while len(item_pool) < total_locations:
            item_pool.append(create_item(self, "Skillpoint"))

        self.multiworld.itempool += item_pool
    
    def fill_slot_data(self):
        return {
            "seed": self.multiworld.seed,
            "player_name": self.player_name
        }