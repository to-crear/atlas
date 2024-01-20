import os
import click
import errno
import subprocess
from sys import platform

from config.atlas_config import ATLAS_HIDDEN_DIRECTORY
from .utils.system_utils import get_root_dir
from atlas.load_config import ConfigValidationError, load_config_file


@click.group("atlas")
@click.version_option(package_name="atlas")
def atlas() -> None:
    """Tool for creating and deploying ML projects"""
    return None


@atlas.command("init")
def init() -> None:
    """Initialization command"""
    setup_folders = ["model_repository","components_ouputs","metadata","inference","manager"]
    root_dir = get_root_dir()
    root_hidden_file = os.path.join(root_dir, ATLAS_HIDDEN_DIRECTORY)
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
    try:
        config_info = load_config_file()
    except FileNotFoundError:
        click.echo(click.style("ERROR", fg="red") + ": Unable to find atlas-config.yaml file")
        return
    except ConfigValidationError as err:
        click.echo(click.style("ERROR", fg="red") + f": {str(err)}")
        return

    click.echo("Stages in Atlas Pipeline:")
    for stage in config_info["pipeline"]["stages"].keys():
        click.echo(f"-> {stage}")

@atlas.command("stage")
@click.argument('stage_name', default=None)
def stage(stage_name) -> None:
    """Print out the information of a particular stage in the pipeline"""
    try:
        config_info = load_config_file()
    except FileNotFoundError:
        click.echo(click.style("ERROR", fg="red") + ": Unable to find atlas-config.yaml file")
        return
    except ConfigValidationError as err:
        click.echo(click.style("ERROR", fg="red") + f": {str(err)}")
        return

    project_stages = config_info["pipeline"]["stages"]
    if stage_name not in project_stages:
        click.secho(f"The specified stage: {stage_name} does not exist! Re-check the stage name.", fg="red")
        return
    else:
        stage_info = project_stages[stage_name]
        click.echo(f"\n{stage_name} stage information:\n") 
        for stage_key, stage_value in stage_info.items():
            click.echo(f"-> {stage_key}: {stage_value}")
        click.echo(f"\n")
        return


@atlas.command("stage_output")
def stage_output() -> None:
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
