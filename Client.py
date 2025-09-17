import asyncio
import logging
import os
import json
from CommonClient import CommonContext, gui_enabled, ClientCommandProcessor, logger, get_base_parser, server_loop
from NetUtils import NetworkItem
from .shared.bl2_data import find_location_by_id

class BL2CommandProcessor(ClientCommandProcessor):
    def _cmd_bl2(self):
        """Check BL2 Connection State"""
        if isinstance(self.ctx, BL2Context):
            logger.info(f"BL2 Status: {self.ctx.get_bl2_status()}")
            logger.info(f"Game Communication Path: {self.ctx.game_communication_path}")


class BL2Context(CommonContext):
    command_processor = BL2CommandProcessor
    game = "Borderlands 2"
    items_handling = 0b111  # full remote

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.game_connected = False
        self.send_index: int = 0
        self.syncing = False
        self.item_num = 1
        
        # Set up game communication path
        # if "localappdata" in os.environ:
        #     self.game_communication_path = os.path.expandvars(r"%localappdata%/BL2Archipelago")
        # else:
        #     self.game_communication_path = os.path.expandvars(r"$HOME/BL2Archipelago")
        
        self.game_communication_path = "/home/marco/.local/share/Steam/steamapps/compatdata/49520/pfx/drive_c/users/steamuser/AppData/Local/BL2Archipelago/"

        if not os.path.exists(self.game_communication_path):
            os.makedirs(self.game_communication_path)
            
        # Clean up any existing communication files
        self.cleanup_files()

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(BL2Context, self).server_auth(password_requested)

        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            logger.info("Connected to Archipelago server!")
            self.game_connected = True

            self.seed_path = os.path.join(self.game_communication_path, str(args['slot_data'].get("seed")))
            if not os.path.exists(self.seed_path):
                os.makedirs(self.seed_path)

            config = {
                "player_name": self.auth,
                "seed": args['slot_data'].get("seed")
            }
            config_path = os.path.join(self.seed_path, "config.json")

            if not os.path.exists(config_path):
                try:
                    with open(config_path, 'w') as f:
                        f.write(json.dumps(config))
                except OSError:
                    logger.warning(f"Could not write config file: config.json")
            
            savefile_binding = {
                "seed": args['slot_data'].get("seed"),
                "save_file": ""
            }
            self.update_savefile_bindings(savefile_binding)

        elif cmd == "ReceivedItems":
            start_index = args["index"]
            if start_index != len(self.items_received):
                logger.info(f"Received {len(args['items'])} new items!")
                
                # Write item files for BL2 mod to read
                for item in args['items']:

                    data = {
                        "item_id": NetworkItem(*item).item,
                        "location_id": NetworkItem(*item).location,
                        "player": self.player_names[NetworkItem(*item).player]
                    }
                    item_filename = f"AP{data["item_id"]}"
                    
                    # Check if file already exists
                    item_path = os.path.join(self.seed_path, item_filename)
                    if not os.path.exists(item_path):
                        try:
                            with open(item_path, 'w') as f:
                                # Write item data in format: item_id\nlocation_id\nplayer_name
                                json.dump(data, f)
                            
                            logger.info(f"Wrote item file: {item_filename}")
                            self.item_num += 1
                            
                        except OSError:
                            logger.warning(f"Could not write item file: {item_filename}")
                            
        elif cmd == "RoomUpdate":
            if "checked_locations" in args:
                # Update our tracked locations
                self.checked_locations = set(args["checked_locations"])

    def get_bl2_status(self):
        return "Hello World - BL2 Client is running!"

    def cleanup_files(self):
        """Clean up communication files"""
        if not os.path.exists(self.game_communication_path):
            return
            
        for root, dirs, files in os.walk(self.game_communication_path):
            for file in files:
                if file.endswith((".item", ".cfg")) or file.startswith("send") or file == "victory":
                    try:
                        os.remove(os.path.join(root, file))
                    except OSError:
                        pass

    def update_savefile_bindings(self, savefile_binding):
        savefile_bindings_path = os.path.join(self.game_communication_path, "savefile_bindings.json")
        # if savefile bindings file does not exist create one with the current seed
        if not os.path.exists(savefile_bindings_path):
            savefile_bindings = [
                savefile_binding
            ]
            
            create_or_replace_file(savefile_bindings_path, savefile_bindings)
            return

        # if it does exist read the current config and update it
        savefile_bindings = []
        try:
            with open(savefile_bindings_path, 'r') as f:
                savefile_bindings = json.load(f)
        except OSError:
            logger.warning(f"Could not read file: {savefile_bindings_path}")
        
        binding = {}
        for b in savefile_bindings:
            if b["seed"] == savefile_binding["seed"]:
                binding = b
                break

        if not binding:
            savefile_bindings.append(savefile_binding)
            create_or_replace_file(savefile_bindings_path, savefile_bindings)
        else:
            if not binding["save_file"]:
                logger.info(f"Seed is not connected to any savefile. Please open Borderlands 2 and start a game with a character.")
            else:
                logger.info(f"Seed is connected to {binding["save_file"]}")


