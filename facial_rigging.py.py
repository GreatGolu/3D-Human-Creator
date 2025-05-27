import bpy
import math
from mathutils import Vector, Euler

class PIXAR_OT_setup_facial_rig(bpy.types.Operator):
    bl_idname = "pixar.setup_facial_rig"
    bl_label = "Setup Facial Rig"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        char = context.active_object
        if not char or not char.type == 'MESH':
            self.report({'ERROR'}, "Select character mesh")
            return {'CANCELLED'}
        
        # Create facial control bones
        self.create_facial_rig(context, char)
        
        # Add shape keys for expressions
        self.create_expression_shapes(char)
        
        return {'FINISHED'}
    
    def create_facial_rig(self, context, char):
        # Create facial control armature
        bpy.ops.object.armature_add(enter_editmode=True)
        rig = context.active_object
        rig.name = f"Facial_Rig_{char.name}"
        
        bones = rig.data.edit_bones
        
        # Main facial controls
        brow_ctrl = bones.new("Brow_Ctrl")
        brow_ctrl.head = Vector((0, 0.5, 0.3))
        brow_ctrl.tail = Vector((0, 0.5, 0.4))
        
        eye_ctrl = bones.new("Eye_Ctrl")
        eye_ctrl.head = Vector((0, 0.4, 0.3))
        eye_ctrl.tail = Vector((0, 0.4, 0.4))
        
        mouth_ctrl = bones.new("Mouth_Ctrl")
        mouth_ctrl.head = Vector((0, 0.3, 0.25))
        mouth_ctrl.tail = Vector((0, 0.3, 0.35))
        
        # Setup drivers for facial controls
        bpy.ops.object.mode_set(mode='OBJECT')
        self.setup_facial_drivers(rig, char)
    
    def setup_facial_drivers(self, rig, char):
        # Add drivers to connect bones to shape keys
        if not char.data.shape_keys:
            char.shape_key_add(name="Basis")
        
        # Brow control drivers
        self.add_bone_driver(
            rig, "Brow_Ctrl", 
            char, "shape_keys.key_blocks['Brow_Up'].value", 
            axis='Z', 
            influence=0.1
        )
        
        # Eye control drivers
        self.add_bone_driver(
            rig, "Eye_Ctrl", 
            char, "shape_keys.key_blocks['Blink'].value", 
            axis='Z'
        )
        
        # Mouth control drivers
        self.add_bone_driver(
            rig, "Mouth_Ctrl", 
            char, "shape_keys.key_blocks['Smile'].value", 
            axis='Z'
        )
    
    def add_bone_driver(self, rig, bone_name, target, data_path, axis='Z', influence=1.0):
        """Helper to create bone drivers"""
        bone = rig.pose.bones[bone_name]
        driver = bone.driver_add("location", ['X','Y','Z'].index(axis)).driver
        
        var = driver.variables.new()
        var.name = "val"
        var.targets[0].id = target
        var.targets[0].data_path = data_path
        
        driver.expression = f"val * {influence}"
    
    def create_expression_shapes(self, char):
        """Create basic facial expression shape keys"""
        expressions = {
            'Smile': self.create_smile_shape,
            'Frown': self.create_frown_shape,
            'Angry': self.create_angry_shape,
            'Surprise': self.create_surprise_shape,
            'Sad': self.create_sad_shape
        }
        
        for name, func in expressions.items():
            if name not in char.data.shape_keys.key_blocks:
                sk = char.shape_key_add(name=name)
                func(char, sk)
    
    def create_smile_shape(self, char, shape_key):
        # Example - would modify vertices to create smile
        for i, vert in enumerate(char.data.vertices):
            if vert.co.y > 0.3:  # Mouth area
                shape_key.data[i].co = vert.co + Vector((0, 0, 0.02))
    
    # Similar methods for other expressions...

class PIXAR_OT_add_expression(bpy.types.Operator):
    """Add new facial expression"""
    bl_idname = "pixar.add_expression"
    bl_label = "Add Expression"
    
    expression: bpy.props.EnumProperty(
        items=[
            ('SMILE', "Smile", ""),
            ('FROWN', "Frown", ""),
            ('ANGRY', "Angry", ""),
            ('SAD', "Sad", "")
        ]
    )
    
    def execute(self, context):
        char = context.active_object
        if not char or not char.type == 'MESH':
            self.report({'ERROR'}, "Select character mesh")
            return {'CANCELLED'}
        
        if not char.data.shape_keys:
            char.shape_key_add(name="Basis")
        
        # Create the selected expression
        sk = char.shape_key_add(name=self.expression.capitalize())
        
        # Apply shape (simplified example)
        for i, vert in enumerate(char.data.vertices):
            if self.expression == 'SMILE':
                sk.data[i].co = vert.co + Vector((0, 0, 0.02))
            elif self.expression == 'FROWN':
                sk.data[i].co = vert.co + Vector((0, 0, -0.02))
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(PIXAR_OT_setup_facial_rig)
    bpy.utils.register_class(PIXAR_OT_add_expression)

def unregister():
    bpy.utils.unregister_class(PIXAR_OT_add_expression)
    bpy.utils.unregister_class(PIXAR_OT_setup_facial_rig)