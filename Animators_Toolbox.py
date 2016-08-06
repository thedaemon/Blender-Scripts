##  Thanks to Frankie Hobbins, Joel Daniels, Julien Duroure, Hjalti Hjalmarsson, Bassam Kurdali, Luciano Munoz, Cristian Hasbun and anyone that I left out!
# Latest update: adding Advanced Boomsmash

bl_info = {
    "name": "Animator's Toolbox",
    "description": "A set of tools specifically for animators.",
    "author": "Brandon Ayers (thedaemon)",
    "version": (0, 3),
    "blender": (2, 77, 0),
    "location": "View3D > Toolbar > Animation > Animator's Toolbox",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "https://github.com/thedaemon/Blender-Scripts",
    "tracker_url": "https://github.com/thedaemon/Blender-Scripts/issues",
    "support": "TESTING",
    "category": "Animation"
    }

import os.path
import bpy
from bpy.props import *
from bpy.types import Operator

KEYMAPS = list()

# FEATURE: Jump forward/backward every N frames. Currently hardcoded variable.
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

# FEATURE: A toggle to keep the animator from selecting something other than the Armature.
class ToggleSelectability(bpy.types.Operator):
    """Turns off selection for all objects leaving only Armatures selectable"""
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

# Useless because blender already has this freaking command but I programmed it anyways. I may use it for specific axis template.
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

# FEATURE: A toggle for OpenSubdiv on all objects in scene with a Subdivision Surface Modifier.
class ToggleOpensubdiv(bpy.types.Operator):
    """Toggles OpenSubdiv for all Objects for improved animation playback speed"""
    bl_idname = "mesh.opensubdiv"
    bl_label = "Mesh OpenSubdiv"
    # Does nothing, testing.
    my_bool = bpy.props.BoolProperty(name="Toggle Option")

    def execute(self,context):
        for mm in (m for o in bpy.context.scene.objects for m in o.modifiers if m.type=='SUBSURF'):
            if mm.use_opensubdiv == True:
                mm.use_opensubdiv = False
            else:
                if mm.use_opensubdiv == False:
                    mm.use_opensubdiv = True
        return{'FINISHED'}

# Feature: Turns OpenSubdiv on for all meshes with Subdivision Surface Modifiers for improved viewport performance.
class OpensubdivOn(bpy.types.Operator):
    bl_idname = "opensubdiv.on"
    bl_label = "OpenSubdiv On"
    
    def execute(self,context):
        for mm in (m for o in bpy.context.scene.objects for m in o.modifiers if m.type=='SUBSURF'):
            mm.use_opensubdiv = True
        return{'FINISHED'}

# Feature: Turns OpenSubdiv on for all meshes with Subdivision Surface Modifiers for improved viewport performance.
class OpensubdivOff(bpy.types.Operator):
    bl_idname = "opensubdiv.off"
    bl_label = "OpenSubdiv Off"
    
    def execute(self,context):
        for mm in (m for o in bpy.context.scene.objects for m in o.modifiers if m.type=='SUBSURF'):
            mm.use_opensubdiv = False
        return{'FINISHED'}

# FEATURE: Simple X-Ray toggle for Armature
class ToggleXray(bpy.types.Operator):
    """Toggles X-Ray mode for bones"""
    bl_idname = "bone.togglexray"
    bl_label = "Armature X-Ray"

    def execute(self, context):
        for obj in bpy.data.objects:
            if obj.type == 'ARMATURE':
                obj.show_x_ray = not obj.show_x_ray
        return{'FINISHED'}

        
# FEATURE: Advanced Boomsmash version 011 classes        
class BoomProps(bpy.types.PropertyGroup):

    global_toggle = BoolProperty(
        name = 'Global',
        description = 'Same boomsmash settings for all scenes in file.',
        default = False)

    #twm.image_settings = bpy.types.ImageFormatSettings(
    #                        bpy.context.scene.render.image_settings)

    #scene_cam = BoolProperty(
    #    name = 'Active Camera',
    #    description = 'Always renders from the active camera that's set in the Scene properties')

    incremental = BoolProperty(
        name = 'Incremental',
        description = 'Save incremental boomsmashes.',
        default = False)

    use_stamp = BoolProperty(
        name = 'Stamp',
        description = 'Turn on stamp (uses settings from render properties).',
        default = False)    
        
    transparent = BoolProperty(
        name = 'Transparent',
        description = 'Make background transparent (only for formats that support alpha, i.e.: .png).',
        default = False)
        
    autoplay = BoolProperty(
        name = 'Autoplay',
        description = 'Automatically play boomsmash after making it.',
        default = False)              
        
    unsimplify = BoolProperty(
        name = 'Unsimplify',
        description = "Boomsmash with the subdivision surface levels at it's render settings.",
        default = False)
        
    onlyrender = BoolProperty(
        name = 'Only Render',
        description = 'Only have renderable objects visible during boomsmash.',
        default = False)
        
    frame_skip = IntProperty(
        name = 'Skip Frames',
        description = 'Number of frames to skip',
        default = 0,
        min = 0)        

    resolution_percentage = IntProperty(
        name = 'Resolution Percentage',
        description = 'define a percentage of the Render Resolution to make your boomsmash',
        default = 50,
        min = 0,
        max = 100)        

    #DEBUG
    #pu.db

    dirname = StringProperty(
        name = '',
        description = 'Folder where your boomsmash will be stored',
        default = bpy.app.tempdir,
        subtype = 'DIR_PATH')  

    filename = StringProperty(
        name = '',
        description = 'Filename where your boomsmash will be stored',
        default = 'Boomsmash',
        subtype = 'FILE_NAME')          
