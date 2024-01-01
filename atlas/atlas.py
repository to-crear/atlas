import os
import click
import errno
import subprocess
from sys import platform
from .utils.system_utils import get_root_dir


@click.group("atlas")
@click.version_option(package_name="atlas")
def atlas() -> None:
    """Tool for creating and deploying ML projects"""
    return None


@atlas.command("init")
def init() -> None:
    """Initialization command"""
    hidden_dir = ".atlas"
    setup_folders = ["model_repository","components_ouputs","metadata","inference","manager"]
    root_dir = get_root_dir()
    root_hidden_file = os.path.join(root_dir, hidden_dir)
    try:
        os.mkdir(root_hidden_file)
        for folder in setup_folders:
            path_ = os.path.join(root_hidden_file, folder)
            os.mkdir(path_)
        # make sure hidden folder isn't displayed via UI.
        if platform == "win32":
            subprocess.run(["attrib","+H", root_hidden_file], check=True)
        elif platform == "darwin":
            subprocess.run(["chflags", "hidden", root_hidden_file], check=True)

        click.secho(f"Initialized atlas at {root_hidden_file}", fg="green")
        return 
    except OSError as e:
        if e.errno == errno.EEXIST:
            click.secho(f"Atlas has already been initialized at {root_hidden_file}", fg="red")
        else:
            click.secho(f"Error initializing atlas: {e.errno}", fg="red")
            
@atlas.command("stages")
def stages() -> None:
    """Print out all the stages in the pipeline"""
    return None


@atlas.command("stage")
def stages() -> None:
    """Print out the information of a particular stage in the pipeline"""
    return None


@atlas.command("stage_output")
def stages() -> None:
    """Prints out the output from a particular stage."""
    return None


@atlas.command("model")
def model() -> None:
    """Prints out a list of the models in the model repository."""
    return None


@atlas.command("run")
def run() -> None:
    """Run the script for a particular stage or all stages."""
    return None


def main():
    atlas(prog_name="atlas")
