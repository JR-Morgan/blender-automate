import os

import bpy

bpy.ops.preferences.addon_install(filepath="/blender-connector.zip")
bpy.ops.preferences.addon_enable(module="bpy_speckle")
bpy.ops.wm.save_userpref()
