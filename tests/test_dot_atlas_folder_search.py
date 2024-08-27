import pytest

from atlas.atlas_manager import AtlasManager, AtlasManagerError


def test_dot_atlas_folder_search(tmp_path):
    tmp_root_dir = tmp_path
    dot_atlas_dir = tmp_root_dir / ".atlas"
    dot_atlas_dir.mkdir()
    dot_atlas_manager = dot_atlas_dir / "manager"
    dot_atlas_manager.mkdir()
    assert isinstance(AtlasManager(str(dot_atlas_dir)).project_json_path, str)


def test_dot_atlas_folder_search_non_existent(tmp_path):
    with pytest.raises(
        AtlasManagerError, match="Error saving information to atlas_project.json."
    ):
        AtlasManager(str(tmp_path))
