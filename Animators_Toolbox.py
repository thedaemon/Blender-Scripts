##############################################
##  thedaemon's Useful Animation Panel       #
##  Thanks to Frankie Hobbins, Joel Daniels, #
##  Julien Duroure, Hjalti Hjalmarsson,      #
##  Bassam Kurdali, Luciano Munoz            #
##############################################

bl_info = {
    "name": "Animator's Toolbox",
    "author": "Brandon Ayers aka thedaemon",
    "version": (0, 1, 5),
    "blender": (2, 77, 0),
    "description": "Various animation tools.",
    "location": "View3D > Toolbar > Animation",
    "category": "Animation"
    }

import bpy
from bpy.props import *

KEYMAPS = list()

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
    my_bool = bpy.props.BoolProperty(name="Toggle Option")

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

# FEATURE: Jump forward/backward every N frames
class AnimatorsToolboxFrameJump(bpy.types.Operator):

    """Jump a number of frames forward/backwards"""
    bl_idname = "screen.animatorstools_frame_jump"
    bl_label = "Jump Frames"

    forward = bpy.props.BoolProperty(default=True)

    def execute(self, context):
        scene = context.scene
        framedelta = 4
        if self.forward:
            scene.frame_current = scene.frame_current + framedelta
        else:
            scene.frame_current = scene.frame_current - framedelta

        return {"FINISHED"}

################
###### UI ######
################

class AnimatorsToolBox(bpy.types.Panel):
    """Creates a custom rigging Panel in the 3D View"""
    # The header of the panel
    bl_label = "Animator's Toolbox"
    bl_idname = "ANIM_TOOLBOX"
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
        #userpref = context.user_preferences
        #ob = context.object
        #edit = userpref.edit
        #oscon = context.scene.objects
        #toolsettings = context.tool_settings
        #scene = context.scene
        #screen = context.screen


#############################
        col = layout.column(align=True)
        col.label(text="Keying")
        row = layout.row(align=True)
        row.prop(context.tool_settings, "use_keyframe_insert_auto", text="", toggle=True)
        if context.tool_settings.use_keyframe_insert_auto:
            row.prop(context.tool_settings, "use_keyframe_insert_keyingset", text="", toggle=True)
            if context.screen.is_animation_playing:
                subsub = row.row()
                subsub.prop(context.tool_settings, "use_record_with_nla", toggle=True)
        row.prop_search(context.scene.keying_sets_all, "active", context.scene, "keying_sets_all", text="")
        row.operator("screen.animation_play", text="", icon='PLAY')
        row.operator("screen.keyframe_jump", text="", icon='PREV_KEYFRAME').next = False
        row.operator("screen.keyframe_jump", text="", icon='NEXT_KEYFRAME').next = True
###########################
        col = layout.column(align=True)
        col.label(text="In Betweens")
        row = col.row()
        row.operator("pose.breakdown", text="Breakdowner")
        row.operator("pose.push", text="Push")
        row.operator("pose.relax", text="Relax")
############################
        col = layout.column(align=True)
        col.label(text="Reset Transforms")
        ## This makes the buttons grouped
        row = layout.row(align=True)
        row.operator("pose.loc_clear", text="Location")
        row.operator("pose.rot_clear", text="Rotation")
        row.operator("pose.scale_clear", text="Scale")
        col = layout.column(align=True)
        row = col.row()
        row.operator("pose.transforms_clear", text="Reset All")

############################
        col.label(text="New Key Type")
        col = layout.column(align=True)
        col.prop(context.user_preferences.edit, "keyframe_new_interpolation_type", text='Keys')
        col.prop(context.user_preferences.edit, "keyframe_new_handle_type", text="Handles")
##############################
        col = layout.column(align=True)
        col.label(text="Optimization")
        #row = layout.row(align=True)
        ## This makes each button seperate
        row = col.row()
        row.operator("mesh.opensubdiv", text ="OpenSubdiv")
        row.prop(context.object, "show_x_ray", text="X-Ray")
        #row.prop("mesh.opensubdiv", text = "OpenSubdiv")
        col = layout.column(align=True)
        #row = col.row()
        #row = layout.row(align=True)
        #row.operator("bone.togglexray", text="X-Ray")

        row = layout.row(align=True)
        row.operator("bone.toggleselectability", text="Select Armature Only")
######################
###### REGISTER ######
######################

def register():

    bpy.utils.register_class(AddFakeUsers)
    bpy.utils.register_class(RemoveFakeUsers)
    bpy.utils.register_class(ToggleSelectability)
    bpy.utils.register_class(ToggleOpensubdiv)
    bpy.utils.register_class(ToggleXray)
    bpy.utils.register_class(ClearAllTransforms)
    bpy.utils.register_class(AnimatorsToolBox)
    bpy.utils.register_class(AnimatorsToolboxFrameJump)
    # register keyboard shortcuts for Frame Jump
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    km = kc.keymaps.new(name="Frames")
    kmi = km.keymap_items.new(
        "screen.animatorstools_frame_jump", "RIGHT_ARROW", "PRESS", shift=True)
    kmi.properties.forward = True
    KEYMAPS.append((km, kmi))
    kmi = km.keymap_items.new(
        "screen.animatorstools_frame_jump", "LEFT_ARROW", "PRESS", shift=True)
    kmi.properties.forward = False
    KEYMAPS.append((km, kmi))

def unregister():

    bpy.utils.unregister_class(AddFakeUsers)
    bpy.utils.unregister_class(RemoveFakeUsers)
    bpy.utils.unregister_class(ToggleSelectability)
    bpy.utils.unregister_class(ToggleOpensubdiv)
    bpy.utils.unregister_class(ToggleXray)
    bpy.utils.unregister_class(ClearAllTransforms)
    bpy.utils.unregister_class(AnimatorsToolBox)
    bpy.utils.unregister_class(AnimatorsToolboxFrameJump)
    for km, kmi in KEYMAPS:
        km.keymap_items.remove(kmi)
    KEYMAPS.clear()

if __name__ == "__main__":
    register()