# BOOMSMASH
class setDirname(bpy.types.Operator):
    bl_idname = 'bs.setdirname'
    bl_label = 'BoomsmashDirname'
    bl_description = 'boomsmash use blendfile directory'
    bl_options = {'REGISTER', 'INTERNAL'}
    
    def execute(self, context):
        cs = context.scene
        cs.boom_props.dirname = os.path.dirname(bpy.data.filepath)
        return {'FINISHED'} 
# BOOMSMASH
class setFilename(bpy.types.Operator):
    bl_idname = 'bs.setfilename'
    bl_label = 'BoomsmashFilename'
    bl_description = 'boomsmash use blendfile name _ scene name'
    bl_options = {'REGISTER', 'INTERNAL'}
    
    def execute(self, context):
        cs = context.scene
        blend_name = os.path.basename(
                      os.path.splitext(bpy.data.filepath)[0])
        cs.boom_props.filename = blend_name + '_' + bpy.context.scene.name
        return {'FINISHED'} 
# BOOMSMASH
class DoBoom(bpy.types.Operator):
    bl_idname = 'bs.doboom'
    bl_label = 'Boomsmash'
    bl_description = 'Start boomsmash, use, enjoy, think about donate ;)'
    bl_options = {'REGISTER'}

    def execute(self, context): 
        cs = context.scene
        wm = context.window_manager
        rd = context.scene.render
        sd = context.space_data

        if wm.boom_props.global_toggle:
            boom_props = wm.boom_props
        else:
            boom_props = cs.boom_props

        #pu.db
        #guardo settings
        old_use_stamp = rd.use_stamp
        old_onlyrender = sd.show_only_render
        old_simplify = rd.use_simplify 
        old_filepath = rd.filepath
        old_alpha_mode = rd.alpha_mode
        #old_image_settings = rd.image_settings
        old_resolution_percentage = rd.resolution_percentage
        old_frame_step = cs.frame_step
        #afecto settings originales
        rd.use_stamp = boom_props.use_stamp
        sd.show_only_render = boom_props.onlyrender
        if boom_props.unsimplify:
            rd.use_simplify = False
        rd.filepath = cs.boom_props.dirname + cs.boom_props.filename
        rd.alpha_mode = 'TRANSPARENT' if boom_props.transparent else 'SKY'
        #rd.image_settings = boom_props.image_settings
        rd.resolution_percentage = boom_props.resolution_percentage
        cs.frame_step = boom_props.frame_skip + 1
        #view_pers = context.area.spaces[0].region_3d.view_perspective
        #if boom_props.scene_cam and view_pers is not 'CAMERA':
        #    bpy.ops.view3d.viewnumpad(type = 'CAMERA')
        #ejecuto
        bpy.ops.render.opengl(animation = True)
        if boom_props.autoplay:
            bpy.ops.render.play_rendered_anim()
        #devuelvo settings
        rd.use_stamp = old_use_stamp
        sd.show_only_render = old_onlyrender
        rd.use_simplify = old_simplify
        rd.filepath = old_filepath
        rd.alpha_mode = old_alpha_mode
        #rd.image_settings = old_image_settings
        rd.resolution_percentage = old_resolution_percentage
        context.scene.frame_step = old_frame_step
        #if boom_props.scene_cam and view_pers is not 'CAMERA':
        #    bpy.ops.view3d.viewnumpad(type = 'CAMERA')    
        return {'FINISHED'}


## UI ##
from bpy.types import PropertyGroup, Panel
from bpy.props import *

class animatorstoolboxData(PropertyGroup):
    bl_idname = 'animatorstoolboxDataUI'
    """
    UI property group for the add-on  WORK IN PROGRESS

    Options to adjust how the panel is displayed.

    bpy > types > WindowManager > animatorstoolboxDataUI
    bpy > context > window_manager > animatorstoolboxDataUI
    """
    displayMode = BoolProperty(name='Display Mode', description="Use this to hi"
                               "de many of the options below that are generally"
                               " needed while rigging. (Useful for animating.)",
                               default=False)
    boomsmashOptions = BoolProperty(name='Deform Options', description="Display th"
                                 "e deform options for this bone.",
                                 default=False)
