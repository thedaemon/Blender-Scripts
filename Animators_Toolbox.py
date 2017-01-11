#____________________________________________________________________________|
#  Thanks to Frankie Hobbins, Joel Daniels, Julien Duroure,
# Hjalti Hjalmarsson, Bassam Kurdali, Luciano Munoz, Cristian Hasbun,
# and anyone that I left out!
#
# Latest update: Rethinking the amount of tools and interface.
# Removed tools that are better left to hotkeys.
# Will add preferences of hotkeys later.
#     "support": "TESTING",
bl_info = {
    "name": "Animator's Toolbox",
    "description": "A set of tools specifically for animators.",
    "author": "Brandon Ayers (thedaemon)",
    "version": (0, 5, 1),
    "blender": (2, 78, 0),
    "location": "View3D > Toolbar > Animation > Animator's Toolbox",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "https://github.com/thedaemon/Blender-Scripts",
    "tracker_url": "https://github.com/thedaemon/Blender-Scripts/issues",
    "category": "Animation"
    }
import os.path
import bpy
from bpy.props import *
from bpy.types import Operator
KEYMAPS = list()

# FEATURE: Jump forward/backward every N frames. Currently hardcoded variable.
# the frame jump amount needs to be in preferences along with hotkey selector (viewer?)
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

# FEATURE: A toggle to keep the animator from selecting something other
# than the Armature.
class ToggleSelectability(bpy.types.Operator):
    """Turns off selection for all objects
    leaving only Armatures selectable"""
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
# Useless because blender already has this freaking command but I programmed
# it anyways. I may use it for specific axis template.
class ClearAllTransforms(bpy.types.Operator):
    """Clears all transforms on the bone I hope"""
    bl_idname = "pose.clearall"
    bl_label = "Clear Transforms"
    def execute(self,context):
        for object in bpy.data.objects:
            if object.type == 'ARMATURE':
                bpy.ops.pose.rot_clear()
                bpy.ops.pose.loc_clear()
                bpy.ops.pose.scale_clear()
        return{'FINISHED'}
# FEATURE: A toggle for OpenSubdiv on all objects in scene with a Subdivision
# Surface Modifier.
class ToggleOpensubdiv(bpy.types.Operator):
    """Toggles OpenSubdiv for all Objects for
    improved animation playback speed"""
    bl_idname = "mesh.opensubdiv"
    bl_label = "Mesh OpenSubdiv"
    # Does nothing, testing.
    my_bool = bpy.props.BoolProperty(name="Toggle Option")
    def execute(self,context):
        for mm in (m for o in bpy.context.scene.objects
                   for m in o.modifiers if m.type=='SUBSURF'):
            if mm.use_opensubdiv == True:
                mm.use_opensubdiv = False
            else:
                if mm.use_opensubdiv == False:
                    mm.use_opensubdiv = True
        return{'FINISHED'}
# Feature: Turns OpenSubdiv on for all meshes with Subdivision Surface
# Modifiers for improved viewport performance.
class OpensubdivOn(bpy.types.Operator):
    bl_idname = "opensubdiv.on"
    bl_label = "OpenSubdiv On"
    def execute(self,context):
        for mm in (m for o in bpy.context.scene.objects
                   for m in o.modifiers if m.type=='SUBSURF'):
            mm.use_opensubdiv = True
        return{'FINISHED'}
# Feature: Turns OpenSubdiv on for all meshes with Subdivision Surface
# Modifiers for improved viewport performance.
class OpensubdivOff(bpy.types.Operator):
    bl_idname = "opensubdiv.off"
    bl_label = "OpenSubdiv Off"
    def execute(self,context):
        for mm in (m for o in bpy.context.scene.objects
                   for m in o.modifiers if m.type=='SUBSURF'):
            mm.use_opensubdiv = False
        return{'FINISHED'}
