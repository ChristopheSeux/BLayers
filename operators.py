import bpy


class ObjectsToLayer(bpy.types.Operator):
    """Remove Parent"""
    bl_idname = "blayers.objects_to_layer"
    bl_label = "Objects To Layer"

    @classmethod
    def poll(self,context) :
        return True if context.selected_objects and len(context.scene.BLayers.layers) else False

    def draw(self,context) :
        scene = context.scene
        BLayers = scene.BLayers
        layout = self.layout

        col = layout.column(align=True)
        for l in BLayers.layers :
            col.prop(l,'move',toggle = True,text = l.name)


    def execute(self, context):
        scene = context.scene
        BLayers = scene.BLayers

        dst_layers = [l.index for l in BLayers.layers if l.move]

        for ob in context.selected_objects :
            for i in dst_layers :
                ob.layers[i]=True

            for i in self.src_layers :
                if i not in dst_layers :
                    ob.layers[i]=False

        return {'FINISHED'}

    def invoke(self, context, event):
        scene = context.scene
        BLayers = scene.BLayers
        index = BLayers.active_index

        self.src_layers = []
        for ob in context.selected_objects :
            for i,l in enumerate(ob.layers) :
                if l and i not in self.src_layers :
                    self.src_layers.append(i)

        print(self.src_layers)
        if index in range(len(BLayers.layers)):
            BLayers.layers[index].move = True
            for l in BLayers.layers :
                if l.index in self.src_layers :
                    l.move = True
                else :
                    l.move = False
        wm = context.window_manager
        return wm.invoke_props_dialog(self,width=175)


class ToggleLayerLock(bpy.types.Operator):
    """Isolate layer lock"""
    bl_idname = "blayers.toogle_layer_lock"
    bl_label = "Toggle Layer Lock"

    def execute(self, context):
        scene = context.scene
        BLayers = scene.BLayers
        active_layer = BLayers.layers[BLayers.active_index]
        passive_layers = [l for l in BLayers.layers if l !=active_layer]

        locked_layers = [l.index for l in BLayers.layers if l !=active_layer and l.lock]

        toogle = False if len(locked_layers)==len(passive_layers) else True

        active_layer.lock = False

        for ob in scene.objects :
            if ob.layers[active_layer.index] :
                ob.hide_select = False
            else :
                ob.hide_select = toogle

        for l in passive_layers:
            l.lock = toogle

        return {'FINISHED'}


class ToogleLayerHide(bpy.types.Operator):
    """Remove Parent"""
    bl_idname = "blayers.toogle_layer_hide"
    bl_label = "Toggle Layer Hide"

    def execute(self, context):
        scene = context.scene
        BLayers = scene.BLayers
        active_index = BLayers.layers[BLayers.active_index].index

        layers_index = [l.index for l in BLayers.layers if l.index !=active_index]
        hide_layers = [i for i in layers_index if not scene.layers[i]]

        toogle = True if len(hide_layers)==len(layers_index) else False

        scene.layers[active_index] = True
        for index in layers_index:
            scene.layers[index] = toogle

        return {'FINISHED'}


class MoveLayer(bpy.types.Operator):
    """Remove Parent"""
    bl_idname = "blayers.layer_move"
    bl_label = "Move Layer"

    step = bpy.props.IntProperty()

    def execute(self, context):
        scene = context.scene
        BLayers = scene.BLayers
        index = BLayers.active_index
        dst = self.step + index
        if dst >= len(BLayers.layers) :
            dst = 0
        elif dst < 0:
            dst = len(BLayers.layers)-1

        print(dst)

        BLayers.layers.move(index,dst)
        BLayers.active_index = dst
        '''
        sc_object = [o for o in scene.objects if o.layers[index]]
        dest_objects = [o for o in scene.objects if o.layers[dst]]

        for ob in sc_object:
            ob.layers[dst] = True
            ob.layers[index] = False

        for ob in dest_objects:
            ob.layers[index] = True
            ob.layers[dst] = False
            '''

        return {'FINISHED'}


class RemoveLayer(bpy.types.Operator):
    """Remove Parent"""
    bl_idname = "blayers.remove_layer"
    bl_label = "Remove Gpencil Layer"

    def execute(self, context):
        scene = context.scene
        BLayers = scene.BLayers
        index = BLayers.active_index

        BLayers.layers.remove(index)
        BLayers.active_index = index-1

        return {'FINISHED'}

class AddLayer(bpy.types.Operator):
    """Remove Parent"""
    bl_idname = "blayers.add_layer"
    bl_label = "Add Gpencil Layer"

    def execute(self, context):
        scene = context.scene
        BLayers = scene.BLayers
        active_index = BLayers.active_index

        existing_indexes = [l.index for l in BLayers.layers]
        free_index = max(existing_indexes)+1 if existing_indexes else 0
        for i in existing_indexes :
            if not i+1 in existing_indexes :
                free_index = i+1
                break

        layer = BLayers.layers.add()
        layer.name = 'New Layer'
        layer.index = free_index
        BLayers.active_index = len(BLayers.layers)-1
        context.area.tag_redraw()

        return {'FINISHED'}
