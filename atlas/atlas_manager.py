import os
import json
import click


class AtlasManagerError(Exception):
    """Error when calling atlas manager class functions"""

class AtlasManager:

    def __init__(self, system_root_folder):
        self.project_json = "atlas_project.json"
        self.project_folder = "manager"
        json_folder_path_ = os.path.join(self.project_folder, self.project_json)
        self.project_json_path = os.path.join(system_root_folder, json_folder_path_)
    
    def save_info_to_project_json(self, root_path: str) -> True:
        """Saves information to project json file.

        Parameters
        ----------
        root_path: str
          Root directory path atlas was intializied
        stage_info: dict
          Information containing stage.

        Returns
        -------
        : bool
        """
        if os.path.isfile(self.project_json_path):
            click.secho(f"Atlas has aready being intialized!", fg="orange")
            return

        try:
            with open(self.project_json_path,"w") as json_file:
                tmp_dict = {}
                tmp_dict["project_root_path"] = root_path
                json.dump(tmp_dict, json_file)
            return True
        except:
            raise  AtlasManagerError(f"Error saving information to {self.project_json}.")