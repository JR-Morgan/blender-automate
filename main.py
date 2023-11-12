"""This module contains the business logic of the function.

use the automation_context module to wrap your function in an Automate context helper
"""

import json
from speckle_automate import (
    AutomationContext,
    execute_automate_function,
)
from pathlib import Path

from subprocess import run

SCREENSHOTS_PATH = "./Screenshots"

def automate_function(
    automate_context: AutomationContext
) -> None:
    
    # Get info from Automate
    client = automate_context.speckle_client
    PROJECT_ID = automate_context.automation_run_data.project_id
    VERSION_ID = automate_context.automation_run_data.version_id
    OBJECT_ID = client.commit.get(PROJECT_ID, VERSION_ID).referencedObject

    data = {
        "TOKEN": client.account.token,
        "SERVER_URL": client.account.serverInfo.url,
        "PROJECT_ID": PROJECT_ID,
        "OBJECT_ID": OBJECT_ID
    }

    Path("./automate_data.json").write_text(json.dumps(data))
    Path(SCREENSHOTS_PATH).mkdir(exist_ok=True)
    
    print("Starting blender")
       
    process = run(    
        [
            'blender',
            'environment.blend',
            '--background',
            '--python',
            'speckle_import.py'
        ],
        capture_output=True,
        text=True,
    )
    print(f"Blender subprocess finished with exit code {process.returncode}")
    print(process.stdout)
    print(process.stderr)
    
    if process.returncode != 0:
        automate_context.mark_run_failed(f"The blender process exited with error code {process.returncode}\n{process.stdout}")
    else:
        files = list(Path(SCREENSHOTS_PATH).glob("**/*.png"))
        for file_path in files:
            automate_context.store_file_result(file_path)

        automate_context.mark_run_success(f"YAYAY!!! we did it! - {len(files)} exported")




# make sure to call the function with the executor
if __name__ == "__main__":
    # NOTE: always pass in the automate function by its reference, do not invoke it!

    # pass in the function reference with the inputs schema to the executor
    execute_automate_function(automate_function)

    # if the function has no arguments, the executor can handle it like so
    # execute_automate_function(automate_function_without_inputs)
