bl_info = {
    "name": "XPS Extender",
    "author": "Pooria1998",
    "version": (1, 0),
    "blender": (3, 5, 0),
    "location": "View3D > Properties > XPS",
    "description": "a set of tools and material fixes for xps models",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}


import bpy
import os
from mathutils import Vector


class MATERIAL_OT_xps_to_principled(bpy.types.Operator):
    """replace xps node group with principled shader"""
    bl_idname = "material.xps_to_principled"
    bl_label = "Convert XPS to Principled"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        objects = bpy.context.selected_objects

        for object in objects:
            
            mat = object.data.materials[0]
            nodes = mat.node_tree.nodes

            xps_shader = nodes.get("Group")
            nodes.remove(xps_shader)

            principled_shader = nodes.new(type="ShaderNodeBsdfPrincipled")
            principled_shader.location = Vector((300.0,385.0))
            output_node = nodes.get("Material Output")
            mat.node_tree.links.new(principled_shader.outputs[0], output_node.inputs[0])


            # get a list of image textures in a material node tree

            image_texture_nodes = []

            for node in nodes:
                if node.type == 'TEX_IMAGE':
                    image_texture_nodes.append(node)
                    
            # do operations based on each type of image texture
                    
            for node in image_texture_nodes:
                if node.label == "Diffuse":
                    mat.node_tree.links.new(node.outputs[0], principled_shader.inputs[0])
                    mat.node_tree.links.new(node.outputs[1], principled_shader.inputs[21])
                    
                if node.label == "Specular":
                    invert_node = nodes.new(type="ShaderNodeInvert")
                    invert_node.location = Vector((50.0,100.0))
                    math_node = nodes.new(type="ShaderNodeMath")
                    math_node.location = Vector((-150.0,100.0))
                    math_node.operation = "POWER"
                    math_node.inputs[1].default_value = 1
                    mat.node_tree.links.new(node.outputs[0], math_node.inputs[0])
                    mat.node_tree.links.new(math_node.outputs[0], invert_node.inputs[1])
                    mat.node_tree.links.new(invert_node.outputs[0], principled_shader.inputs[9])
                    
                if node.label == "Bump Map":
                    normalmap_node = nodes.new(type="ShaderNodeNormalMap")
                    normalmap_node.location = Vector((-150.0,-200.0))
                    mat.node_tree.links.new(node.outputs[0], normalmap_node.inputs[1])
                    mat.node_tree.links.new(normalmap_node.outputs[0], principled_shader.inputs[22])
                    
                if node.label == "Light Map":
                    nodes.remove(node)
                    
                
        return {"FINISHED"}


class MATERIAL_OT_fix_blendmode(bpy.types.Operator):
    """change non-opaque materials blend mode to alpha hashed for selected objects"""
    bl_idname = "material.fix_blendmode"
    bl_label = "fix non-opaque blend mode"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        objects = bpy.context.selected_objects
        for object in objects:
            mat = object.data.materials[0]
            if mat.blend_method != "OPAQUE":
                mat.blend_method = "HASHED"
                mat.shadow_method = "HASHED"
        return {"FINISHED"}
    
    
class MATERIAL_OT_all_opaque(bpy.types.Operator):
    """change all materials blend mode to opaque for selected objects"""
    bl_idname = "material.opaque_blendmode"
    bl_label = "opaque blend mode"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        objects = bpy.context.selected_objects
        for object in objects:
            mat = object.data.materials[0]
            mat.blend_method = "OPAQUE"
            mat.shadow_method = "OPAQUE"
        return {"FINISHED"}
    
    
class MATERIAL_OT_all_blend(bpy.types.Operator):
    """change all materials blend mode to alpha blend for selected objects"""
    bl_idname = "material.alhpa_blend_blendmode"
    bl_label = "alpha-blend blend mode"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        objects = bpy.context.selected_objects
        for object in objects:
            mat = object.data.materials[0]
            mat.blend_method = "BLEND"
            mat.shadow_method = "HASHED"
        return {"FINISHED"}
    
    