# Animator's Toolbox Main Panel
def draw_animatorstoolbox_panel(context, layout):
#--Defining shortcuts for commands
    obj = context.object
    userpref = context.user_preferences
    obj = context.object
    edit = userpref.edit
    toolsettings = context.tool_settings
    scene = context.scene
    screen = context.screen
    rd = scene.render
    cscene = scene.cycles
#--Keying
    col = layout.column(align=True)
    col.label(text="Keyframes:")
    row = layout.row(align=True)
    row.prop(toolsettings, "use_keyframe_insert_auto", text="", toggle=True)
    if toolsettings.use_keyframe_insert_auto:
        row.prop(toolsettings, "use_keyframe_insert_keyingset", text="", toggle=True)
        if screen.is_animation_playing:
            subsub = row.row()
            subsub.prop(toolsettings, "use_record_with_nla", toggle=True)
    row.prop_search(scene.keying_sets_all, "active", scene, "keying_sets_all", text="")
    row.operator("screen.animation_play", text="", icon='PLAY')
    row.operator("screen.keyframe_jump", text="", icon='PREV_KEYFRAME').next = False
    row.operator("screen.keyframe_jump", text="", icon='NEXT_KEYFRAME').next = True    
#--Pose Tools
    col = layout.column(align=True)
    col.label(text="Pose:")
    row = col.row(align=True)
    row.operator("pose.copy", text="Copy")
    row.operator("pose.paste", text="Paste")
    row.operator("pose.paste", text="Flipped").flipped = True
    col = layout.column(align=True)
    row = col.row(align=True)
    row.operator("pose.breakdown", text="Breakdowner")
    row.operator("pose.push", text="Push")
    row.operator("pose.relax", text="Relax")
    col = layout.column(align=True)
    row = col.row()
    row.prop(context.active_object.data, "use_auto_ik", text="Auto IK")
    row.prop(obj, "show_x_ray", text="X Ray")       
#--Reset Transforms
    col = layout.column(align=True)
    col.label(text="Reset Transforms:")
    row = layout.row(align=True)
    row.operator("pose.loc_clear", text="Location")
    row.operator("pose.rot_clear", text="Rotation")
    row.operator("pose.scale_clear", text="Scale")
    col = layout.column(align=True)
    row = col.row()
    row.operator("pose.transforms_clear", text="Reset All")
#--Optimizations
    col = layout.column(align=True)
    col.label(text="Optimizations:")
    #col.layout.column(align=True)
    #col.label(text="OpenSubdiv")
    row = layout.row(align=True)
    row.label(text="OpenSubdiv")
    row.operator("opensubdiv.on", text="On")
    row.operator("opensubdiv.off", text="Off")
    row = layout.row(align=True)
    row.operator("bone.toggleselectability", text="Select Armature Only")
#--Simplify
    col = layout.column(align=True)
    col.label(text="Simplify:")
    row = layout.row(align=True)
    row.prop(rd, "use_simplify", text="Use Simplify")
    #layout.active = rd.use_simplify
    split = layout.split()
    col = split.column()
    col.label(text="Viewport:")
    col.prop(rd, "simplify_subdivision", text="Subdivision")
    col.prop(rd, "simplify_child_particles", text="Child Particles")
    col = split.column()
    col.label(text="Render:")
    col.prop(rd, "simplify_subdivision_render", text="Subdivision")
    col.prop(rd, "simplify_child_particles_render", text="Child Particles")
    col = layout.column()
    col.prop(cscene, "use_camera_cull")
    subsub = col.column()
    subsub.active = cscene.use_camera_cull
    subsub.prop(cscene, "camera_cull_margin")        
#--Motion Path
    pchan = context.active_pose_bone
    mpath = pchan.motion_path if pchan else None
    col = layout.column(align=True)
    col.label(text="Motion Paths:")
    if mpath:
        row = col.row(align=True)
        row.operator("pose.paths_update", text="Update")
        row.operator("pose.paths_clear", text="", icon='X')
    else:
        col.operator("pose.paths_calculate", text="Calculate")
#--New Key Type
    col = layout.column(align=True)
    col.label(text="New Key Type:")
    col.prop(edit, "keyframe_new_interpolation_type", text='Keys')
    col.prop(edit, "keyframe_new_handle_type", text="Handles")

# Animator's ToolBox Draw Calls
class AnimatorsToolBox(bpy.types.Panel):
    """Creates a custom Animator Panel in the 3D View"""
    bl_label = "Animator's Toolbox"
    bl_idname = "ANIM_TOOLBOX"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Animation"
