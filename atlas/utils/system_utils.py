import os


def get_root_dir() -> str:
    """Get root directory path"""
    return os.path.abspath(os.curdir)
