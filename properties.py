import bpy
import copy
from .utils import source_layers

def lock_layers(self,context):
    scene = context.scene
    ob = context.object
    #layers_from,BLayers,BLayersSettings,layers,objects,selected,nb_layers = source_layers()

    BLayers = self.id_data.BLayers.layers
    #objects = scene.objects if self.id_data == scene else ob.data.bones
    #layers = BLayers.values()
    objects = scene.objects
    item = BLayers[self.col_index]

    lock = self.lock
    id = self.id

    #layer_type = str(item.type)

    #if layer_type == 'LAYER' :
    #    layer_to_lock = [self]
    #else :
    #layer_to_lock = [l for l in BLayers if l.type=='LAYER' and l.id == id]
    #layer_to_lock.remove(self)
    layer_to_lock = eval(self.get_layers)
    print(layer_to_lock)

    for l in layer_to_lock :
        l.lock = lock
        for ob in [o for o in objects if o.layers[l.index]] :
            setattr(ob,'hide_select', lock)
            if lock:
                ob.select = False



def hide_render_layers(self,context):
    BLayers = context.scene.BLayers.layers
    #layers = BLayers.values()
    item = BLayers[self.col_index]

    hide_render = self.hide_render
    id = self.id

    if item.type == 'LAYER' :
        layer_to_hide = [self]
    else :
        layer_to_hide = [l for l in BLayers if l.type=='LAYER' and l.id == id]

    for l in layer_to_hide :
        l.hide_render = hide_render
        for ob in [o for o in context.scene.objects if o.layers[l.index]] :
            ob.hide_render = hide_render


def hide_layers(self,context) :
    BLayers = context.scene.BLayers.layers
    #layers = BLayers.layers.values()
    item = BLayers[self.col_index]


    layer_to_hide = [l for l in BLayers.layers if l.type=='LAYER' and l.id == self.id]

    for l in layer_to_hide :
        context.scene.layers[l.index] = self.visibility
            #l.lock = self.lock


def get_layers(self):
    return str([l for l in self.id_data.BLayers.layers if l.type=='LAYER' and l.id == self.id and l!=self])

class LayersSettings(bpy.types.PropertyGroup):
    lock = bpy.props.BoolProperty(update = lock_layers)

    get_layers = bpy.props.StringProperty(get = get_layers)

    #lock_scene_layer = bpy.props.BoolProperty(update = lock_layers)
    #lock_scene_group = bpy.props.BoolProperty(update = lock_layers)
    #lock_armature_layer = bpy.props.BoolProperty(update = lock_layers)
    #lock_armature_group = bpy.props.BoolProperty(update = lock_layers)
    #lock_group =

    move = bpy.props.BoolProperty()
    index = bpy.props.IntProperty(default = -1)
    type = bpy.props.StringProperty(default = 'LAYER')
    visibility = bpy.props.BoolProperty(default = True,update=hide_layers)
    hide_render = bpy.props.BoolProperty(default = False,update=hide_render_layers)
    expand = bpy.props.BoolProperty(default = True)
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
    layer_type = bpy.props.EnumProperty(items = layer_type_items)
    show_index = bpy.props.BoolProperty(default = False)
    #bone_layers =
    active_index = bpy.props.IntProperty()
    #category = bpy.props.EnumProperty(items = gp_category)
