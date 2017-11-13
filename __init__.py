bl_info = {
    "name": "BLayers",
    "author": "Christophe Seux",
    "version": (0, 1),
    "blender": (2, 78, 0),
    "category": "User"}

if "bpy" in locals():
    import imp
    imp.reload(properties)
    imp.reload(operators)
    imp.reload(panels)

from .properties import *
from .operators import *
from .panels import *
from .utils import get_icons

import os
import bpy
from bpy.app.handlers import persistent


# Key map changer
class ModalOperator(bpy.types.Operator):
    """Move an object with the mouse, example"""
    bl_idname = "blayers.key_remmapper"
    bl_label = "Key Remmaper"
    bl_options = {'INTERNAL'}

    def modal(self, context, event):
        wm = bpy.context.window_manager
        keyconfig = wm.keyconfigs[0].keymaps.get('Object Mode')

        if keyconfig and keyconfig.keymap_items.get('object.move_to_layer'):
            keyconfig.keymap_items.get('object.move_to_layer').active = False

            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}


@persistent
def change_key_map(dummy):
    bpy.ops.blayers.key_remmapper('INVOKE_DEFAULT')

    for scene in bpy.data.scenes :
        if not scene.BLayers.layers :
            src_layers = []
            for ob in scene.objects :
                for i,l in enumerate(ob.layers) :
                    if l and i not in src_layers :
                        src_layers.append(i)

            for l_index in sorted(src_layers) :
                l = scene.BLayers.layers.add()
                l.index = l_index
                l.name = 'Layer_%02d'%(l_index+1)

custom_icons = None

def unregister():

    bpy.utils.unregister_module(__name__)



def register():
    get_icons()

    register.Panels = []
    bpy.app.handlers.load_post.append(change_key_map)
    bpy.utils.register_module(__name__)
    bpy.types.Scene.BLayers = bpy.props.PointerProperty(type = BLayersSettings)

    # unregister blender object to layer
    wm = bpy.context.window_manager
    keyconfig = wm.keyconfigs[0].keymaps.get('Object Mode')

    if keyconfig and keyconfig.keymap_items.get('object.move_to_layer'):
        keyconfig.keymap_items.get('object.move_to_layer').active = False

    register.addon_keymaps = []
    wm = bpy.context.window_manager
    addon = wm.keyconfigs.addon

    if addon:
        km = addon.keymaps.new(name = "3D View", space_type = "VIEW_3D")
        km.keymap_items.new("blayers.objects_to_layer", type = "M", value = "PRESS")
        register.addon_keymaps.append(km)

    #unregister render layer panel
    panels =[a for a in bpy.types.Panel.__subclasses__() if a.__name__ == 'CyclesRender_PT_layer_options']
    register.layer_panel = panels[0]
    register.rl_draw = panels[0].draw

    register.layer_panel.draw = render_layer_draw

    '''
    for pt in bpy.types.Panel.__subclasses__():
        if pt.bl_space_type == 'VIEW_3D' and pt.bl_region_type == 'UI'  :
            if pt.bl_label in ['Grease Pencil Layers','Grease Pencil Colors']:
                if "bl_rna" in pt.__dict__:   # <-- check if we already removed!
                    register.Panels.append(pt)
                    bpy.utils.unregister_class(pt)
                    '''

def unregister():
    bpy.utils.previews.remove(get_icons.custom_icons)
    register.layer_panel.draw = register.rl_draw

    wm = bpy.context.window_manager
    wm.keyconfigs['Blender User'].keymaps['Object Mode'].keymap_items['object.move_to_layer'].active = True
    for km in register.addon_keymaps:
        for kmi in km.keymap_items:
            km.keymap_items.remove(kmi)

    register.addon_keymaps.clear()
    bpy.app.handlers.load_post.remove(change_key_map)
    del bpy.types.Scene.BLayers
    bpy.utils.unregister_module(__name__)
    '''
    for panel in register.Panels :
        bpy.utils.register_class(panel)
        '''
