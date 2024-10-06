# Atlas

[![PyPI Atlas](https://img.shields.io/pypi/v/ml-atlas.svg?style=for-the-badge&logo=pypi&logoColor=white&label=ml-atlas)](https://pypi.org/project/ml-atlas/) [![License](https://img.shields.io/badge/license-Apache%202-brightgreen.svg?style=for-the-badge&logo=apache)](https://github.com/to-crear/atlas/blob/main/LICENSE)

Atlas is an MLOps tool used for creating and managing the lifecycle of machine learning projects. With Atlas, users are able to create a pipeline for running end-to-end machine learning projects, as well as store models in a versioned manner.

## Usage

Atlas is available as a Python library and can be installed via pip;

`pip install ml-atlas`

In the project's root directory, a yaml config that defines the pipeline structure is also required. The yaml **must** be named `atlas-config.yaml`. The format for this config file should be as follows;

```yaml
pipeline:
  stages:
    data_collection:
      script: "data_collection.py"
      root: True
      next_stages: 
        - preprocessing

    preprocessing:
      script: "preprocess.py"
      next_stages:
        - model_training

    model_training:
      script: "train.py"
```

The yaml contains a `pipeline` key, and inside it a `stages` key which lists all the stages in the pipeline. Each stage is listed along with the `script` parameter which is the path to the script for running this part of the pipeline. There's also a `next_stage` parameter for the next stage in the pipeline to run. `root` is only defined for the stage that starts the pipeline workflow.

From the sample yaml file there are three stages in the workflow named **data_collection**, **preprocessing**, and **model_training**. Each class has the path to its script as well as the next stage after it, except the **model_training** stage which is supposed to be the final stage in the pipeline. Note that **data_collection** stage also has a `root` parameter that is set to `True`, showing that this is the start of the pipeline.

Atlas will need to be initialized in the root directory of the project using the `atlas init` command. After initialization, atlas commands can be run successfully.

Once the config file is present and Atlas has been initialized, the project is all set to run the different commands.

The following commands can be run;

* `atlas stages` - List all the stages in the pipeline

* `atlas stage {stage_name}` - Return information on that particular stage. If `stage_name` is not defined, information on all stages is returned. 

* `atlas run {stage_name}` - Run a particular stage in the pipeline. If `atlas run all` is used instead, the whole pipeline is ran in the order specified from the atlas config.

* `atlas model` - Return information on all models in atlas model repository. `-v` tag is used to specify a specific version, `-n` tag will return the last n models stored in the repository (sorted in descending order of version) and `--verbose` tag also return performance metrics and other information attached to the model.

To save and load models while running scripts in your project, use the `save_model` and `load_model` modules.

```py3
from atlas.model import save_model, load_model

# Creating a model
model = MyModel()
model_parameters = {"max_depth": 2, "max_features": 3}
model_metrics = {"accuracy": 0.98}

# Save model in Atlas model repository
save_model(
  model=model,
  model_name="my-model",
  parameters=model_parameters,
  metrics=model_metrics,
  update_type="patch" # Can be either major, minor or patch
)

# Load model from Atlas model repository
created_model = load_model(model_name="my_model", version="1.0.0")
```

## Contributing

Contributions are encouraged to Atlas as it an open source project. Feel free to reach out via tocrear.3@gmail.com if you need more information!
