import json
import os
from typing import Optional, Union

from config.atlas_config import ATLAS_HIDDEN_DIRECTORY


class AtlasManagerError(Exception):
    """Error when calling atlas manager class functions"""


class AtlasManager:
    """AtlasManager Class Object"""

    def __init__(self, system_root_folder=None):
        self.project_json = "atlas_project.json"
        self.project_folder = "manager"
        json_folder_path_ = os.path.join(self.project_folder, self.project_json)
        if system_root_folder is None:
            self.system_root_folder = self.get_project_dot_atlas_folder_path()
            self.project_json_path = os.path.join(
                self.system_root_folder, json_folder_path_
            )
        else:
            self.system_root_folder = system_root_folder
            self.project_json_path = os.path.join(
                self.system_root_folder, json_folder_path_
            )
            tmp_info = {"project_root_path": self.system_root_folder}
            self.save_info_to_project_json(tmp_info)

    def __search_for_dot_atlas_folder_path(self):
        """Recursively Search for .atlas directory.

        Parameters
        ----------

        Returns
        -------
        : bool
        """
        dot_atlas_path = None

        try:
            for root, dirs, files in os.walk("."):
                for dir_ in dirs:
                    if dir_ == ATLAS_HIDDEN_DIRECTORY:
                        root_dir = os.path.join(root, dir_)
                        dot_atlas_path = os.path.abspath(root_dir)
                        return dot_atlas_path
        except Exception as e:
            raise AtlasManagerError(f"'.atlas' Search Error: {e}")

    def get_project_dot_atlas_folder_path(self):
        """Get system root folder

        Parameters
        ----------

        Returns
        -------
        : bool
        """
        root_hidden_dir = self.__search_for_dot_atlas_folder_path()
        return root_hidden_dir

    def save_info_to_project_json(self, info: dict) -> Optional[Union[bool, None]]:
        """Saves information to project json file.

        Parameters
        ----------
        info:  dict
            information to  be save into json file.

        Returns
        -------
        : bool
        """
        try:
            with open(self.project_json_path, "w") as json_file:
                json.dump(info, json_file)
            return True
        except:
            raise AtlasManagerError(f"Error saving information to {self.project_json}.")
