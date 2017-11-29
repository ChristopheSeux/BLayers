import bpy
import copy
from .utils import source_layers

def lock_layers(self,context):
    scene = context.scene
    ob = context.object
    layers_from,BLayers,BLayersSettings,layers,objects,selected,nb_layers = source_layers()

    #BLayers = scene.BLayers
    layers = BLayers.values()
    item = BLayers[layers.index(self)]

    lock = self.lock
    id = self.id

    if item.type == 'LAYER' :
        layer_to_lock = [self]
    else :
        layer_to_lock = [l for l in BLayers if l.type=='LAYER' and l.id == id]

    for l in layer_to_lock :
        l.lock = lock
        for ob in scene.objects :
            setattr(ob,'hide_select', lock)
            if lock:
                ob.select = False



def hide_render_layers(self,context):
    BLayers = context.scene.BLayers
    layers = BLayers.layers.values()
    item = BLayers.layers[layers.index(self)]

    hide_render = self.hide_render
    id = self.id

    if item.type == 'LAYER' :
        layer_to_hide = [self]
    else :
        layer_to_hide = [l for l in BLayers.layers if l.type=='LAYER' and l.id == id]

    for l in layer_to_hide :
        l.hide_render = hide_render
        for ob in [o for o in context.scene.objects if o.layers[l.index]] :
            ob.hide_render = hide_render


def hide_layers(self,context) :
    BLayers = context.scene.BLayers
    layers = BLayers.layers.values()
    item = BLayers.layers[layers.index(self)]

    layer_to_hide = [l for l in BLayers.layers if l.type=='LAYER' and l.id == self.id]

    for l in layer_to_hide :
        context.scene.layers[l.index] = self.visibility
            #l.lock = self.lock


class LayersSettings(bpy.types.PropertyGroup):
    lock = bpy.props.BoolProperty(update = lock_layers)
    move = bpy.props.BoolProperty()
    index = bpy.props.IntProperty(default = -1)
    type = bpy.props.StringProperty(default = 'LAYER')
    visibility = bpy.props.BoolProperty(default = True,update=hide_layers)
    hide_render = bpy.props.BoolProperty(default = False,update=hide_render_layers)
    expand = bpy.props.BoolProperty(default = True)
    id = bpy.props.IntProperty(default = -1)




layer_type_items = easingItems = [
    ("AUTO", "", "", 'REC', 1),
    ("SCENE", "", "", 'SCENE_DATA', 2),
    ("ARMATURE", "", "", 'MOD_ARMATURE', 3)]


class BoneBLayersSettings(bpy.types.PropertyGroup) :
    #layers = bpy.props.CollectionProperty(type = LayersSettings)
    active_index = bpy.props.IntProperty()


class SceneBLayersSettings(bpy.types.PropertyGroup) :
    id_count = bpy.props.IntProperty(default = 1)
    #layers = bpy.props.CollectionProperty(type = LayersSettings)
    layer_type = bpy.props.EnumProperty(items = layer_type_items)
    show_index = bpy.props.BoolProperty(default = False)
    #bone_layers =
    active_index = bpy.props.IntProperty()
    #category = bpy.props.EnumProperty(items = gp_category)
