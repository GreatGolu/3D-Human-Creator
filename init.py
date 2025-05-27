from . import (
    character_properties,
    character_operator,
    character_panel,
    face_library,
    facial_rigging,  # New
    lipsync_shapes   # New
)

def register():
    character_properties.register()
    character_operator.register()
    character_panel.register()
    face_library.register()
    facial_rigging.register()  # New
    lipsync_shapes.register()  # New

def unregister():
    lipsync_shapes.unregister()  # New
    facial_rigging.unregister()  # New
    face_library.unregister()
    character_panel.unregister()
    character_operator.unregister()
    character_properties.unregister()
