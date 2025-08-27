from worlds.AutoWorld import World
from worlds.LauncherComponents import Component, components, launch as launch_component, Type

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
    item_name_to_id = {}
    location_name_to_id = {}
    
    def create_regions(self):
        pass
    
    def create_items(self):
        pass
    
    def set_rules(self):
        pass
    
    def create_item(self, name: str):
        pass
    
    def fill_slot_data(self):
        return {}