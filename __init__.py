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
    imp.reload(utils)
    imp.reload(functions)

else :
    from . import properties
    from . import operators
    from . import panels
    from . import utils
    from . import functions

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
        #print('check')
        if keyconfig and keyconfig.keymap_items.get('object.move_to_layer'):
            move_to_layer = keyconfig.keymap_items.get('object.move_to_layer')
            move_to_layer.idname = 'blayers.objects_to_layer'

            #keyconfig.keymap_items.remove(keymap)

            print('check')

            return {'CANCELLED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}


@persistent
def change_key_map(dummy):
    bpy.ops.blayers.key_remmapper('INVOKE_DEFAULT')
    functions.create_layers()


custom_icons = None


def register():
    utils.get_icons()

    bpy.app.handlers.load_post.append(change_key_map)
    bpy.utils.register_module(__name__)
    bpy.types.Scene.BLayers = bpy.props.PointerProperty(type = properties.BLayersSettings)

    # unregister blender object to layer
    wm = bpy.context.window_manager
    keyconfig = wm.keyconfigs[0].keymaps.get('Object Mode')
    if keyconfig and keyconfig.keymap_items.get('object.move_to_layer'):
        move_to_layer = keyconfig.keymap_items.get('object.move_to_layer')
        move_to_layer.idname = 'blayers.objects_to_layer'


    #unregister render layer panel
    renderpasses =[a for a in bpy.types.Panel.__subclasses__() if a.__name__ == 'CyclesRender_PT_layer_options']
    register.layer_panel = renderpasses[0]
    register.rl_draw = register.layer_panel.draw

    register.layer_panel.draw = panels.render_layer_draw



def unregister():
    bpy.utils.previews.remove(utils.custom_icons)
    register.layer_panel.draw = register.rl_draw

    wm = bpy.context.window_manager
    keyconfig = wm.keyconfigs[0].keymaps.get('Object Mode')
    if keyconfig and keyconfig.keymap_items.get('blayers.objects_to_layer'):
        move_to_layer = keyconfig.keymap_items.get('blayers.objects_to_layer')
        move_to_layer.idname = 'object.move_to_layer'


    bpy.app.handlers.load_post.remove(change_key_map)
    del bpy.types.Scene.BLayers
    bpy.utils.unregister_module(__name__)