class MATERIAL_OT_all_hashed(bpy.types.Operator):
    """change all materials blend mode to alpha hashed for selected objects"""
    bl_idname = "material.alpha_hashed_blendmode"
    bl_label = "alpha-hashed blend mode"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        objects = bpy.context.selected_objects
        for object in objects:
            mat = object.data.materials[0]
            mat.blend_method = "HASHED"
            mat.shadow_method = "HASHED"
        return {"FINISHED"}
    
    
class MATERIAL_OT_all_clip(bpy.types.Operator):
    """change all materials blend mode to alpha clip for selected objects"""
    bl_idname = "material.alpha_clip_blendmode"
    bl_label = "alpha-clip blend mode"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        objects = bpy.context.selected_objects
        for object in objects:
            mat = object.data.materials[0]
            mat.blend_method = "CLIP"
            mat.shadow_method = "HASHED"
        return {"FINISHED"}


class ARMATURE_OT_fix_bone_layers(bpy.types.Operator):
    """distribute different groups of bones to separate bones layers"""
    bl_idname = "armature.fix_bone_layers"
    bl_label = "fix bone layers"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        armature_obj = bpy.context.active_object
        if armature_obj.type != 'ARMATURE':
            print("Error: Selected object is not an armature.")
            exit()
        
        for bone in armature_obj.data.bones:
    
            bpy.ops.object.mode_set(mode='POSE')
            
            if "ctr" in bone.name.lower():
                bpy.ops.pose.select_all(action='DESELECT')
                bone.select = True
                bpy.ops.pose.hide(unselected=False)        
                
            if "hair" in bone.name.lower():
                bpy.ops.pose.select_all(action='DESELECT')
                bone.select = True
                bone.layers[9] = True
                bone.layers[0] = False
                
            if "head" in bone.name.lower():
                bpy.ops.pose.select_all(action='DESELECT')
                bone.select = True
                bone.layers[8] = True
                bone.layers[0] = False
                
            if bone.name == "head neck lower":
                bpy.ops.pose.select_all(action='DESELECT')
                bone.select = True
                bone.layers[0] = True
                bone.layers[8] = False
                
            if bone.name == "head neck upper":
                bpy.ops.pose.select_all(action='DESELECT')
                bone.select = True
                bone.layers[0] = True
                bone.layers[8] = False
                
            if bone.name == "head eyelid upper *side*.R":
                bpy.ops.pose.select_all(action='DESELECT')
                bone.select = True
                bone.layers[0] = True
                bone.layers[8] = False
                
            if bone.name == "head eyelid upper *side*.L":
                bpy.ops.pose.select_all(action='DESELECT')
                bone.select = True
                bone.layers[0] = True
                bone.layers[8] = False
            
            if bone.name == "head eyeball *side*.R":
                bpy.ops.pose.select_all(action='DESELECT')
                bone.select = True
                bone.layers[0] = True
                bone.layers[8] = False
            
            if bone.name == "head eyeball *side*.L":
                bpy.ops.pose.select_all(action='DESELECT')
                bone.select = True
                bone.layers[0] = True
                bone.layers[8] = False
                
            if "breast" in bone.name.lower():
                bpy.ops.pose.select_all(action='DESELECT')
                bone.select = True
                bone.layers[10] = True
                bone.layers[0] = False
                
            if bone.name == "breast *side* base.L" or bone.name == "breast left base":
                bpy.ops.pose.select_all(action='DESELECT')
                bone.select = True
                bone.layers[0] = True
                bone.layers[10] = False
                
            if bone.name == "breast *side* base.R" or bone.name == "breast right base":
                bpy.ops.pose.select_all(action='DESELECT')
                bone.select = True
                bone.layers[0] = True
                bone.layers[10] = False
                
            if "adj" in bone.name.lower():
                bpy.ops.pose.select_all(action='DESELECT')
                bone.select = True
                bone.layers[11] = True
                bone.layers[0] = False

            bpy.ops.object.mode_set(mode='OBJECT')
            
        return {"FINISHED"}


