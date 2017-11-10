import bpy

from .functions import *


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

        #print(self.src_layers)
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
        col_index = BLayers.active_index
        active_layer = BLayers.layers[col_index]

        #index_in_group = [i for i,l in enumerate(BLayers.layers) if l.type=='LAYER' and l.id == active_layer.id]

        dst = self.step + col_index
        if dst >= len(BLayers.layers) :
            dst = 0
        elif dst < 0:
            dst = len(BLayers.layers)-1

        same_group = same_prop(BLayers.layers,col_index,'id')

        if self.step > 0 : #DOWN
            new_index = move_layer_down(BLayers.layers,col_index)
            if active_layer.type == 'LAYER' or (active_layer.type == 'GROUP' and len(same_group)==1):
                BLayers.layers.move(col_index,new_index)

            else :
                #new_index = move_group_down(BLayers.layers,col_index)
                print('new_index',new_index)
                j=0
                for i in reversed(same_group) :
                    BLayers.layers.move(i,new_index+j)
                    j-=1

                new_index = new_index+j+1
        elif self.step < 0 : #UP
            new_index = move_layer_up(BLayers.layers,col_index)
            if active_layer.type == 'LAYER' or (active_layer.type == 'GROUP' and len(same_group)==1):
                BLayers.layers.move(col_index,new_index)

            else  :
                for i in range(len(same_group)) :
                    BLayers.layers.move(max(same_group),new_index)

                    #new_index = move_layer_up(collection,i)
                #new_index = move_group_up(BLayers.layers,col_index)

        BLayers.active_index = new_index
        '''
        if active_layer.type == 'LAYER' :
            if col_index == max(index_in_group) and self.step > 0 or col_index == min(index_in_group) and self.step < 0:
                active_layer.id = -1

            if self.step > 0 and col_index < len(BLayers.layers)-1 and BLayers.layers[col_index+1].id != -1:
                index_in_group = [i for i,l in enumerate(BLayers.layers) if  l.id == BLayers.layers[col_index+1].id]
                dst = max(index_in_group)
            elif self.step < 0 and BLayers.layers[col_index-1].id != -1 :
                index_in_group = [i for i,l in enumerate(BLayers.layers) if  l.id == BLayers.layers[col_index-1].id]
                dst = min(index_in_group)

            BLayers.layers.move(col_index,dst)
            BLayers.active_index = dst

        elif active_layer.type == 'GROUP' :
            if self.step > 0 : ## DOWN
                if BLayers.layers[col_index-1].id != -1 :
                    src = max(index_in_group)
                    dst = col_index
                    iteration = 1
                else :

            if self.step < 0 :  ## UP
                if BLayers.layers[col_index+1].id != -1 :
                    src = col_index-1
                    dst = max(index_in_group)
                    iteration = 1
                else :
                    move =

            for i in range(iteration) :
                BLayers.layers.move(col_index-1,max(index_in_group))
                BLayers.active_index = col_index-1
                '''

        return {'FINISHED'}


class RemoveLayer(bpy.types.Operator):
    """Remove Parent"""
    bl_idname = "blayers.remove_layer"
    bl_label = "Remove Gpencil Layer"

    def execute(self, context):
        scene = context.scene
        BLayers = scene.BLayers
        col_index = BLayers.active_index
        layer = BLayers.layers[col_index]

        if layer.type == 'GROUP' or not [o for o in scene.objects if o.layers[layer.index]] :
            if layer.type == 'GROUP' :
                for l in [l for l in BLayers.layers if l.id == layer.id] :
                    l.id = -1
            BLayers.layers.remove(col_index)
            BLayers.active_index = col_index-1

        else :
            self.report({'ERROR'},'You only can delete empty layer')


        return {'FINISHED'}


class AddGroup(bpy.types.Operator):
    """Remove Parent"""
    bl_idname = "blayers.add_group"
    bl_label = "Add Gpencil Layer"

    def execute(self, context):
        scene = context.scene
        BLayers = scene.BLayers
        active_index = BLayers.active_index

        group = BLayers.layers.add()

        existing_number = [int(l.name[-2:]) for l in BLayers.layers if l.name.startswith('GROUP_') and l.name[-2:].isnumeric()]
        free_number = max(existing_number)+1 if existing_number else 1
        for i in existing_number :
            if not i+1 in existing_number :
                free_number = i+1
                break

        group.name = 'GROUP_%02d'%free_number
        group.type = 'GROUP'
        scene.BLayers.id_count +=1
        group.id = BLayers.id_count
        #print(group.id)
        BLayers.active_index = len(BLayers.layers)-1
        context.area.tag_redraw()

        return {'FINISHED'}

class MoveInGroup(bpy.types.Operator):
    """Remove Parent"""
    bl_idname = "blayers.move_in_group"
    bl_label = "Add Gpencil Layer"

    index = bpy.props.IntProperty()

    def execute(self, context):
        scene = context.scene
        BLayers = scene.BLayers
        col_index = BLayers.active_index
        layer = BLayers.layers[col_index]

        if layer.type =='LAYER' :

            group = BLayers.layers[self.index]
            offset = 1 if col_index > self.index else 0
            layer.id = group.id
            BLayers.layers.move(col_index,self.index+offset)
            BLayers.active_index = self.index+offset
            context.area.tag_redraw()

        return {'FINISHED'}

class AddLayer(bpy.types.Operator):
    """Remove Parent"""
    bl_idname = "blayers.add_layer"
    bl_label = "Add Gpencil Layer"

    def execute(self, context):
        scene = context.scene
        BLayers = scene.BLayers
        active_index = BLayers.active_index

        existing_indexes = [l.index for l in BLayers.layers if l.type =='LAYER']
        if len(existing_indexes) <= 19 :
            free_index = max(existing_indexes)+1 if existing_indexes else 0
            for i in existing_indexes :
                if not i+1 in existing_indexes :
                    free_index = i+1
                    break

            layer = BLayers.layers.add()
            existing_number = [int(l.name[-2:]) for l in BLayers.layers if l.name.startswith('Layer_') and l.name[-2:].isnumeric()]
            free_number = max(existing_number)+1 if existing_number else 1
            for i in existing_number :
                if not i+1 in existing_number :
                    free_number = i+1
                    break


            layer.name = 'Layer_%02d'%free_number
            layer.index = free_index
            layer.type = 'LAYER'
            BLayers.active_index = len(BLayers.layers)-1
            context.area.tag_redraw()

        return {'FINISHED'}