def create_or_replace_file(path, content):
    if os.path.exists(path):
        os.remove(path)

    try:
        with open(path, 'w') as f:
            json.dump(content, f)
        
        logger.info(f"Created file in {path}")

    except OSError:
        logger.warning(f"Could not write file: {path}")

def convert_json_to_map(filepath):
    jsonmap = {}
    try:
        with open(filepath, 'r') as f:
            jsonmap = json.load(f)
    except OSError:
        logger.warning(f"Could not read file: {filepath}")
    
    return jsonmap

async def game_watcher(ctx: BL2Context):
    """Main game watching loop - monitors for location checks from BL2 mod"""
    logger.info("BL2 Game Watcher started")
    
    while not ctx.exit_event.is_set():
        if ctx.game_connected:
            if ctx.syncing == True:
                sync_msg = [{'cmd': 'Sync'}]
                if ctx.locations_checked:
                    sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
                await ctx.send_msgs(sync_msg)
                ctx.syncing = False

            sending = []
            victory = False
            
            # Check for files in communication directory
            try:
                for root, dirs, files in os.walk(ctx.seed_path):
                    for file in files:
                        if file.startswith("check"):
                            json = convert_json_to_map(os.path.join(root, file))
                            sending.append(json["id"])
                        if file == "victory":
                            victory = True
                            logger.info(f"DEBUG found vic!")
                # Send location checks to server
                if sending:
                    # logger.info(f"DEBUG before location_checks {sending}")

                    ctx.locations_checked.update(sending)

                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": sending}])
                    # await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

                    # logger.info("DEBUG after location_checks")

                    # Clean up processed location files
                    for loc_id in sending:
                        try:
                            # logger.info(f"DEBUG try cleanup {loc_id}")

                            os.remove(os.path.join(ctx.seed_path, f"check{loc_id}.json"))
                        except OSError:
                            pass
                
                # Handle victory
                if not ctx.finished_game and victory:
                    logger.info(f"DEBUG vic!")
                    await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])  # CLIENT_GOAL
                    ctx.finished_game = True
                    try:
                        os.remove(os.path.join(self.seed_path, "victory"))
                    except OSError:
                        pass
                        
            except OSError:
                # Directory access error, continue
                pass
        
        await asyncio.sleep(0.1)  # Poll every 100ms like other Archipelago clients


async def main(args):
    parser = get_base_parser(description="Borderlands 2 Client")
    args, rest = parser.parse_known_args(args)

    ctx = BL2Context(args.connect, args.password)
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
    ctx.game_watcher_task = asyncio.create_task(game_watcher(ctx), name="game watcher")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    try:
        await ctx.exit_event.wait()
    finally:
        # Clean up files on exit
        ctx.cleanup_files()
        await ctx.shutdown()


def launch(*launch_args: str):
    import colorama
    import sys
    colorama.init()
    if launch_args:
        asyncio.run(main(launch_args))
    else:
        asyncio.run(main(sys.argv[1:]))


if __name__ == '__main__':
    launch()