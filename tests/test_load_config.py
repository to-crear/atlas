import pytest

from atlas.load_config import ConfigValidationError, validate_config_file


def test_validate_config_file():
    config_info = {
        "pipeline": {
            "stages": {
                "stage1": {
                    "script": "stage1.py",
                    "next_stages": ["stage2"],
                    "root": True,
                },
                "stage2": {"script": "stage2.py"},
            }
        }
    }

    assert validate_config_file(config_info) == None


def test_validate_config_file_no_pipeline_key():
    config_info = {
        "stages": {
            "stage1": {"script": "stage1.py", "next_stages": ["stage2"], "root": True}
        }
    }

    with pytest.raises(
        ConfigValidationError, match="Failed to find 'pipeline' key in config file"
    ):
        validate_config_file(config_info)


def test_validate_config_file_no_stages_key():
    config_info = {
        "pipeline": {
            "stage1": {"script": "stage1.py", "next_stages": ["stage2"], "root": True}
        }
    }

    with pytest.raises(
        ConfigValidationError, match="Failed to find 'stages' key in pipeline"
    ):
        validate_config_file(config_info)


def test_validate_config_file_no_script_key():
    config_info = {
        "pipeline": {"stages": {"stage1": {"next_stages": ["stage2"], "root": True}}}
    }

    with pytest.raises(
        ConfigValidationError, match="Failed to find 'script' key in 'stage1' stage"
    ):
        validate_config_file(config_info)


def test_validate_config_file_no_root():
    config_info = {
        "pipeline": {
            "stages": {
                "stage1": {
                    "script": "stage1.py",
                    "next_stages": ["stage2"],
                },
                "stage2": {"script": "stage2.py"},
            }
        }
    }

    with pytest.raises(
        ConfigValidationError, match="Failed to find any root stage in config file"
    ):
        validate_config_file(config_info)
