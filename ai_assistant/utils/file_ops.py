import os
import shutil
from datetime import datetime

def backup_files(src, dest):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copytree(src, f"{dest}/backup_{timestamp}")