###########################################
# thedaemon's custom animation panel
# Thanks to Frankie Hobbins, Joel Daniels
###########################################

bl_info = {
    "name": "thedaemon's Animation Tools",
    "author": "Brandon Ayers aka (thedaemon)",
    "version": (0, 2, 0),
    "blender": (2, 77, 0),
    "description": "Various animation tools.",
    "location": "View3D > Toolbar",
    "category": "Animation"
    }

import bpy
from bpy.props import *

########################
####### FUNCTIONS ######
########################


#######################
###### OPERATORS ######
#######################

class ToggleSelectability(bpy.types.Operator):
    """Toggles all scene object selectability leaving rig always selectable """
    bl_idname = "bone.toggleselectability"
    bl_label = "Armature Selection Only"

    def execute(self, context):
        do_i_hide_select = not bpy.context.active_object.hide_select
        if bpy.context.selected_objects == []:
            if bpy.context.object.type == "ARMATURE":
                for ob in bpy.context.scene.objects:
                    ob.hide_select = True
            else:
                for ob in bpy.context.scene.objects:
                    if ob.type != "ARMATURE":
                        ob.hide_select = do_i_hide_select
        else:
            if bpy.context.object.type == "ARMATURE":
                for ob in bpy.context.scene.objects:
                    if ob.type != "ARMATURE":
                        do_i_hide_select2 = not ob.hide_select
                        for ob in bpy.context.scene.objects:
                            ob.hide_select = do_i_hide_select2
                        break
                bpy.context.object.hide_select = False
            else:
                for ob in bpy.context.selected_objects:
                    ob.hide_select = not ob.hide_select
        return{'FINISHED'}
        
class ToggleXray(bpy.types.Operator):
    """Toggle Xray mode """
    bl_idname = "bone.togglexray"
    bl_label = "Armature X-Ray"

    def execute(self, context):
        for obj in bpy.data.objects:
            if obj.type == 'ARMATURE':
                obj.show_x_ray = not obj.show_x_ray
        return{'FINISHED'}

class AddFakeUsers(bpy.types.Operator):
    """Add Fake users to all actions to stop them getting deleted on save"""
    bl_idname = "bone.addfakeusers"
    bl_label = "Unused"

    def execute(self, context):
        for a in bpy.data.actions:
            a.use_fake_user=True
        return{'FINISHED'}

class RemoveFakeUsers(bpy.types.Operator):
    """Remove Fake users from all actions to help them getting removed on save"""
    bl_idname = "bone.removefakeusers"
    bl_label = "Unused"

    def execute(self, context):
        for a in bpy.data.actions:
            a.user_clear()
            a.use_fake_user=False
        return{'FINISHED'}
        
################
###### UI ######
################
        
class thedaemonsAnimationTools(bpy.types.Panel):
    """Creates a custom rigging Panel in the 3D View"""
    # The header of the panel
    bl_label = "thedaemon's Animation Tools"
    bl_idname = "POSE_PT_thedaemon"
    # This is where the panel is located. Currently in the 3d viewport, view_3d
    bl_space_type = 'VIEW_3D'
    # This places it in the left Tools Menu.
    bl_region_type = 'TOOLS'
    # This is the Tab that the panel is located.
    bl_category = "Animation"
    # This limits the panel to the listed context. IE it won't show up unless you are in this mode!
    #bl_context = "posemode"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        col = layout.column(align=True)
        col.label(text="Selection and visibility")
        row = layout.row(align=True)
        row.operator("bone.togglexray", text="X-Ray")
        row = layout.row(align=True)
        row.operator("bone.toggleselectability", text="Selectability")
        row = layout.row(align=True)
        row.prop(obj, "hide", text="hide object")
        row.prop(obj, "hide_select", text="hide select")
        row.prop(context.object, "hide_render")

######################
###### REGISTER ######
######################

def register():

    bpy.utils.register_class(AddFakeUsers)
    bpy.utils.register_class(RemoveFakeUsers)
    bpy.utils.register_class(ToggleSelectability)
    bpy.utils.register_class(ToggleXray)
    bpy.utils.register_class(thedaemonsAnimationTools)

def unregister():

    bpy.utils.unregister_class(AddFakeUsers)
    bpy.utils.unregister_class(RemoveFakeUsers)
    bpy.utils.unregister_class(ToggleSelectability)
    bpy.utils.unregister_class(ToggleXray)
    bpy.utils.unregister_class(thedaemonsAnimationTools)

if __name__ == "__main__":
    register()  