class ARMATURE_OT_add_rig_shapes(bpy.types.Operator):
    """add custom rig shapes"""
    bl_idname = "armature.add_rig_shapes"
    bl_label = "add custom rig shapes"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        file_path = 'G:/3D/CONTENT/BLENDER/ASSETS/Rig shapes/XPS_Custom_RigShapes.blend'
        inner_path = 'Collection'
        object_name = 'custom_rig_shapes'

        bpy.ops.wm.append(
            filepath=os.path.join(file_path, inner_path, object_name),
            directory=os.path.join(file_path, inner_path),
            filename=object_name
            )


        armature_obj = bpy.context.active_object
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.armature.select_all(action='SELECT')

        bones = bpy.context.selected_bones
        
        for bone in bones:
            if bone.name == "head eyelid upper *side*.R":
                bone_head = bone.head
                bone.tail = bone_head + Vector((0,0,0.02))
            if bone.name == "head eyeball *side*.R":
                bone_head = bone.head
                bone.tail = bone_head + Vector((0,0,0.02))
            if bone.name == "head eyelid upper *side*.L":
                bone_head = bone.head
                bone.tail = bone_head + Vector((0,0,0.02))
            if bone.name == "head eyeball *side*.L":
                bone_head = bone.head
                bone.tail = bone_head + Vector((0,0,0.02))
                
        bpy.ops.object.mode_set(mode='POSE')
        bones = bpy.context.selected_pose_bones
        
        for bone in bones:
            if bone.name == "head eyeball *side*.R":
                eyeball_R_head = bone.head
                eyeball_R_tail = bone.tail
            if bone.name == "head eyeball *side*.L":
                eyeball_L_head = bone.head
                eyeball_L_tail = bone.tail
                
        bpy.ops.object.mode_set(mode='EDIT')

        eye_R_bone = armature_obj.data.edit_bones.new('eye.R')
        eye_L_bone = armature_obj.data.edit_bones.new('eye.L')
        eyes_bone = armature_obj.data.edit_bones.new('eyes')

        eye_R_bone.tail = eyeball_R_tail
        eye_R_bone.head = eyeball_R_head
        eye_R_bone.tail = eye_R_bone.tail + Vector((0,-0.1,0))
        eye_R_bone.head = eye_R_bone.head + Vector((0,-0.1,0))

        eye_L_bone.tail = eyeball_L_tail
        eye_L_bone.head = eyeball_L_head
        eye_L_bone.tail = eye_L_bone.tail + Vector((0,-0.1,0))
        eye_L_bone.head = eye_L_bone.head + Vector((0,-0.1,0))

        eyes_bone.tail = (eye_L_bone.tail + eye_R_bone.tail) / 2
        eyes_bone.head = (eye_L_bone.head + eye_R_bone.head) / 2

        bpy.ops.object.mode_set(mode='POSE')

        armature_obj.data.bones.active = armature_obj.data.bones["head eyelid upper *side*.R"]
        active_bone = bpy.context.active_pose_bone
        active_bone.constraints.new("COPY_ROTATION")
        active_bone.constraints["Copy Rotation"].target = armature_obj
        active_bone.constraints["Copy Rotation"].subtarget = "head eyeball *side*.R"
        active_bone.constraints["Copy Rotation"].influence = 0.4

        armature_obj.data.bones.active = armature_obj.data.bones["head eyelid upper *side*.L"]
        active_bone = bpy.context.active_pose_bone
        active_bone.constraints.new("COPY_ROTATION")
        active_bone.constraints["Copy Rotation"].target = armature_obj
        active_bone.constraints["Copy Rotation"].subtarget = "head eyeball *side*.L"
        active_bone.constraints["Copy Rotation"].influence = 0.4

        armature_obj.data.bones.active = armature_obj.data.bones["head eyeball *side*.R"]
        active_bone = bpy.context.active_pose_bone
        bpy.ops.pose.constraint_add(type='TRACK_TO')
        active_bone.constraints["Track To"].target = armature_obj
        active_bone.constraints["Track To"].subtarget = "eye.R"
        active_bone.constraints["Track To"].track_axis = 'TRACK_Z'

        armature_obj.data.bones.active = armature_obj.data.bones["head eyeball *side*.L"]
        active_bone = bpy.context.active_pose_bone
        bpy.ops.pose.constraint_add(type='TRACK_TO')
        active_bone.constraints["Track To"].target = armature_obj
        active_bone.constraints["Track To"].subtarget = "eye.L"
        active_bone.constraints["Track To"].track_axis = 'TRACK_Z'

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.armature.select_all(action='SELECT')

        bones = bpy.context.selected_bones
        for bone in bones:
            if bone.name == "eye.R":
                bone.parent = armature_obj.data.edit_bones["eyes"]
            if bone.name == "eye.L":
                bone.parent = armature_obj.data.edit_bones["eyes"]
            if bone.name == "eyes":
                bone.parent = armature_obj.data.edit_bones["head neck upper"]
                
        bpy.ops.object.mode_set(mode='POSE')

        armature_obj.data.bones.active = armature_obj.data.bones["eyes"]
        active_bone = bpy.context.active_pose_bone
        active_bone.custom_shape = bpy.data.objects["rig_shape eyes"]
        active_bone.custom_shape_scale_xyz[1] = 40
        active_bone.custom_shape_scale_xyz[2] = 40
        active_bone.custom_shape_scale_xyz[0] = 40

        armature_obj.data.bones.active = armature_obj.data.bones["eye.R"]
        active_bone = bpy.context.active_pose_bone
        active_bone.custom_shape = bpy.data.objects["rig_shape circle"]
        active_bone.custom_shape_scale_xyz[1] = 0.7
        active_bone.custom_shape_scale_xyz[2] = 0.7
        active_bone.custom_shape_scale_xyz[0] = 0.7
        active_bone.custom_shape_translation[0] = -0.01

        armature_obj.data.bones.active = armature_obj.data.bones["eye.L"]
        active_bone = bpy.context.active_pose_bone
        active_bone.custom_shape = bpy.data.objects["rig_shape circle"]
        active_bone.custom_shape_scale_xyz[1] = 0.7
        active_bone.custom_shape_scale_xyz[2] = 0.7
        active_bone.custom_shape_scale_xyz[0] = 0.7
        active_bone.custom_shape_translation[0] = 0.01

        for bone in armature_obj.data.bones:
            if bone.name == "head eyelid upper *side*.R":
                bpy.ops.pose.select_all(action='DESELECT')
                bone.select = True
                bone.layers[8] = True
                bone.layers[0] = False
                
            if bone.name == "head eyelid upper *side*.L":
                bpy.ops.pose.select_all(action='DESELECT')
                bone.select = True
                bone.layers[8] = True
                bone.layers[0] = False
            
            if bone.name == "head eyeball *side*.R":
                bpy.ops.pose.select_all(action='DESELECT')
                bone.select = True
                bone.layers[8] = True
                bone.layers[0] = False
            
            if bone.name == "head eyeball *side*.L":
                bpy.ops.pose.select_all(action='DESELECT')
                bone.select = True
                bone.layers[8] = True
                bone.layers[0] = False
                
        bpy.ops.pose.select_all(action='SELECT')

        for bone in bpy.context.selected_pose_bones:
            
            if bone.name == "root ground":
                bone.custom_shape = bpy.data.objects["rig_shape root square"]
                bone.custom_shape_scale_xyz[0] = 35
                bone.custom_shape_scale_xyz[1] = 35
                bone.custom_shape_scale_xyz[2] = 35
            if bone.name == "root hips":
                bone.custom_shape = bpy.data.objects["rig_shape torso"]
                bone.custom_shape_scale_xyz[0] = 5
                bone.custom_shape_scale_xyz[1] = 5
                bone.custom_shape_scale_xyz[2] = 5
                bone.custom_shape_rotation_euler[0] = 1.5708
            
            if bone.name == "head neck lower":
                bone.custom_shape = bpy.data.objects["rig_shape circle"]
                bone.custom_shape_rotation_euler[0] = 1.5708
                bone.custom_shape_translation[1] = 0.03
            if bone.name == "head neck upper":
                bone.custom_shape = bpy.data.objects["rig_shape circle"]
                bone.custom_shape_rotation_euler[0] = 1.5708
                bone.custom_shape_scale_xyz[0] = 1.5
                bone.custom_shape_scale_xyz[1] = 1.5
                bone.custom_shape_scale_xyz[2] = 1.5
                bone.custom_shape_translation[1] = 0.1
            
            if bone.name == "spine upper":
                bone.custom_shape = bpy.data.objects["rig_shape circle"]
                bone.custom_shape_rotation_euler[0] = 1.5708
            if bone.name == "spine lower":
                bone.custom_shape = bpy.data.objects["rig_shape circle"]
                bone.custom_shape_rotation_euler[0] = 1.5708
                bone.custom_shape_scale_xyz[0] = 1.35
                bone.custom_shape_scale_xyz[1] = 1.35
                bone.custom_shape_scale_xyz[2] = 1.35
            if bone.name == "pelvis":
                bone.custom_shape = bpy.data.objects["rig_shape hips"]
                bone.custom_shape_rotation_euler[0] = 2.35619
                bone.custom_shape_scale_xyz[0] = 13
                bone.custom_shape_scale_xyz[1] = 13
                bone.custom_shape_scale_xyz[2] = 13
                bone.custom_shape_translation[1] = 0.05
                
            if bone.name == "arm right shoulder 1" or bone.name == "arm *side* shoulder 1.R":
                bone.custom_shape = bpy.data.objects["rig_shape shoulder"]
                bone.custom_shape_rotation_euler[0] = 1.5708
                bone.custom_shape_rotation_euler[2] = 1.5708
                bone.custom_shape_scale_xyz[0] = 20
                bone.custom_shape_scale_xyz[1] = 20
                bone.custom_shape_scale_xyz[2] = 20
                bone.custom_shape_translation[1] = 0.07
                bone.custom_shape_translation[2] = 0.03
            if bone.name == "arm left shoulder 1" or bone.name == "arm *side* shoulder 1.L":
                bone.custom_shape = bpy.data.objects["rig_shape shoulder"]
                bone.custom_shape_rotation_euler[0] = 1.5708
                bone.custom_shape_rotation_euler[2] = 1.5708
                bone.custom_shape_scale_xyz[0] = 20
                bone.custom_shape_scale_xyz[1] = 20
                bone.custom_shape_scale_xyz[2] = 20
                bone.custom_shape_translation[1] = 0.07
                bone.custom_shape_translation[2] = 0.03
            
            if bone.name == "arm right shoulder 2" or bone.name == "arm *side* shoulder 2.R":
                bone.custom_shape = bpy.data.objects["rig_shape circle"]
                bone.custom_shape_rotation_euler[0] = 1.5708
                bone.custom_shape_scale_xyz[0] = 0.3
                bone.custom_shape_scale_xyz[1] = 0.3
                bone.custom_shape_scale_xyz[2] = 0.3
                bone.custom_shape_translation[1] = 0.15
            if bone.name == "arm left shoulder 2" or bone.name == "arm *side* shoulder 2.L":
                bone.custom_shape = bpy.data.objects["rig_shape circle"]
                bone.custom_shape_rotation_euler[0] = 1.5708
                bone.custom_shape_scale_xyz[0] = 0.3
                bone.custom_shape_scale_xyz[1] = 0.3
                bone.custom_shape_scale_xyz[2] = 0.3
                bone.custom_shape_translation[1] = 0.15
            if bone.name == "arm right elbow" or bone.name == "arm *side* elbow.R":
                bone.custom_shape = bpy.data.objects["rig_shape circle"]
                bone.custom_shape_rotation_euler[0] = 1.5708
                bone.custom_shape_scale_xyz[0] = 0.3
                bone.custom_shape_scale_xyz[1] = 0.3
                bone.custom_shape_scale_xyz[2] = 0.3
                bone.custom_shape_translation[1] = 0.12
            if bone.name == "arm left elbow" or bone.name == "arm *side* elbow.L":
                bone.custom_shape = bpy.data.objects["rig_shape circle"]
                bone.custom_shape_rotation_euler[0] = 1.5708
                bone.custom_shape_scale_xyz[0] = 0.3
                bone.custom_shape_scale_xyz[1] = 0.3
                bone.custom_shape_scale_xyz[2] = 0.3
                bone.custom_shape_translation[1] = 0.12
            if bone.name == "arm right wrist" or bone.name == "arm *side* wrist.R":
                bone.custom_shape = bpy.data.objects["rig_shape circle"]
                bone.custom_shape_rotation_euler[0] = 1.5708
                bone.custom_shape_scale_xyz[0] = 0.3
                bone.custom_shape_scale_xyz[1] = 0.3
                bone.custom_shape_scale_xyz[2] = 0.3
                bone.custom_shape_translation[1] = 0.02
            if bone.name == "arm left wrist" or bone.name == "arm *side* wrist.L":
                bone.custom_shape = bpy.data.objects["rig_shape circle"]
                bone.custom_shape_rotation_euler[0] = 1.5708
                bone.custom_shape_scale_xyz[0] = 0.3
                bone.custom_shape_scale_xyz[1] = 0.3
                bone.custom_shape_scale_xyz[2] = 0.3
                bone.custom_shape_translation[1] = 0.02
            
            if bone.name == "leg right thigh" or bone.name == "leg *side* thigh.R":
                bone.custom_shape = bpy.data.objects["rig_shape circle"]
                bone.custom_shape_rotation_euler[0] = 1.5708
                bone.custom_shape_scale_xyz[0] = 0.3
                bone.custom_shape_scale_xyz[1] = 0.3
                bone.custom_shape_scale_xyz[2] = 0.3
                bone.custom_shape_translation[1] = 0.22
            if bone.name == "leg left thigh" or bone.name == "leg *side* thigh.L":
                bone.custom_shape = bpy.data.objects["rig_shape circle"]
                bone.custom_shape_rotation_euler[0] = 1.5708
                bone.custom_shape_scale_xyz[0] = 0.3
                bone.custom_shape_scale_xyz[1] = 0.3
                bone.custom_shape_scale_xyz[2] = 0.3
                bone.custom_shape_translation[1] = 0.22
            if bone.name == "leg right knee" or bone.name == "leg *side* knee.R":
                bone.custom_shape = bpy.data.objects["rig_shape circle"]
                bone.custom_shape_rotation_euler[0] = 1.5708
                bone.custom_shape_scale_xyz[0] = 0.3
                bone.custom_shape_scale_xyz[1] = 0.3
                bone.custom_shape_scale_xyz[2] = 0.3
                bone.custom_shape_translation[1] = 0.2
            if bone.name == "leg left knee" or bone.name == "leg *side* knee.L":
                bone.custom_shape = bpy.data.objects["rig_shape circle"]
                bone.custom_shape_rotation_euler[0] = 1.5708
                bone.custom_shape_scale_xyz[0] = 0.3
                bone.custom_shape_scale_xyz[1] = 0.3
                bone.custom_shape_scale_xyz[2] = 0.3
                bone.custom_shape_translation[1] = 0.2
            if bone.name == "leg right ankle" or bone.name == "leg *side* ankle.R":
                bone.custom_shape = bpy.data.objects["rig_shape circle"]
                bone.custom_shape_rotation_euler[0] = 1.5708
                bone.custom_shape_scale_xyz[0] = 0.6
                bone.custom_shape_scale_xyz[1] = 0.6
                bone.custom_shape_scale_xyz[2] = 0.6
                bone.custom_shape_translation[1] = 0.06
            if bone.name == "leg left ankle" or bone.name == "leg *side* ankle.L":
                bone.custom_shape = bpy.data.objects["rig_shape circle"]
                bone.custom_shape_rotation_euler[0] = 1.5708
                bone.custom_shape_scale_xyz[0] = 0.6
                bone.custom_shape_scale_xyz[1] = 0.6
                bone.custom_shape_scale_xyz[2] = 0.6
                bone.custom_shape_translation[1] = 0.06
            if bone.name == "leg right toes" or bone.name == "leg *side* toes.R":
                bone.custom_shape = bpy.data.objects["rig_shape circle"]
                bone.custom_shape_rotation_euler[0] = 1.5708
                bone.custom_shape_scale_xyz[0] = 0.4
                bone.custom_shape_scale_xyz[1] = 0.4
                bone.custom_shape_scale_xyz[2] = 0.4
                bone.custom_shape_translation[1] = 0.02
            if bone.name == "leg left toes" or bone.name == "leg *side* toes.L":
                bone.custom_shape = bpy.data.objects["rig_shape circle"]
                bone.custom_shape_rotation_euler[0] = 1.5708
                bone.custom_shape_scale_xyz[0] = 0.4
                bone.custom_shape_scale_xyz[1] = 0.4
                bone.custom_shape_scale_xyz[2] = 0.4
                bone.custom_shape_translation[1] = 0.02
                
            if bone.name == "breast right base" or bone.name == "breast *side* base.R":
                bone.custom_shape = bpy.data.objects["rig_shape circle"]
                bone.custom_shape_rotation_euler[0] = 1.5708
                bone.custom_shape_translation[1] = 0.1
            if bone.name == "breast left base" or bone.name == "breast *side* base.L":
                bone.custom_shape = bpy.data.objects["rig_shape circle"]
                bone.custom_shape_rotation_euler[0] = 1.5708
                bone.custom_shape_translation[1] = 0.1
            
            if bone.name == "leg right butt base" or bone.name == "leg *side* butt base.R":
                bone.custom_shape = bpy.data.objects["rig_shape circle"]
                bone.custom_shape_rotation_euler[0] = 1.5708
                bone.custom_shape_rotation_euler[2] = -1.0472
                bone.custom_shape_translation[0] = 0.06
                bone.custom_shape_translation[1] = 0.04
                bone.custom_shape_scale_xyz[0] = 0.7
                bone.custom_shape_scale_xyz[1] = 0.7
                bone.custom_shape_scale_xyz[2] = 0.7

            if bone.name == "leg left butt base" or bone.name == "leg *side* butt base.L":
                bone.custom_shape = bpy.data.objects["rig_shape circle"]
                bone.custom_shape_rotation_euler[0] = 1.5708
                bone.custom_shape_rotation_euler[2] = 1.0472
                bone.custom_shape_translation[0] = -0.06
                bone.custom_shape_translation[1] = 0.04
                bone.custom_shape_scale_xyz[0] = 0.7
                bone.custom_shape_scale_xyz[1] = 0.7
                bone.custom_shape_scale_xyz[2] = 0.7

        return {"FINISHED"}


