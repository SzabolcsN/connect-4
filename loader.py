import importlib.util
import os
from game.player import Player

def load_bot(path):
    spec = importlib.util.spec_from_file_location("bot_module", path)
    bot_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bot_module)
    return bot_module

def discover_bots(directory):
    bots = []
    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            path = os.path.join(directory, filename)
            module = load_bot(path)
            for name in dir(module):
                if name == "Player":
                    continue  # Skip base class named Player
                obj = getattr(module, name)
                is_builtin = getattr(obj, "builtin", False)
                if (
                    isinstance(obj, type)
                    and issubclass(obj, Player)
                    and obj is not Player
                    and hasattr(obj, 'get_move')
                    and callable(getattr(obj, 'get_move'))
                ):
                    display_name = f"[Builtin] {name}" if is_builtin else name
                    bots.append((display_name, obj))
    return bots
