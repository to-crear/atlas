import errno
import json
import os
import subprocess
from sys import platform
from typing import Optional

import click
from packaging.version import Version

from atlas.atlas_manager import AtlasManager
from atlas.atlas_pipeline import AtlasPipeline
from atlas.load_config import ConfigValidationError, load_config_file
from config.atlas_config import ATLAS_HIDDEN_DIRECTORY

from .utils.system_utils import get_root_dir

root_dir = get_root_dir()
root_hidden_file = os.path.join(root_dir, ATLAS_HIDDEN_DIRECTORY)


@click.group("atlas")
@click.version_option(package_name="ml-atlas")
def atlas() -> None:
    """Tool for creating and deploying ML projects"""
    return None


@atlas.command("init")
def init() -> None:
    """Initialization command"""
    setup_folders = [
        "model_repository",
        "components_ouputs",
        "metadata",
        "inference",
        "manager",
    ]

    if os.path.isdir(root_hidden_file):
        click.secho("Atlas has aready being intialized!", fg="red")
        return

    try:
        os.mkdir(root_hidden_file)
        for folder in setup_folders:
            path_ = os.path.join(root_hidden_file, folder)
            os.mkdir(path_)
        # make sure hidden folder isn't displayed via UI.
        if platform == "win32":
            subprocess.run(["attrib", "+H", root_hidden_file], check=True)
        elif platform == "darwin":
            subprocess.run(["chflags", "hidden", root_hidden_file], check=True)

        # Intialize atlas
        AtlasManager(root_hidden_file)

        click.secho(f"Initialized atlas at {root_hidden_file}", fg="green")
        return
    except OSError as err:
        if err.errno == errno.EEXIST:
            click.secho(
                f"Atlas has already been initialized at {root_hidden_file}", fg="red"
            )
        else:
            click.secho(f"Error initializing atlas: {err.errno}", fg="red")


@atlas.command("stages")
def stages() -> None:
    """Print out all the stages in the pipeline"""
    try:
        config_info = load_config_file()
    except FileNotFoundError:
        click.echo(
            click.style("ERROR", fg="red") + ": Unable to find atlas-config.yaml file"
        )
        return
    except ConfigValidationError as err:
        click.echo(click.style("ERROR", fg="red") + f": {str(err)}")
        return

    click.echo("Stages in Atlas Pipeline:")
    for stage in config_info["pipeline"]["stages"].keys():
        click.echo(f"-> {stage}")


@atlas.command("stage")
@click.argument("stage_name", default=None)
def stage(stage_name) -> None:
    """Print out the information of a particular stage in the pipeline"""
    try:
        config_info = load_config_file()
    except FileNotFoundError:
        click.echo(
            click.style("ERROR", fg="red") + ": Unable to find atlas-config.yaml file"
        )
        return
    except ConfigValidationError as err:
        click.echo(click.style("ERROR", fg="red") + f": {str(err)}")
        return

    project_stages = config_info["pipeline"]["stages"]
    if stage_name not in project_stages:
        click.secho(
            f"Error: The specified stage '{stage_name}' does not exist! Re-check the stage name.",
            fg="red",
        )
        return

    stage_info = project_stages[stage_name]
    click.echo(f"\n{stage_name} stage information:\n")
    for stage_key, stage_value in stage_info.items():
        click.echo(f"-> {stage_key}: {stage_value}")
    click.echo("\n")
    return


@atlas.command("stage_output")
def stage_output() -> None:
    """Prints out the output from a particular stage."""
    return None


@atlas.command("model")
@click.argument("model_name", required=False)
@click.option("-v", "--version", help="Model version")
@click.option("-n", "--num", type=int, help="Get last n model versions")
@click.option(
    "--verbose", is_flag=True, help="Print out model parameters and performance metrics"
)
def model(
    model_name: Optional[str], version: Optional[str], num: int, verbose: bool
) -> None:
    """Prints out a list of the models in the model repository."""
    model_repository_path = os.path.join(root_hidden_file, "model_repository")
    if not os.path.isdir(model_repository_path):
        click.echo(
            click.style("ERROR", fg="red") + ": Failed to find atlas model repository"
        )
        return

    models = []
    if model_name:
        if not os.path.isdir(os.path.join(model_repository_path, model_name)):
            click.echo(
                click.style("ERROR", fg="red")
                + f": Failed to find model {model_name} in atlas model repository"
            )
            return
        models.append(model_name)
    else:
        models = os.listdir(model_repository_path)

    if not models:
        click.secho("No models found in atlas model repository", fg="yellow")
        return

    for model in models:
        model_path = os.path.join(model_repository_path, model)
        click.secho(model, fg="yellow")

        model_versions = os.listdir(model_path)
        model_versions.sort(key=Version, reverse=True)
        lastest_version = model_versions[0]

        if version:
            if not os.path.isdir(os.path.join(model_path, version)):
                click.echo(
                    click.style("ERROR", fg="red")
                    + f": Failed to find {model} {version} in atlas model repository"
                )
                continue
            if version == "latest":
                version = lastest_version

            model_versions = [version]
        else:
            if num:
                model_versions = model_versions[:num]

        for model_version in model_versions:
            if model_version == lastest_version:
                click.echo(
                    "-> "
                    + click.style(model_version, fg="bright_cyan")
                    + click.style(" (latest)", fg="green")
                )
            else:
                click.echo("-> " + click.style(model_version, fg="bright_cyan"))
            if verbose:
                model_infos = ["parameters", "metrics", "gems"]
                for model_info in model_infos:
                    info_path = os.path.join(
                        model_path, model_version, model_info + ".json"
                    )
                    if not os.path.isfile(info_path):
                        continue

                    with open(info_path, "r") as file:
                        info_dict = json.load(file)

                    click.echo(f"->-> {model_info.capitalize()}: {info_dict}")

    return


@atlas.command("run")
@click.argument("stage_name", default=None)
def run(stage_name) -> None:
    """Run the script for a particular stage or all stages."""
    try:
        config_info = load_config_file()
    except FileNotFoundError:
        click.echo(
            click.style("ERROR", fg="red") + ": Unable to find atlas-config.yaml file"
        )
        return
    except ConfigValidationError as err:
        click.echo(click.style("ERROR", fg="red") + f": {str(err)}")
        return

    project_stages = config_info["pipeline"]["stages"]

    if stage_name == "all":
        atlas_pipeline = AtlasPipeline(project_stages)
        atlas_pipeline.run_atlas()
        click.secho("Pipeline Run: Successful.", fg="green")
    else:
        if stage_name not in project_stages:
            click.secho(
                f"Error: The specified stage '{stage_name}' does not exist! Re-check the stage name.",
                fg="red",
            )
            return

        stage_info = project_stages[stage_name]
        script_ = stage_info["script"]
        click.secho(f"Running {stage_name} stage ...")
        try:
            click.secho(f"Running script: {script_} in {stage_name} stage.")
            with open(script_) as module:
                exec(module.read())
            click.secho(f"{stage_name} run: Successful.", fg="green")
            return
        except BaseException as error_message:
            click.secho(f"|{stage_name}| failed.", fg="red")
            click.secho(f"Error: {error_message}", fg="red")


def main():
    atlas(prog_name="atlas")
