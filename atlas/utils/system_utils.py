import os
from pathlib import Path

def get_root_dir(file):
    """Get root directory path"""
    return os.path.abspath(os.curdir)#os.path.dirname(os.path.dirname(os.path.abspath(file)))