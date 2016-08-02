##############################################
##  thedaemon's Useful Animation Panel       #
##  Thanks to Frankie Hobbins, Joel Daniels, #
##  Julien Duroure, Hjalti Hjalmarsson,      #
##  Bassam Kurdali, Luciano Munoz            #
##############################################

bl_info = {
    "name": "Animator's Tool Kit",
    "author": "Brandon Ayers aka thedaemon",
    "version": (0, 2, 1),
    "blender": (2, 77, 0),
    "description": "Various animation tools.",
    "location": "View3D > Toolbar > Animation",
    "category": "Animation"
    }

import bpy
from bpy.props import *

#######################
###### OPERATORS ######
#######################

class ToggleSelectability(bpy.types.Operator):
    """Toggles selectability of all objects leaving only Armature Selectable"""
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

class ToggleOpensubdiv(bpy.types.Operator):
    """Toggles OpenSubdiv for all Objects for improved animation playback speed"""
    bl_idname = "mesh.opensubdiv"
    bl_label = "Mesh OpenSubdiv"
    
    def execute(self,context):
        for mm in (m for o in bpy.context.scene.objects for m in o.modifiers if m.type=='SUBSURF'):
            if mm.use_opensubdiv == True:
                mm.use_opensubdiv = False
            else:
                if mm.use_opensubdiv == False:
                    mm.use_opensubdiv = True
        return{'FINISHED'}

## USELESS BECAUSE BLENDER ALREADY HAS THIS FREAKING COMMAND            
class ClearAllTransforms(bpy.types.Operator):
    """Clears all transforms on the bone I hope"""
    bl_idname = "pose.clearall"
    bl_label = "Clear Transforms"
    
    def execute(self,context):
        for obj in bpy.data.objects:
            if obj.type == 'ARMATURE':
                bpy.ops.pose.rot_clear()
                bpy.ops.pose.loc_clear()
                bpy.ops.pose.scale_clear()
        return{'FINISHED'}
        
class ToggleXray(bpy.types.Operator):
    """Toggles X-Ray mode for bones"""
    bl_idname = "bone.togglexray"
    bl_label = "Armature X-Ray"

    def execute(self, context):
        for obj in bpy.data.objects:
            if obj.type == 'ARMATURE':
                obj.show_x_ray = not obj.show_x_ray
        return{'FINISHED'}
## CURRENTLY UNUSED BUT I WILL USE AT A LATER DATE
class AddFakeUsers(bpy.types.Operator):
    """Add Fake users to all actions to stop them getting deleted on save"""
    bl_idname = "bone.addfakeusers"
    bl_label = "Unused"

    def execute(self, context):
        for a in bpy.data.actions:
            a.use_fake_user=True
        return{'FINISHED'}
## CURENTELY UNUSED BUT I WILL USE AT A LATER DATE
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
        # Defining shortcuts for commands
        obj = context.object
        userpref = context.user_preferences
        edit = userpref.edit 

############################
        col = layout.column(align=True)
        col.label(text="Optimization")
        #row = layout.row(align=True)
        ## This makes each button seperate
        row = col.row()
        row.operator("mesh.opensubdiv", text ="OpenSubdiv")
        #row = layout.row(align=True)
        row.operator("bone.togglexray", text="X-Ray")
        #row = layout.row(align=True)
        row.operator("bone.toggleselectability", text="Selectability")
############################        
        col = layout.column(align=True)
        col.label(text="Visibility")
        ## This makes the buttons grouped
        row = layout.row(align=True)
        row.prop(obj, "hide", text="Object")
        row.prop(obj, "hide_select", text="Select")
        row.prop(context.object, "Render")
############################
        col = layout.column(align=True)
        col.label(text="Reset Transforms")
        row = layout.row(align=True)
        row.operator("pose.loc_clear", text="Location")
        row.operator("pose.rot_clear", text="Rotation")
        row.operator("pose.scale_clear", text="Scale")
        col = layout.column(align=True)
        row = col.row()
        row.operator("pose.transforms_clear", text="Reset All")
###########################        
        col = layout.column(align=True)
        col.label(text="Inbetween")
        row = col.row()
        row.operator("pose.breakdown", text="Breakdowner")        
        row.operator("pose.push", text="Push")
        row.operator("pose.relax", text="Relax")
############################        
        col.label(text="New Key Type")
        col = layout.column(align=True)
        col.prop(edit, "keyframe_new_interpolation_type", text='Keys')
        col.prop(edit, "keyframe_new_handle_type", text="Handles")
        
######################
###### REGISTER ######
######################

def register():

    bpy.utils.register_class(AddFakeUsers)
    bpy.utils.register_class(RemoveFakeUsers)
    bpy.utils.register_class(ToggleSelectability)
    bpy.utils.register_class(ToggleOpensubdiv)
    bpy.utils.register_class(ToggleXray)
    bpy.utils.register_class(thedaemonsAnimationTools)
    bpy.utils.register_class(ClearAllTransforms)

def unregister():

    bpy.utils.unregister_class(AddFakeUsers)
    bpy.utils.unregister_class(RemoveFakeUsers)
    bpy.utils.unregister_class(ToggleSelectability)
    bpy.utils.unregister_class(ToggleOpensubdiv)
    bpy.utils.unregister_class(ToggleXray)
    bpy.utils.unregister_class(thedaemonsAnimationTools)
    bpy.utils.unregister_class(ClearAllTransforms)

if __name__ == "__main__":
    register()  
