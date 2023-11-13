import math
import bpy
import json
from pathlib import Path

from mathutils import Color, Vector
from bpy_speckle.convert.to_native import _deep_conversion, can_convert_to_native, convert_to_native, display_value_to_native, get_scale_factor

from specklepy.api import operations
from specklepy.transports.server import ServerTransport

from bpy_speckle.functions import get_default_traversal_func

filepath = bpy.data.filepath
directory = Path(filepath).parent

def set_filename(fileName):
    """Sets the output directory for rendered images"""

    if not filepath:
        raise Exception("Blend file must be saved!")
    
    path = Path(directory, "Screenshots", fileName)
    print(path)
    bpy.context.scene.render.filepath = str(path)


print(f"Starting Receive...")

text = Path(directory, "automate_data.json").read_text()
data = json.loads(text)

PROJECT_ID = data["PROJECT_ID"]
TOKEN = data["TOKEN"]
SERVER_URL = data["SERVER_URL"]
OBJECT_ID = data["OBJECT_ID"]

remote_transport = ServerTransport(PROJECT_ID, token=TOKEN, url=SERVER_URL)
root_object = operations.receive(OBJECT_ID, remote_transport)

converted_objects = {}
_deep_conversion(root_object, converted_objects, True)

#Make all materials white
for mat in bpy.data.materials:
    COLOR = (1.0, 1.0, 1.0, 1.0)
    mat.diffuse_color = COLOR
    
    if not mat.node_tree:
        continue
    inputs = mat.node_tree.nodes["Principled BSDF"].inputs
    inputs["Base Color"].default_value = COLOR

# Convert all rooms as lights
traversal_func = get_default_traversal_func(can_convert_to_native)
rooms = [x.current for x in traversal_func.traverse(root_object) if x.current.speckle_type == "Objects.BuiltElements.Room"]

light = bpy.data.lights.new("myLight", 'POINT')
light.color = Color((1, 0.34, 0.1))
light.energy = 300 #watts

print(f"Found {len(rooms)} rooms")
for room in rooms:
    (converted, _) = display_value_to_native(room, f"FakeRoom{room.id}", get_scale_factor(room))
    if not converted:
        continue
    
    #calculate bounds
    minimum = Vector((+math.inf, +math.inf, +math.inf))
    maximum = Vector((-math.inf, -math.inf, -math.inf))

    for vert in converted.vertices:
        minimum.x = min(minimum.x, vert.co.x)
        minimum.y = min(minimum.y, vert.co.y)
        minimum.z = min(minimum.z, vert.co.z)
        maximum.x = max(maximum.x, vert.co.x)
        maximum.y = max(maximum.y, vert.co.y)
        maximum.z = max(maximum.z, vert.co.z)

    light_pos = minimum.lerp(maximum, 0.5)

    light_object = bpy.data.objects.new(f"FakeLight{room.id}", light)
    light_object.matrix_local.translation = light_pos

    bpy.context.collection.objects.link(light_object)


all_cameras = [o for o in bpy.context.scene.objects if o.type == "CAMERA"]
total = len(all_cameras)

print(f"Starting rendering cameras... 0/{total}")

for i, ob in enumerate(all_cameras):
    # Set as active render cam
    bpy.context.scene.camera = ob

    # Render camera to output directory
    set_filename(f"{ob.name}")
    bpy.ops.render.render(write_still=True)
    print(f"Render {i + 1}/{total} complete! saved at {bpy.context.scene.render.filepath}")

print(f"All Done!")
