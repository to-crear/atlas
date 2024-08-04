import pytest

from atlas.atlas_manager import AtlasManager, AtlasManagerError


def test_dot_atlas_folder_search():
    try:
        AtlasManager()
    except Exception as e:
        raise AtlasManagerError(f"Test:Error: {e}")
