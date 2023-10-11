import bpy
import os
from bpy_speckle.properties.scene import SpeckleSceneSettings





def take_screenshot():
    bpy.ops.render.render(write_still = True)
    print(f"We took a screenshot! saved at {bpy.context.scene.render.filepath}")

def set_output_path(commitId, cameraName):
    #Get Output file directory
    filepath = bpy.data.filepath
    filename = os.path.basename(filepath)
    directory = os.path.dirname(filepath)
    if not filepath:
        raise Exception("Blend file must be saved!")

    bpy.context.scene.render.filepath = os.path.join(directory, "Screenshots", f"{commitId}.{cameraName}")




speckle: SpeckleSceneSettings = bpy.context.scene.speckle


print("hello speckle screenshot tool!")
bpy.ops.speckle.users_load()
bpy.ops.speckle.receive_stream_objects()


print(f"We received the objects!")




for ob in bpy.context.scene.objects:
    if ob.type != 'CAMERA':
        continue
    bpy.context.scene.camera = ob
    commit = speckle.get_active_user().get_active_stream().get_active_branch().get_active_commit()
    set_output_path(commit.id, ob.name)
    take_screenshot()




