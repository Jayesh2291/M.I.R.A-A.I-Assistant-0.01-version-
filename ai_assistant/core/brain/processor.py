import os
import shutil
from utils.logger import logger

def process_command(command, memory):
    # File Operations
    if "create folder" in command:
        path = command.split("create folder")[1].strip()
        os.makedirs(path, exist_ok=True)
        return f"Created folder: {path}"

    elif "delete folder" in command:
        path = command.split("delete folder")[1].strip()
        shutil.rmtree(path)
        return f"Deleted folder: {path}"

    # Memory Recall
    elif "remember" in command:
        return str(memory.data["conversations"][-3:])  # Last 3 interactions

    else:
        return "Command processed."