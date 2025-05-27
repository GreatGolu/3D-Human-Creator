import bpy

class PIXAR_OT_setup_lipsync(bpy.types.Operator):
    bl_idname = "pixar.setup_lipsync"
    bl_label = "Setup Lip-Sync Shapes"
    
    def execute(self, context):
        char = context.active_object
        if not char or not char.type == 'MESH':
            self.report({'ERROR'}, "Select character mesh")
            return {'CANCELLED'}
        
        self.create_phoneme_shapes(char)
        return {'FINISHED'}
    
    def create_phoneme_shapes(self, char):
        """Create shape keys for visemes"""
        phonemes = {
            'A': self.create_A_shape,
            'I': self.create_I_shape,
            'O': self.create_O_shape,
            'U': self.create_U_shape,
            'F': self.create_F_shape,
            'V': self.create_V_shape,
            'L': self.create_L_shape,
            'M': self.create_M_shape,
            'W': self.create_W_shape
        }
        
        for name, func in phonemes.items():
            if f"Viseme_{name}" not in char.data.shape_keys.key_blocks:
                sk = char.shape_key_add(name=f"Viseme_{name}")
                func(char, sk)
    
    def create_A_shape(self, char, shape_key):
        """Open mouth shape for 'Ah' sound"""
        for i, vert in enumerate(char.data.vertices):
            if 0.2 < vert.co.y < 0.4:  # Mouth area
                shape_key.data[i].co = vert.co + Vector((0, 0, 0.1))
    
    def create_I_shape(self, char, shape_key):
        """'Ee' sound shape"""
        for i, vert in enumerate(char.data.vertices):
            if 0.2 < vert.co.y < 0.4:
                shape_key.data[i].co.x *= 0.9  # Narrow mouth
    
    # Similar methods for other phonemes...

class PIXAR_OT_preview_phoneme(bpy.types.Operator):
    bl_idname = "pixar.preview_phoneme"
    bl_label = "Preview Phoneme"
    
    phoneme: bpy.props.StringProperty()
    
    def execute(self, context):
        char = context.active_object
        if not char or not char.data.shape_keys:
            return {'CANCELLED'}
        
        # Reset all phonemes
        for kb in char.data.shape_keys.key_blocks:
            if kb.name.startswith("Viseme_"):
                kb.value = 0
        
        # Activate selected phoneme
        if f"Viseme_{self.phoneme}" in char.data.shape_keys.key_blocks:
            char.data.shape_keys.key_blocks[f"Viseme_{self.phoneme}"].value = 1
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(PIXAR_OT_setup_lipsync)
    bpy.utils.register_class(PIXAR_OT_preview_phoneme)

def unregister():
    bpy.utils.unregister_class(PIXAR_OT_preview_phoneme)
    bpy.utils.unregister_class(PIXAR_OT_setup_lipsync)