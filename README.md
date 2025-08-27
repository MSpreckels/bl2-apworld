# Borderlands 2 Archipelago Implementation

## File-Based Communication Protocol

The BL2 Archipelago client uses file-based communication to interface with the Borderlands 2 game mod, following established Archipelago patterns.

### Communication Directory
- **Windows**: `%LOCALAPPDATA%/BL2Archipelago/`
- **Linux**: `$HOME/BL2Archipelago/`
- Directory is automatically created by the client on startup
- Files are cleaned up on client startup and shutdown

### File Types

#### Location Checks (Mod → Client)
Files created by the BL2 mod to signal that a location has been checked:
- **Format**: `send{location_id}` (empty files)
- **Example**: `send12345` indicates location ID 12345 was checked
- **Processing**: Client detects file, sends location check to server, deletes file

#### Items Received (Client → Mod)
Files created by the client when items are received from the server:
- **Format**: `AP_{item_number}.item`
- **Content**: Three lines containing:
  ```
  {item_id}
  {location_id}
  {player_name}
  ```
- **Example**: `AP_1.item` containing:
  ```
  67890
  12345
  Alice
  ```

#### Configuration Files (Client → Mod)
Slot data from the server written as configuration files:
- **Format**: `{key}.cfg`
- **Content**: Single value from slot data
- **Examples**: `goal.cfg`, `difficulty.cfg`, `starting_weapons.cfg`

#### Victory Condition (Mod → Client)
- **Format**: `victory` (empty file)
- **Purpose**: Signals that the player has completed their goal
- **Processing**: Client sends goal completion to server, deletes file

### Polling Behavior
- Client polls the directory every 100ms
- Files are processed immediately when detected
- Processed files are automatically deleted

## Potential Game Content

### Location Checks (Things to Track)

#### Story Progress
- Main quest completions (Handsome Jack's storyline)
- Side quest completions (hundreds available)
- Area discoveries (new map regions)
- Fast travel station activations

#### Combat/Bosses
- Named boss kills (Terramorphous, Vermivorous, etc.)
- Raid boss completions
- Badass rank challenges completed
- Vault Hunter relic pieces found

#### Exploration
- Vault symbols found (hidden collectibles)
- Audio logs discovered
- Red chests opened
- Legendary weapon drops from specific sources

#### Character Progression
- Skill points earned (level milestones)
- Class mod acquisitions
- Eridium milestones reached

### Items to Unlock (Rewards from Other Players)

#### Weapons
- Legendary weapons (specific guns with unique effects)
- Weapon parts/accessories
- Weapon proficiency bonuses
- Ammo capacity upgrades

#### Equipment
- Shields (different rarities/effects)
- Grenade mods
- Class mods (character-specific equipment)
- Relics (passive bonus items)

#### Character Abilities
- Skill points for talent trees
- Action skill cooldown reductions
- Individual skill unlocks (instead of points)

#### Resources
- Eridium (premium currency)
- Money/cash
- Inventory slots
- Bank storage slots

#### Progression Gates
- Area access (unlock new regions)
- Vehicle parts/upgrades
- Weapon slot unlocks
- Backpack space increases

### Archipelago-Specific Mechanics

#### Progressive Items
- Progressive weapon slots (2→3→4 weapons equipped)
- Progressive inventory size
- Progressive skill tree access

#### Trap Items
- Spawn enemies near player
- Reduce weapon accuracy temporarily
- Drain shield/health
- Scramble controls briefly

#### Quality of Life
- Fast travel unlocks to specific stations
- Vehicle spawn permissions
- Vendor discounts
- Respawn cost reductions

## Implementation Notes

### For BL2 Mod Development

#### To Signal a Location Check
```bash
# Create empty file with location ID as filename
touch $HOME/BL2Archipelago/send12345
```

#### To Read Received Items
```bash
# Check for AP_*.item files and parse their contents
# Format: item_id\nlocation_id\nplayer_name
```

#### To Signal Victory
```bash
# Create victory file when goal is completed
touch $HOME/BL2Archipelago/victory
```

### Client Features
- 100ms polling interval (matches other Archipelago clients)
- Automatic file cleanup on startup/shutdown
- Robust error handling for file operations
- Logging of all communication events
- Status command (`/bl2`) for debugging

### Future Enhancements
- Death link support via `dlsend`/`dlreceive` files
- Hint system integration
- Multiplayer position sharing
- Save state synchronization

This implementation creates a completely different Borderlands 2 experience where character progression depends on helping other players in their respective game worlds, following the core Archipelago philosophy of interconnected randomized gameplay.