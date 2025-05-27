class PIXAR_PT_creator_panel(Panel):
    # ... (previous code remains) ...
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.pixar_character_props
        
        # ... (previous UI elements remain) ...
        
        # Facial Rigging Section
        if context.active_object and context.active_object.name.startswith("Pixar_"):
            box = layout.box()
            box.label(text="Facial Controls", icon='EMOTION_HAPPY')
            
            if "Facial_Rig" not in context.active_object.children:
                box.operator("pixar.setup_facial_rig", icon='CONSTRAINT_BONE')
            else:
                row = box.row()
                row.operator("pixar.add_expression", text="Add Smile").expression = 'SMILE'
                row.operator("pixar.add_expression", text="Add Frown").expression = 'FROWN'
                
                # Expression sliders
                if context.active_object.data.shape_keys:
                    for kb in context.active_object.data.shape_keys.key_blocks:
                        if kb.name in ['Smile', 'Frown', 'Angry', 'Sad']:
                            box.prop(kb, "value", text=kb.name, slider=True)
            
            # Lip-Sync Controls
            box = layout.box()
            box.label(text="Lip-Sync Shapes", icon='SPEAKER')
            
            if "Viseme_A" not in context.active_object.data.shape_keys.key_blocks:
                box.operator("pixar.setup_lipsync", text="Setup Lip-Sync")
            else:
                row = box.row()
                row.operator("pixar.preview_phoneme", text="A").phoneme = 'A'
                row.operator("pixar.preview_phoneme", text="I").phoneme = 'I'
                row.operator("pixar.preview_phoneme", text="O").phoneme = 'O'
                
                row = box.row()
                row.operator("pixar.preview_phoneme", text="U").phoneme = 'U'
                row.operator("pixar.preview_phoneme", text="F").phoneme = 'F'
                row.operator("pixar.preview_phoneme", text="V").phoneme = 'V'
                
                # Phoneme sliders
                for kb in context.active_object.data.shape_keys.key_blocks:
                    if kb.name.startswith("Viseme_"):
                        box.prop(kb, "value", text=kb.name[7:], slider=True)