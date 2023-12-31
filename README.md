# Atlas

Next level MLOps tool for creating and deploying ML projects!

## Local Setup

To install the package, clone the repository and install the requirements in a virtual environment. After that, run;

`python setup.py develop`

Test out that it works by running;

`atlas --version`

## Running Tests

For testing, run the following command in the virtual environment;

`python3 -m pytest`

## Format for config file

Projects using atlas should have a config file in it's root directory named
`atlas-config.yaml`. A sample yaml file is given below;

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
