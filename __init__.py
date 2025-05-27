bl_info = {
    "name": "Pixar-Style Character Creator",
    "author": "Your Name",
    "version": (1, 3, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > Pixar Creator",
    "description": "Create stylized characters with facial rigging and lip-sync controls",
    "warning": "",
    "doc_url": "https://example.com/docs",
    "tracker_url": "https://example.com/support",
    "category": "Character",
}

import bpy
from . import (
    character_properties,
    character_operator,
    character_panel,
    face_library,
    facial_rigging,
    lipsync_shapes
)

def register():
    character_properties.register()
    character_operator.register()
    character_panel.register()
    face_library.register()
    facial_rigging.register()
    lipsync_shapes.register()

def unregister():
    lipsync_shapes.unregister()
    facial_rigging.unregister()
    face_library.unregister()
    character_panel.unregister()
    character_operator.unregister()
    character_properties.unregister()

# Required for Blender to recognize the addon
if __name__ == "__main__":
    register()