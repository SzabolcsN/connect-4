import importlib.util
import os
from game.player import Player
from game.player import ExecutableBot

def load_bot(path):
    spec = importlib.util.spec_from_file_location("bot_module", path)
    bot_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bot_module)
    return bot_module

def discover_executables(directory):
    bots = []
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if os.path.isfile(path) and os.access(path, os.X_OK):
            bots.append((f"[Exec] {filename}", lambda name, pid, p=path: ExecutableBot(name, pid, p)))
    return bots

def discover_builtin_bots(directory):
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

def discover_bots(directory="bots"):
    bots = []
    bots += discover_builtin_bots(directory)
    bots += discover_executables("bots_exe")
    return bots
