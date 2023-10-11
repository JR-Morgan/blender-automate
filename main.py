"""This module contains the business logic of the function.

use the automation_context module to wrap your function in an Autamate context helper
"""

from speckle_automate import (
    AutomationContext,
    execute_automate_function,
)
from pathlib import Path

from subprocess import run


def automate_function(
    automate_context: AutomationContext
) -> None:
    
    account = automate_context.speckle_client.account
    AccountStorage.SaveObject(account.id, JsonConvert.SerializeObject(account));
    run(    
        [
            'blender',
            '"environment.blend"',
            '--background',
            '--python speckle_import.py',
            '-f 10',
        ],
        capture_output=True,
        text=True,
    )

    for file_path in Path("./screenshots").glob("**/*.png") :
        automate_context.store_file_result(file_path)

    automate_context.mark_run_success("YAYAY!!! we did it!")




# make sure to call the function with the executor
if __name__ == "__main__":
    # NOTE: always pass in the automate function by its reference, do not invoke it!

    # pass in the function reference with the inputs schema to the executor
    execute_automate_function(automate_function)

    # if the function has no arguments, the executor can handle it like so
    # execute_automate_function(automate_function_without_inputs)
