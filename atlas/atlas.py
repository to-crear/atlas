import click


@click.group("atlas")
@click.version_option(package_name="atlas")
def atlas() -> None:
    """Tool for creating and deploying ML projects"""
    return None


@atlas.command("init")
def init() -> None:
    """Initialization command"""
    return None


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
