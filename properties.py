import bpy

def lock_layers(self,context):
    BLayers = context.scene.BLayers
    layers = BLayers.layers.values()
    item = BLayers.layers[layers.index(self)]

    if self.type == 'LAYER' :
        layer_to_lock = [item]
    else :
        layer_to_lock = [l for l in BLayers.layers if l.type=='LAYER' and l.id == self.id]


    for l in layer_to_lock :
        l.lock = self.lock
        for ob in [o for o in context.scene.objects if o.layers[l.index]] :
            ob.hide_select = self.lock
            if self.lock:
                ob.select = False

    #if

def hide_layers(self,context) :
    BLayers = context.scene.BLayers
    layers = BLayers.layers.values()
    item = BLayers.layers[layers.index(self)]

    layer_to_hide = [l for l in BLayers.layers if l.type=='LAYER' and l.id == self.id]
    print(layer_to_hide)

    for l in layer_to_hide :
        context.scene.layers[l.index] = not self.hide
            #l.lock = self.lock



class LayersSettings(bpy.types.PropertyGroup):
    lock = bpy.props.BoolProperty(update = lock_layers)
    move = bpy.props.BoolProperty()
    index = bpy.props.IntProperty(default = -1)
    type = bpy.props.StringProperty(default = 'LAYER')
    hide = bpy.props.BoolProperty(default = False,update=hide_layers)
    expand = bpy.props.BoolProperty(default = True)
    id = bpy.props.IntProperty(default = -1)

class BLayersSettings(bpy.types.PropertyGroup) :
    id_count = bpy.props.IntProperty(default = 1)
    layers = bpy.props.CollectionProperty(type = LayersSettings)
    active_index = bpy.props.IntProperty()
    #category = bpy.props.EnumProperty(items = gp_category)
