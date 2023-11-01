# Blender <> Automate


Speckle Automate unlocks new potentials for running Blender in the cloud.

This Speckle Function uses Blender's rendering engine *Cycles* to produce global illumation renders for each 3d view/camera in your versioned Speckle data.


## Using this Speckle Function

1. [Create](https://automate.speckle.dev/) a new Speckle Automation.
1. Select your Speckle Project and Speckle Model.
1. Select the existing Speckle Function named [`blender-automate`](https://automate.speckle.dev/functions/fe6015a999).
1. Click `Create Automation`.


## Repostructure

The function entry point is `main.py` following the structure of the [speckle_automate_python_example](https://github.com/specklesystems/speckle_automate_python_example).

The function serializes an `automate_data.json` file with the required data to receive the Speckle data within a Blender subprocess running the Speckle Blender connector.

`speckle_import.py` runs within the Blender context, receiving speckle data, applying material styalisation, replacing Speckle Rooms with point lights, and rendering each camera to the `./Screenshots` folder. Automate will then pickup and attach these renders as blobs to the automate result.


## Developer Requirements

1. Install the following:
    - [Python 3](https://www.python.org/downloads/)
    - [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
    - [Blender 3.X](https://www.blender.org/)
1. Run `poetry shell && poetry install` to install the required Python packages.

## Building and Testing

The code can be tested locally by running `poetry run pytest`.
The code should also be packaged into the format required by Speckle Automate, a Docker Container Image, and that should also be tested.

## Resources

- [Learn](https://speckle.guide/dev/python.html) more about SpecklePy, and interacting with Speckle from Python.
