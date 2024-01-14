import cloudpickle
import json
import os

from distutils.version import StrictVersion
from typing import Any, Dict, Literal, Optional

from atlas.utils.system_utils import get_root_dir
from config.atlas_config import ATLAS_HIDDEN_DIRECTORY


# TODO: Instead to getting root directory, get directory where .atlas is defined
# Issue related to https://tocreate.atlassian.net/browse/ATLAS-11
root_dir = get_root_dir()
atlas_folder_path = os.path.join(root_dir, ATLAS_HIDDEN_DIRECTORY)
model_repository_path = os.path.join(atlas_folder_path, "model_repository")

VERSION = Literal["major", "minor", "patch"]


class AtlasModelError(Exception):
    """Error when calling atlas model functions"""
    pass


def generate_new_version(last_version: str, update_type: VERSION) -> str:
    """Generates a new version tag based on the previous version and type of update.
    
    Parameters
    ----------
    last_version: str
        Previous version
    
    update_type: VERSION
        Type of update for new version (major, minor or patch)

    Returns
    -------
    new_version: str
        New version    
    """
    major, minor, patch = last_version.split(".")
    if update_type == "major":
        return f"{int(major)+1}.0.0"
    elif update_type == "minor":
        return f"{major}.{int(minor)+1}.0"
    else:
        return f"{major}.{minor}.{int(patch)+1}"


def save_model(model: Any, model_name: str, parameters: Optional[Dict[str, Any]] = None, metrics: Optional[Dict[str, Any]] = None, update_type: Optional[VERSION] = "patch") -> None:
    """Callable function that saves a model and revelant info of it in the atlas model repository.
    
    Parameters
    ----------
    model: Any
        Model object to be saved in the repository
    
    model_name: str
        Name of model

    parameters: Optional[Dict[str, Any]] = None
        Model parameters stored in a dictionary

    metrics: Optional[Dict[str, Any]] = None
        Model metrics stored in a dictionary

    update_type: VERSION
        Type of update for new version (major, minor or patch)
    """   
    if not os.path.isdir(model_repository_path):
        try:
            os.mkdir(model_repository_path)
        except OSError as err:
            raise AtlasModelError(f"Error raised while creating model repository: {err.errno}")
    
    model_path = os.path.join(model_repository_path, model_name)
    last_version = "0.0.0"
    if not os.path.isdir(model_path):
        try:
            os.mkdir(model_path)
        except OSError as err:
            raise AtlasModelError(f"Error raised while creating model path: {err.errno}")
    else:
        model_versions = [model_version for model_version in os.listdir(model_path)]
        if model_versions:
            model_versions.sort(key=StrictVersion)
            last_version = model_versions[-1]
            
    new_version = generate_new_version(last_version, update_type)
    new_version_path = os.path.join(model_path, new_version)

    try:
        os.mkdir(new_version_path)
    except OSError as err:
        raise AtlasModelError(f"Error raised while creating new version path: {err.errno}")

    new_version_model_path = os.path.join(new_version_path, "model.pkl")
    with open(new_version_model_path, "wb") as f:
        cloudpickle.dump(model, f)

    model_infos = {"parameters": parameters, "metrics": metrics}
    for model_info, info_dict in model_infos.items():
        if not info_dict:
            continue

        full_json_path = os.path.join(new_version_path, model_info + ".json")

        try:
            with open(full_json_path, 'w') as f:
                json.dump(info_dict, f)
        except json.JSONDecodeError as err:
            raise AtlasModelError(f"Failed to save model {model_info}: {str(err)}")

    print(f"{model_name} {new_version} successfully stored in atlas model repository")
