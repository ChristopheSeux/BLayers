import bpy

def lock_layers(self,context):

    print(self)
    #print(self.name)

    #print([a for a in BLayersSettings.layers[0]])
    #print(BLayersSettings.layers.index(self))
    layers = context.scene.BLayers.layers.values()
    index = layers.index(self)
    for ob in [o for o in context.scene.objects if o.layers[index]] :
        ob.hide_select = self.lock
        if self.lock:
            ob.select = False

class LayersSettings(bpy.types.PropertyGroup):
    lock = bpy.props.BoolProperty(update = lock_layers)
    move = bpy.props.BoolProperty()
    index = bpy.props.IntProperty()
    #hide = bpy.props.BoolProperty(default = False)


class BLayersSettings(bpy.types.PropertyGroup) :
    layers = bpy.props.CollectionProperty(type = LayersSettings)
    active_index = bpy.props.IntProperty()
    #category = bpy.props.EnumProperty(items = gp_category)