class VIEW3D_PT_xps_fixes(bpy.types.Panel):
    bl_idname = "xps_fixes"
    bl_label = "XPS Fixes"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "XPS"
    bl_context = 'objectmode'
    
    def draw(self, context):
        col = self.layout.column(align=True)
        col.label(text='Convert XPS to Principled')
        col.operator("material.xps_to_principled", text= "XPS to Principled")
        # col space
        col = self.layout.column(align=True)
        col.label(text='Convert Alpha Blend to Hashed')
        col.operator("material.fix_blendmode", text= "Non-Opaque to Hashed")
        # col space
        col = self.layout.column(align=True)
        col.label(text='Change all blend modes')
        col.operator("material.opaque_blendmode", text= "Opaque")
        col.operator("material.alhpa_blend_blendmode", text= "Alpha Blend")
        col.operator("material.alpha_hashed_blendmode", text= "Alpha Hashed")
        col.operator("material.alpha_clip_blendmode", text= "Alpha Clip")
        # col space
        col = self.layout.column(align=True)
        col.label(text='Bones Fixes')
        col.operator("armature.fix_bone_layers", text= "Fix bones layers")
        col.operator("armature.add_rig_shapes", text= "Add custom rig")
    

def register():
    bpy.utils.register_class(MATERIAL_OT_xps_to_principled)
    bpy.utils.register_class(MATERIAL_OT_fix_blendmode)
    bpy.utils.register_class(MATERIAL_OT_all_opaque)
    bpy.utils.register_class(MATERIAL_OT_all_blend)
    bpy.utils.register_class(MATERIAL_OT_all_hashed)
    bpy.utils.register_class(MATERIAL_OT_all_clip)
    bpy.utils.register_class(ARMATURE_OT_fix_bone_layers)
    bpy.utils.register_class(ARMATURE_OT_add_rig_shapes)
    bpy.utils.register_class(VIEW3D_PT_xps_fixes)
    
def unregister():
    bpy.utils.unregister_class(MATERIAL_OT_xps_to_principled)
    bpy.utils.unregister_class(MATERIAL_OT_fix_blendmode)
    bpy.utils.unregister_class(MATERIAL_OT_all_opaque)
    bpy.utils.unregister_class(MATERIAL_OT_all_blend)
    bpy.utils.unregister_class(MATERIAL_OT_all_hashed)
    bpy.utils.unregister_class(MATERIAL_OT_all_clip)
    bpy.utils.unregister_class(ARMATURE_OT_fix_bone_layers)
    bpy.utils.unregister_class(ARMATURE_OT_add_rig_shapes)
    bpy.utils.unregister_class(VIEW3D_PT_xps_fixes)