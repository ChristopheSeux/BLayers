import bpy
import copy
from .utils import source_layers

def lock_layers(self,context):
    scene = context.scene
    ob = context.object
    BLayers = self.id_data.BLayers.layers

    objects = scene.objects if self.id_data == context.scene else ob.data.bones

    lock = self.lock

    for ob in [o for o in objects if o.layers[self.index]] :
        setattr(ob,'hide_select', lock)
        if lock:
            ob.select = False


def lock_group_layers(self,context):
    scene = context.scene
    ob = context.object

    BLayers = self.id_data.BLayers.layers

    lock = self.lock_group

    layer_to_lock = [l for l in BLayers if l.type=='LAYER' and l.id == self.id]

    print(layer_to_lock)
    for l in layer_to_lock :
        l.lock = lock



def hide_render_layers(self,context):
    BLayers = context.scene.BLayers.layers
    #layers = BLayers.values()
    item = BLayers[self.col_index]

    hide_render = self.hide_render

    for ob in [o for o in context.scene.objects if o.layers[self.index]] :
        ob.hide_render = hide_render

def hide_group_render_layers(self,context) :
    BLayers = context.scene.BLayers.layers

    hide_render = self.hide_group_render

    layer_to_lock = [l for l in BLayers if l.type=='LAYER' and l.id == self.id]
    print(layer_to_lock)

    for l in layer_to_lock :
        l.hide_render = hide_render

def hide_group_layers(self,context) :
    BLayers = self.id_data.BLayers.layers

    item = BLayers[self.col_index]

    layer_to_hide = [l for l in BLayers if l.type=='LAYER' and l.id == self.id]

    for l in layer_to_hide :
        self.id_data.layers[l.index] = self.visibility


class LayersSettings(bpy.types.PropertyGroup):
    lock = bpy.props.BoolProperty(update = lock_layers,description = 'Lock all objects on this layer')
    lock_group = bpy.props.BoolProperty(update = lock_group_layers,description = 'Lock all layers in this group')

    move = bpy.props.BoolProperty()
    index = bpy.props.IntProperty(default = -1)
    type = bpy.props.StringProperty(default = 'LAYER')
    visibility = bpy.props.BoolProperty(default = True,update=hide_group_layers,description = 'Hide all layers in this group')

    hide_render = bpy.props.BoolProperty(default = False,update=hide_render_layers,description = 'Hide render all objects on this layer')
    hide_group_render = bpy.props.BoolProperty(default = False,update=hide_group_render_layers,description = 'Hide render all layers in this group')

    expand = bpy.props.BoolProperty(default = True,description = 'Expand this group')
    id = bpy.props.IntProperty(default = -1)
    col_index = bpy.props.IntProperty()



layer_type_items = easingItems = [
    ("AUTO", "", "", 'REC', 1),
    ("SCENE", "", "", 'SCENE_DATA', 2),
    ("ARMATURE", "", "", 'MOD_ARMATURE', 3)]


class BLayersArmature(bpy.types.PropertyGroup) :
    layers = bpy.props.CollectionProperty(type = LayersSettings)
    active_index = bpy.props.IntProperty()


class BLayersScene(bpy.types.PropertyGroup) :
    id_count = bpy.props.IntProperty(default = 1)
    layers = bpy.props.CollectionProperty(type = LayersSettings)
    layer_type = bpy.props.EnumProperty(items = layer_type_items,description = 'Change layer mode')
    show_index = bpy.props.BoolProperty(default = False)
    #bone_layers =
    active_index = bpy.props.IntProperty()
    #category = bpy.props.EnumProperty(items = gp_category)
