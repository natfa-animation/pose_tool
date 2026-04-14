from typing import TYPE_CHECKING

import bpy  # type: ignore[import-not-found]
import json
from bpy_extras.io_utils import ExportHelper, ImportHelper  # type: ignore[import-not-found]
import os

from bpy.props import StringProperty  # type: ignore[import-not-found]


class PT_OT_ExportPoses(bpy.types.Operator, ExportHelper):
    bl_idname = "pt.export_poses"
    bl_label = "Export Poses"
    bl_description = "Export poses and groups to a JSON file"
    filename_ext = ".json"
    
    def execute(self, context):
        armature = context.scene.sim_pt_selected_armature if context.scene.sim_pt_selected_armature else context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature")
            return {'CANCELLED'}
        data = {"poses": [], "groups": []}
        for pose in armature.data.sim_pt_poses:
            pose_dict = {
                "name": pose.name,
                "group_name": pose.group_name,
                "is_mirrored": pose.is_mirrored,
                "bone_poses": [
                    {
                        "bone_name": bd.bone_name,
                        "target_rotation_x": bd.target_rotation_x,
                        "target_rotation_y": bd.target_rotation_y,
                        "target_rotation_z": bd.target_rotation_z,
                        "target_quat_w": bd.target_quat_w,
                        "target_quat_x": bd.target_quat_x,
                        "target_quat_y": bd.target_quat_y,
                        "target_quat_z": bd.target_quat_z,
                        "rotation_mode": bd.rotation_mode,
                        "target_location_x": bd.target_location_x,
                        "target_location_y": bd.target_location_y,
                        "target_location_z": bd.target_location_z,
                        "target_scale_x": bd.target_scale_x,
                        "target_scale_y": bd.target_scale_y,
                        "target_scale_z": bd.target_scale_z,
                        "use_quaternion": bd.use_quaternion
                    } for bd in pose.bone_poses
                ]
            }
            data["poses"].append(pose_dict)
        for group in armature.data.sim_pt_pose_groups:
            group_dict = {
                "name": group.name,
                "parent_group": group.parent_group,
                "is_expanded": group.is_expanded
            }
            data["groups"].append(group_dict)
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            self.report({'INFO'}, f"Poses and groups exported to {self.filepath}")
            bpy.ops.ed.undo_push(message="Export poses")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to export poses: {str(e)}")
            return {'CANCELLED'}
        return {'FINISHED'}


class PT_OT_ImportPoses(bpy.types.Operator, ImportHelper):
    bl_idname = "pt.import_poses"
    bl_label = "Import Poses"
    bl_description = "Import poses and groups, replacing existing"
    filename_ext = ".json"
    
    def execute(self, context):
        armature = context.scene.sim_pt_selected_armature if context.scene.sim_pt_selected_armature else context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature")
            return {'CANCELLED'}
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            self.report({'ERROR'}, f"Failed to load JSON file: {str(e)}")
            return {'CANCELLED'}
        
        armature.data.sim_pt_poses.clear()
        armature.data.sim_pt_pose_groups.clear()
        for group_data in data.get("groups", []):
            new_group = armature.data.sim_pt_pose_groups.add()
            new_group.name = group_data.get("name", "Group")
            new_group.parent_group = group_data.get("parent_group", "")
            new_group.is_expanded = group_data.get("is_expanded", True)
        for pose_data in data.get("poses", []):
            new_pose = armature.data.sim_pt_poses.add()
            new_pose.name = pose_data.get("name", "Pose")
            new_pose.group_name = pose_data.get("group_name", "")
            new_pose.is_mirrored = pose_data.get("is_mirrored", False)
            for bd_data in pose_data.get("bone_poses", []):
                bone_data = new_pose.bone_poses.add()
                for key, value in bd_data.items():
                    if hasattr(bone_data, key):
                        setattr(bone_data, key, value)
        self.report({'INFO'}, f"Poses and groups imported from {self.filepath}")
        bpy.ops.ed.undo_push(message="Import poses")
        return {'FINISHED'}


class PT_OT_MergePoses(bpy.types.Operator, ImportHelper):
    bl_idname = "pt.merge_poses"
    bl_label = "Merge Poses"
    bl_description = "Merge poses and groups from a JSON file"
    filename_ext = ".json"
    
    def execute(self, context):
        armature = context.scene.sim_pt_selected_armature if context.scene.sim_pt_selected_armature else context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature")
            return {'CANCELLED'}
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            self.report({'ERROR'}, f"Failed to load JSON file: {str(e)}")
            return {'CANCELLED'}
        
        existing_groups = {g.name for g in armature.data.sim_pt_pose_groups}
        for group_data in data.get("groups", []):
            if group_data.get("name", "Group") not in existing_groups:
                new_group = armature.data.sim_pt_pose_groups.add()
                new_group.name = group_data.get("name", "Group")
                new_group.parent_group = group_data.get("parent_group", "")
                new_group.is_expanded = group_data.get("is_expanded", True)
        for pose_data in data.get("poses", []):
            new_pose = armature.data.sim_pt_poses.add()
            new_pose.name = pose_data.get("name", "Pose")
            new_pose.group_name = pose_data.get("group_name", "")
            new_pose.is_mirrored = pose_data.get("is_mirrored", False)
            for bd_data in pose_data.get("bone_poses", []):
                bone_data = new_pose.bone_poses.add()
                for key, value in bd_data.items():
                    if hasattr(bone_data, key):
                        setattr(bone_data, key, value)
        self.report({'INFO'}, f"Poses and groups merged from {self.filepath}")
        bpy.ops.ed.undo_push(message="Merge poses")
        return {'FINISHED'}


class PT_OT_LoadPreset(bpy.types.Operator):
    bl_idname = "pt.load_preset"
    bl_label = "Load Preset"
    bl_description = "Load a pose preset from the presets folder"
    if TYPE_CHECKING:
        preset_name: str
    else:
        __annotations__ = {"preset_name": StringProperty(name="Preset Name", default="")}

    def execute(self, context):
        armature = context.scene.sim_pt_selected_armature if context.scene.sim_pt_selected_armature else context.active_object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature")
            return {'CANCELLED'}
        presets_path = context.scene.sim_pt_presets_path
        preset_filepath = os.path.join(presets_path, self.preset_name)
        if not os.path.exists(preset_filepath):
            self.report({'ERROR'}, f"Preset file '{preset_filepath}' does not exist")
            return {'CANCELLED'}
        try:
            with open(preset_filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            armature.data.sim_pt_poses.clear()
            armature.data.sim_pt_pose_groups.clear()
            for group_data in data.get("groups", []):
                new_group = armature.data.sim_pt_pose_groups.add()
                new_group.name = group_data.get("name", "Group")
                new_group.parent_group = group_data.get("parent_group", "")
                new_group.is_expanded = group_data.get("is_expanded", True)
            for pose_data in data.get("poses", []):
                new_pose = armature.data.sim_pt_poses.add()
                new_pose.name = pose_data.get("name", "Pose")
                new_pose.group_name = pose_data.get("group_name", "")
                new_pose.is_mirrored = pose_data.get("is_mirrored", False)
                for bd_data in pose_data.get("bone_poses", []):
                    bone_data = new_pose.bone_poses.add()
                    for key, value in bd_data.items():
                        if hasattr(bone_data, key):
                            setattr(bone_data, key, value)
            self.report({'INFO'}, f"Preset '{self.preset_name}' loaded successfully")
            bpy.ops.ed.undo_push(message=f"Load preset '{self.preset_name}'")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to load preset: {str(e)}")
            return {'CANCELLED'}
        return {'FINISHED'}

