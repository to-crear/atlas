from typing import Optional, TypedDict

import yaml
from yaml.parser import ParserError

ATLAS_CONFIG_FILE = "atlas-config.yaml"


class AtlasStageInfo(TypedDict):
    """Format for stage information in config file"""

    script: str
    root: Optional[bool]
    next_stages: list[str]


class AtlasPipelineInfo(TypedDict):
    """Format for pipeline information in config file"""

    stages: dict[str, AtlasStageInfo]


class AtlasConfigInfo(TypedDict):
    """Format for config file"""

    pipeline: AtlasPipelineInfo


class ConfigValidationError(Exception):
    """Exception for error when validating config file"""


def validate_config_file(config_info: AtlasConfigInfo) -> None:
    """Validation function for atlas config file.

    Parameters
    ----------
    config_info: AtlasConfigInfo
        Config information from atlas-config.yaml
    """
    if not isinstance(config_info, dict):
        raise ConfigValidationError("Improper structure of config file")

    if "pipeline" not in config_info:
        raise ConfigValidationError("Failed to find 'pipeline' key in config file")

    if "stages" not in config_info["pipeline"]:
        raise ConfigValidationError("Failed to find 'stages' key in pipeline")

    stages = config_info["pipeline"]["stages"]
    contains_root = False
    for stage, stage_info in stages.items():
        if "script" not in stage_info.keys():
            raise ConfigValidationError(
                f"Failed to find 'script' key in '{stage}' stage"
            )

        if not contains_root and stage_info.get("root"):
            contains_root = True

    if not contains_root:
        raise ConfigValidationError("Failed to find any root stage in config file")


def load_config_file() -> AtlasConfigInfo:
    """Function for loading in atlas config file.

    Returns
    -------
    config_info: AtlasConfigInfo
        Config information from atlas-config.yaml
    """
    config_info: AtlasConfigInfo = {}

    try:
        with open(ATLAS_CONFIG_FILE, "r") as file:
            config_info = yaml.safe_load(file)
    except ParserError:
        raise ConfigValidationError(
            "Failed to parse atlas-config.yaml, please check file format"
        )

    validate_config_file(config_info)

    return config_info