# FEATURE: Simple X-Ray toggle for Armature
class ToggleXray(bpy.types.Operator):
    """Toggles X-Ray mode for bones"""
    bl_idname = "bone.togglexray"
    bl_label = "Armature X-Ray"
    def execute(self, context):
        for object in bpy.data.objects:
            if object.type == 'ARMATURE':
                object.show_x_ray = not object.show_x_ray
        return{'FINISHED'}
# FEATURE: Simple Auto-IK toggle for Armature
#context.active_object.data, "use_auto_ik", text="Auto IK")
class ToggleAutoIK(bpy.types.Operator):
    """Toggles Auto IK mode for bones"""
    bl_idname = "bone.toggleautoik"
    bl_label = "Armature Auto IK"
    def execute(self, context):
        for object in bpy.data.active_object:
            if object.type == 'ARMATURE':
                object.use_auto_ik = not object.use_auto_ik
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
    #    description = 'Always renders from the active camera
    #                   that's set in the Scene properties')
    incremental = BoolProperty(
        name = 'Incremental',
        description = 'Save incremental boomsmashes.',
        default = False)
    use_stamp = BoolProperty(
        name = 'Stamp',
        description = 'Turn on stamp .',
        default = False)
    transparent = BoolProperty(
        name = 'Transparent',
        description = 'Make background transparent .',
        default = False)
    autoplay = BoolProperty(
        name = 'Autoplay',
        description = 'Automatically play boomsmash after making it.',
        default = False)
    unsimplify = BoolProperty(
        name = 'Unsimplify',
        description = "subdivision surface levels at it's render settings.",
        default = False)
    onlyrender = BoolProperty(
        name = 'Only Render',
        description = 'Only have renderable objects visible during.',
        default = False)
    frame_skip = IntProperty(
        name = 'Skip Frames',
        description = 'Number of frames to skip',
        default = 0,
        min = 0)
    resolution_percentage = IntProperty(
        name = 'Resolution Percentage',
        description = ' a percentage of the Render Resolution.',
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
        render = context.scene.render
        sd = context.space_data

        if wm.boom_props.global_toggle:
            boom_props = wm.boom_props
        else:
            boom_props = cs.boom_props
        #pu.db
        old_use_stamp = render.use_stamp
        old_onlyrender = sd.show_only_render
        old_simplify = render.use_simplify
        old_filepath = render.filepath
        old_alpha_mode = render.alpha_mode
        #old_image_settings = render.image_settings
        old_resolution_percentage = render.resolution_percentage
        old_frame_step = cs.frame_step
        #Changes settings of originals
        render.use_stamp = boom_props.use_stamp
        sd.show_only_render = boom_props.onlyrender
        if boom_props.unsimplify:
            render.use_simplify = False
        render.filepath = cs.boom_props.dirname + cs.boom_props.filename
        render.alpha_mode = 'TRANSPARENT' if boom_props.transparent else 'SKY'
        #render.image_settings = boom_props.image_settings
        render.resolution_percentage = boom_props.resolution_percentage
        cs.frame_step = boom_props.frame_skip + 1
        #view_pers = context.area.spaces[0].region_3d.view_perspective
        #if boom_props.scene_cam and view_pers is not 'CAMERA':
        #    bpy.ops.view3d.viewnumpad(type = 'CAMERA')
        #ejecuto
        bpy.ops.render.opengl(animation = True)
        if boom_props.autoplay:
            bpy.ops.render.play_rendered_anim()
        #developer settings
        render.use_stamp = old_use_stamp
        sd.show_only_render = old_onlyrender
        render.use_simplify = old_simplify
        render.filepath = old_filepath
        render.alpha_mode = old_alpha_mode
        #render.image_settings = old_image_settings
        render.resolution_percentage = old_resolution_percentage
        context.scene.frame_step = old_frame_step
        #if boom_props.scene_cam and view_pers is not 'CAMERA':
        #    bpy.ops.view3d.viewnumpad(type = 'CAMERA')
        return {'FINISHED'}
class QuickMotionPath(bpy.types.Operator):
	"""Create motion path by preview range"""
	bl_label = "Calculate"
	bl_idname = "cenda.motion_pats"
	def execute(self, context ):
		if(bpy.context.scene.use_preview_range):
			startFrame = bpy.context.scene.frame_preview_start
			endFrame = bpy.context.scene.frame_preview_end
		else:
			startFrame = bpy.context.scene.frame_start
			endFrame = bpy.context.scene.frame_end
		bpy.ops.pose.paths_calculate(start_frame=startFrame, end_frame=endFrame, bake_location='TAILS')		
		return{'FINISHED'}        
## UI --
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
    displayMode = BoolProperty(name='Display Mode', description="Use"
                               "this to hide many of the options below that"
                               "are generally needed while rigging."
                               "(Useful for animating.)",
                               default=False)
    deformOptions = BoolProperty(name='Deform Options', description="Disp"
                                    "lay the deform options for this bone.",
                                 default=False)
    breakdowner_percentage = IntProperty(
        name = 'Breakdowner Percentage',
        description = ' a percentage for the Breakdowner Button.',
        default = 50,
        min = 0,
        max = 100)
def draw_animatorstoolbox_panel(context, layout):    
    scene = context.scene
    screen = context.screen
    render = scene.render
    cscene = scene.cycles
    object = context.object    
    toolsettings = context.tool_settings
    userpref = context.user_preferences
    edit = userpref.edit
    #
    col = layout.column(align=True)
    row = col.row(align=True)
    box = row.box()    
    box.operator("pose.transforms_clear", text="Reset All")
    box.operator("show_x_ray", text="X-Ray")
    box.operator("bone.toggleselectability", text="Select Armature Only")
    col = layout.column(align=True)
    row = col.row(align=True)
    row.operator("pose.copy", text="Copy")
    row.operator("pose.paste", text="Paste").flipped = False
    row.operator("pose.paste", text="Flip").flipped = True
    col = layout.column(align=True)
    row = col.row(align=True)
    row.prop(toolsettings, "use_keyframe_insert_auto", text="", toggle=True)
    if toolsettings.use_keyframe_insert_auto:
        row.prop(toolsettings, "use_keyframe_insert_keyingset",
                 text="", toggle=True)
        if screen.is_animation_playing:
            subsub = row.row()
            subsub.prop(toolsettings, "use_record_with_nla", toggle=True)
    row.prop_search(scene.keying_sets_all, "active", scene, "keying_sets_all", text="")
    col = layout.column(align=True)
    row = col.row(align=True)
    row.operator("pose.relax", text="Relax")
    row.operator("pose.breakdown", text="Tween")
    row.operator("pose.push", text="Push")    
    #row.prop(scene, 'breakdowner_percentage', slider=True )
    #--Motion Path
    pchan = context.active_pose_bone
    mpath = pchan.motion_path if pchan else None
    col = layout.column(align=True)
    col.label(text="Paths Preview Range:")
    if mpath:
        row = col.row(align=True)
        row.operator("pose.paths_update", text="Update")
        row.operator("pose.paths_clear", text="", icon='X')
    else:
        #col.operator("pose.paths_calculate", text="Calculate")
        col.operator("cenda.motion_pats", icon = 'ANIM_DATA')        
    col = layout.column(align=True)
    row = col.row(align=True)
    row.operator("opensubdiv.on", text="OpenSubdiv")
    row.operator("opensubdiv.off", text="Off")
    col.separator()
#--Simplify
    #col = layout.column(align=True)
    #col.label(text="Simplify:")
    col = layout.column(align=True)
    row = col.row(align=True)
    row.prop(render, "use_simplify", text="Simplify")
    row = col.row(align=True)
    row.prop(render, "simplify_subdivision", text="Subdivision")
#--New Key Type
    col.separator()
    col = layout.column(align=True)
    row = col.row()
    row.prop(edit, "keyframe_new_interpolation_type", text="", icon_only=False)
    row = col.row()
    row.prop(edit, "keyframe_new_handle_type", text="", icon_only=False)
    row = col.row()
    row.prop(toolsettings, "keyframe_type", text="", icon_only=False)
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
        DoButton = self.layout
        DoButton.operator('bs.doboom', text = '', icon = 'RENDER_ANIMATION')
#--Draw Toolboxes
    def draw(self, context):
        layout = self.layout
        draw_animatorstoolbox_panel(context, layout)
# BOOMSMASH        
class BoomsmashPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Animation'
    bl_label = "Boomsmash"
    #bl_context = 'objectmode'
    def draw(self, context):
        layout = self.layout
        draw_boomsmash_panel(context, layout)
def draw_boomsmash_panel(context, layout):
    #layout.row().prop(self, "boomsmash_panel", expand=True)
    col = layout.column(align = True)
    cs = context.scene
    wm = context.window_manager
    render = context.scene.render
    if wm.boom_props.global_toggle:
        boom_props = wm.boom_props
    else:
        boom_props = cs.boom_props
#-File Name
    col.label(text = 'boomsmash filename:')
    row = col.row()
    row.prop(cs.boom_props, 'filename')
    row.operator('bs.setfilename', text = '', icon = 'FILE_BLEND')
#-Folder
    col.label(text = 'boomsmash folder:')
    row = col.row()
    row.prop(cs.boom_props, 'dirname')
    row.operator('bs.setdirname', text = '', icon = 'FILE_FOLDER')
    col.separator()

    col.label(text = 'Use preview range:')
    sub = col.split()
    subrow = sub.row(align = True)
    subrow.prop(context.scene, 'use_preview_range', text = '')
    subrow.prop(context.scene, 'frame_preview_start', text = 'Start')
    subrow.prop(boom_props, 'frame_skip', text = 'Skip')
    subrow.prop(context.scene, 'frame_preview_end', text = 'End')
    col.separator()
    final_res_x = (render.resolution_x * boom_props.resolution_percentage) / 100
    final_res_y = (render.resolution_y * boom_props.resolution_percentage) / 100
    col.label(text = 'Final Resolution: {} x {}'.format(str(final_res_x)[:-2],
              str(final_res_y)[:-2]))
    col.prop(boom_props, 'resolution_percentage', slider = True )
    col.separator()
    #col.label(text="BoomSmash:")
    #col.operator('bs.doboom', text = 'BoomSmash', icon = 'RENDER_ANIMATION')
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
def register():
    bpy.utils.register_module(__name__)
#---Boomsmash
    bpy.types.Scene.boom_props = PointerProperty(
            type = BoomProps, name = 'BoomSmash Properties', description = '')

    bpy.types.WindowManager.boom_props = PointerProperty(
                                       type = BoomProps,
                                       name = 'BoomSmash Global Properties',
                                       description = '')
#---KeyMaps
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    km = kc.keymaps.new(name="Frames")
    kmi = km.keymap_items.new(
        "screen.animatorstools_frame_jump",
        "RIGHT_ARROW", "PRESS", shift=True)
    kmi.properties.forward = True
    KEYMAPS.append((km, kmi))
    kmi = km.keymap_items.new(
        "screen.animatorstools_frame_jump",
        "LEFT_ARROW", "PRESS", shift=True)
    kmi.properties.forward = False
    KEYMAPS.append((km, kmi))
#---New Preferences Tab Apply after Blender Restart FIX
#--update_panel(None, bpy.context)
def unregister():
    bpy.utils.unregister_module(__name__)
#---Boomsmash
    del bpy.types.Scene.boom_props
    del bpy.types.WindowManager.boom_props
#---KeyMaps
    for km, kmi in KEYMAPS:
        km.keymap_items.remove(kmi)
    KEYMAPS.clear()
if __name__ == "__main__":
    register()