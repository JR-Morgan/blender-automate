from bpy_speckle.convert.to_native import _deep_conversion

from specklepy.api import operations
from specklepy.transports.server import ServerTransport
from automate_data import *


def set_filename(fileName):
    """Sets the output directory for rendered images"""
    filepath = bpy.data.filepath
    directory = os.path.dirname(filepath)
    if not filepath:
        raise Exception("Blend file must be saved!")

    bpy.context.scene.render.filepath = os.path.join(directory, "Screenshots", fileName)


print(f"Starting Receive...")

remote_transport = ServerTransport(STREAMID, token=TOKEN, url=SERVER_URL)
commit_object = operations.receive(OBJECTID, remote_transport)

converted_objects = {}
_deep_conversion(commit_object, converted_objects, True)


all_cameras = [o for o in bpy.context.scene.objects if o.type == "CAMERA"]
total = len(all_cameras)

print(f"Starting rendering cameras... 0/{total}")

for i, ob in enumerate(all_cameras):
    # Set as active render cam
    bpy.context.scene.camera = ob

    # Render camera to output directory
    set_filename(f"{ob.name}")
    bpy.ops.render.render(write_still=True)
    print(f"Render {i}/{total} complete! saved at {bpy.context.scene.render.filepath}")

print(f"All Done!")
