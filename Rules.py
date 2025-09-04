from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule
from math import ceil

def set_rules(bl2world):
    player = bl2world.player
    multiworld = bl2world.multiworld

    bl2world.multiworld.completion_condition[bl2world.player] = lambda state: state.has("Victory", bl2world.player)