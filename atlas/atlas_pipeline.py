from collections import deque

import click


class AtlasPipelineError(Exception):
    """Error when calling atlas pipeline class functions"""


class AtlasStage:
    """Atlas Stage Class Object"""

    def __init__(self, stage_name: str, script: str, next_stages: list[str]):
        self.stage_name = stage_name
        self.script = script
        self.next_stages = next_stages


class AtlasPipeline:
    """Atlas Pipeline Class object."""

    def __init__(self, project_stages: dict[str, AtlasStage]):
        self.stages: dict[str, AtlasStage] = {}
        self.root_stage: AtlasStage = None
        self.project_stages = project_stages
        self.initialize_run_pipeline()

    def __iter__(self):
        return iter(self.stages.values())

    def _add_stage(self, stage_name: str, stage_info: dict) -> None:
        """Internal function that populates the DAG pipeline with the stages.

        Parameters
        ----------
        stage_name: str
          Name of stage.

        stage_info: dict
          Information containing stage.
        """
        stage_script = stage_info.get("script")
        next_stages = stage_info.get("next_stages")

        root_stage = stage_info.get("root")
        atlas_stage = AtlasStage(stage_name, stage_script, next_stages)

        if root_stage:
            self.root_stage = atlas_stage
        self.stages[stage_name] = atlas_stage

    def initialize_run_pipeline(self) -> None:
        """Callable function that populates the DAG pipeline with the stages."""
        for stage in self.project_stages:
            if stage in self.stages:
                continue
            self._add_stage(stage, self.project_stages[stage])

    def _run_stage(self, stage_obj: AtlasStage) -> None:
        """Internal function runs the atlas stage.

        Parameters
        ----------
        stage_obj: AtlasStage
          AtlasStage Class object
        """
        script_ = stage_obj.script
        try:
            print(f"Running script: {script_} in |{stage_obj.stage_name}| stage.")
            with open(script_) as module:
                exec(module.read())
            click.secho(f"|{stage_obj.stage_name}| is successful.", fg="green")
            print("\n===\n")
        except BaseException as error_message:
            click.secho(f"|{stage_obj.stage_name}| failed.", fg="red")
            raise AtlasPipelineError(f"Error: {error_message}")

    def run_atlas(self):
        """Callable function that runs the atlas pipeline"""
        current_stage = self.root_stage

        if current_stage is None:
            raise AtlasPipelineError("No root stage been set.")

        stages_queue = deque([current_stage])
        active_stage = set()

        while stages_queue:

            curr_stage = stages_queue.popleft()

            self._run_stage(curr_stage)
            next_stages = curr_stage.next_stages

            if next_stages is None:
                return

            for next_stage in next_stages:
                if next_stage not in active_stage:
                    stage_object = self.stages[next_stage]
                    active_stage.add(stage_object)
                    stages_queue.append(stage_object)
