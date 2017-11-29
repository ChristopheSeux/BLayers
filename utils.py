import bpy
import bpy.utils.previews
from os.path import join,basename,dirname,splitext
from os import listdir

def redraw_areas():
    for area in bpy.context.screen.areas :
        area.tag_redraw()

def get_icons():
    global custom_icons
    custom_icons = bpy.utils.previews.new()
    icons_dir = join(dirname(__file__),'icons')
    for icon in listdir(icons_dir) :
        custom_icons.load(splitext(icon)[0].upper(), join(icons_dir, icon), 'IMAGE',force_reload=True)

    custom_icons.update()

def source_layers():
    scene = bpy.context.scene
    ob = bpy.context.object
    BLayersSettings = scene.BLayersSettings

    if BLayersSettings.layer_type == 'ARMATURE' :
        if ob and ob.type == 'ARMATURE' :
            layer_mode= 'ARMATURE'
        else :
            layer_mode = 'SCENE'

    elif BLayersSettings.layer_type == 'SCENE' :
        layer_mode = 'SCENE'

    else :
        if bpy.context.mode in ['POSE','EDIT_ARMATURE'] :
            layer_mode = 'ARMATURE'
        else :
            layer_mode = 'SCENE'

    if layer_mode == 'SCENE' :
        return scene,scene.BLayers,scene.BLayersSettings,scene.layers,scene.objects,bpy.context.selected_pose_bones,20
    else :
        selected_bones =[]
        if bpy.context.mode =='POSE':
            selected_bones = [b.bone for b in bpy.context.selected_pose_bones]
        elif bpy.context.mode =='EDIT_ARMATURE' :
            selected_bones = [b for b in bpy.context.selected_editable_bones]

        return ob.data,ob.data.BLayers,ob.data.BLayersSettings,ob.data.layers,ob.data.bones,selected_bones,31