#--Header
    def draw_header(self, context):
        layout = self.layout
        #animatorstoolboxDataUIProps = context.window_manager.animatorstoolboxDataUI
        #layout.prop('animatorstoolboxDataUI', "displayMode", text="")
        DoBTN = self.layout
        DoBTN.operator('bs.doboom', text = '', icon = 'RENDER_ANIMATION')
#--Draw Toolboxes
    def draw(self, context):
        layout = self.layout
        #animatorstoolboxData = context.window_manager.animatorstoolboxDataUI
        draw_animatorstoolbox_panel(context, layout)
        draw_boomsmash_panel(context, layout)

# BOOMSMASH - copy to animators
def draw_boomsmash_panel(context, layout):
    col = layout.column(align = True)
    cs = context.scene
    wm = context.window_manager 
    rd = context.scene.render
    if wm.boom_props.global_toggle:
        boom_props = wm.boom_props
    else:
        boom_props = cs.boom_props
    col.label(text="BoomSmash:")
    col.operator('bs.doboom', text = 'BoomSmash', icon = 'RENDER_ANIMATION')
    split = col.split()
    subcol = split.column()
    #subcol.prop(boom_props, 'incremental')
    subcol.prop(boom_props, 'use_stamp')
    subcol.prop(boom_props, 'onlyrender')
    #subcol.prop(boom_props, 'scene_cam')
    subcol = split.column()
    subcol.prop(boom_props, 'transparent')
    subcol.prop(boom_props, 'autoplay')
    subcol.prop(boom_props, 'unsimplify')
    col.separator()
    col.label(text = 'Use preview range:')
    sub = col.split()
    subrow = sub.row(align = True)
    subrow.prop(context.scene, 'use_preview_range', text = '')
    subrow.prop(context.scene, 'frame_preview_start', text = 'Start')
    subrow.prop(boom_props, 'frame_skip', text = 'Skip')
    subrow.prop(context.scene, 'frame_preview_end', text = 'End')
    col.separator()
    final_res_x = (rd.resolution_x * boom_props.resolution_percentage) / 100
    final_res_y = (rd.resolution_y * boom_props.resolution_percentage) / 100
    col.label(text = 'Final Resolution: {} x {}'.format(str(final_res_x)[:-2], str(final_res_y)[:-2]))
    col.prop(boom_props, 'resolution_percentage', slider = True )
    col.separator()
    #col.label(text = 'Output Format:')
    #col.template_image_settings(wm.image_settings, color_management = False)
    col.label(text = 'boomsmash folder:')
    row = col.row()
    row.prop(cs.boom_props, 'dirname')
    row.operator('bs.setdirname', text = '', icon = 'FILE_FOLDER')
    col.separator()
    col.label(text = 'boomsmash filename:')
    row = col.row()
    row.prop(cs.boom_props, 'filename')
    row.operator('bs.setfilename', text = '', icon = 'FILE_BLEND')
    

def register():
    # This command is supposed to register EVERYTHING, are you kidding me that it's that easy?
    bpy.utils.register_module(__name__)
    #bpy.utils.register_class(AnimatorsToolboxFrameJump)
    #bpy.utils.register_class(ToggleSelectability)
    #bpy.utils.register_class(ClearAllTransforms)
    #bpy.utils.register_class(AnimatorsToolBox)
    #bpy.utils.register_class(ToggleOpensubdiv)
    #bpy.utils.register_class(OpensubdivOff)
    #bpy.utils.register_class(OpensubdivOn)
    #bpy.utils.register_class(ToggleXray)
#---Boomsmash
    bpy.types.Scene.boom_props = PointerProperty(
            type = BoomProps, name = 'BoomSmash Properties', description = '')

    bpy.types.WindowManager.boom_props = PointerProperty(
            type = BoomProps, name = 'BoomSmash Global Properties', description = '')    
#---    
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
    bpy.utils.unregister_module(__name__)
    #bpy.utils.unregister_class(AnimatorsToolboxFrameJump)
    #bpy.utils.unregister_class(ToggleSelectability)
    #bpy.utils.unregister_class(ClearAllTransforms)
    #bpy.utils.unregister_class(AnimatorsToolBox)
    #bpy.utils.unregister_class(ToggleOpensubdiv)
    #bpy.utils.unregister_class(OpensubdivOff)
    #bpy.utils.unregister_class(OpensubdivOn)
    #bpy.utils.unregister_class(ToggleXray)
#---Boomsmash
    del bpy.types.Scene.boom_props
    del bpy.types.WindowManager.boom_props
#---
    for km, kmi in KEYMAPS:
        km.keymap_items.remove(kmi)
    KEYMAPS.clear()

# The End
if __name__ == "__main__":
    register()