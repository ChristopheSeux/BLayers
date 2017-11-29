import bpy

from .functions import *
from .utils import source_layers


class ChangeShortcut(bpy.types.Operator):
    """Change BLayers shortcut"""
    bl_idname = "blayers.change_shorcut"
    bl_label = "Change Shortcut"

    def execute(self, context):
        wm = context.window_manager
        keyconfig = wm.keyconfigs.user.keymaps.get('Object Mode')
        #print('check')
        if keyconfig and keyconfig.keymap_items.get('object.move_to_layer'):
            move_to_layer = keyconfig.keymap_items.get('object.move_to_layer')
            move_to_layer.active = False

        return {'FINISHED'}

class SynchroniseLayers(bpy.types.Operator):
    """Synchronise BLayers"""
    bl_idname = "blayers.synchronise_layers"
    bl_label = "Synchronise Layers"

    def execute(self, context):
        scene = context.scene
        ob = context.object

        layers_from,BLayers,BLayersSettings,layers,objects,selected,nb_layers = source_layers()

        full_layers = []
        existing_indexes = [l.index for l in BLayers if l.type =='LAYER']

        for ob in objects :
            for i,l in enumerate(ob.layers) :
                if l and i not in full_layers:
                    full_layers.append(i)

        for free_index in full_layers :
            if not free_index in existing_indexes :
                layer = BLayers.add()
                existing_number = [int(l.name[-2:]) for l in BLayers if l.name.startswith('Layer_') and l.name[-2:].isnumeric()]

                free_number = max(existing_number)+1 if existing_number else 1
                for i in existing_number :
                    if not i+1 in existing_number :
                        free_number = i+1
                        break

                layer.name = 'Layer_%02d'%free_number
                layer.index = free_index
                layer.type = 'LAYER'
        return {'FINISHED'}


class ObjectsToLayer(bpy.types.Operator):
    """Remove Parent"""
    bl_idname = "blayers.objects_to_layer"
    bl_label = "Objects To Layer"

    @classmethod
    def poll(self,context) :
        layers_from,BLayers,BLayersSettings,layers,objects,selected,nb_layers = source_layers()
        return True if selected and len(BLayers) else False

    def draw(self,context) :
        scene = context.scene
        layout = self.layout

        layers_from,BLayers,BLayersSettings,layers,objects,selected,nb_layers = source_layers()

        col = layout.column(align=True)
        for l in [l for l in BLayers if l.type == 'LAYER'] :
            col.prop(l,'move',toggle = True,text = l.name)


    def execute(self, context):
        scene = context.scene
        layers_from,BLayers,BLayersSettings,layers,objects,selected,nb_layers = source_layers()

        dst_layers = [l.index for l in BLayers if l.move]

        for ob in context.selected_objects :
            for i in dst_layers :
                ob.layers[i]=True

            for i in self.src_layers :
                if i not in dst_layers :
                    ob.layers[i]=False

        return {'FINISHED'}

    def invoke(self, context, event):
        scene = context.scene
        layers_from,BLayers,BLayersSettings,layers,objects,selected,nb_layers = source_layers()
        index = BLayers.active_index

        self.src_layers = []
        for ob in context.selected_objects :
            for i,l in enumerate(ob.layers) :
                if l and i not in self.src_layers :
                    self.src_layers.append(i)

        #print(self.src_layers)
        if index in range(len(BLayers)):
            BLayers[index].move = True
            for l in BLayers :
                if l.index in self.src_layers :
                    l.move = True
                else :
                    l.move = False
        wm = context.window_manager
        return wm.invoke_props_dialog(self,width=175)


class SelectObjects(bpy.types.Operator):
    """Isolate layer lock"""
    bl_idname = "blayers.select_objects"
    bl_label = "Select all objects on active layer"

    def execute(self, context):
        scene = context.scene
        ob = context.object
        layers_from,BLayers,BLayersSettings,layers,objects,selected,nb_layers = source_layers()

        active_layer = BLayers[BLayersSettings.active_index]
        active_index = active_layer.index

        if active_layer.type == 'LAYER' :
            layers = [active_index]
        else :
            layers = [l.index for l in BLayers if l.id == active_layer.id]

        for ob in objects :
            for index in real_layers :
                if ob.layers[index] :
                    ob.select = True
                    objects.active = True



        return {'FINISHED'}

class ToggleLayer(bpy.types.Operator):
    """Isolate layer lock"""
    bl_idname = "blayers.toogle_layer"
    bl_label = "Toggle Layer Render"

    prop = bpy.props.StringProperty()

    def execute(self, context):
        scene = context.scene

        layers_from,BLayers,BLayersSettings,layers,objects,selected,nb_layers = source_layers()

        active_layer = BLayers[BLayersSettings.active_index]
        passive_layers = [l for l in BLayers if l !=active_layer]

        prop = self.prop

        if active_layer.type == 'GROUP' :
            passive_layers = [l for l in BLayers if l.type =='LAYER' and l !=active_layer and l.id != active_layer.id]
        else :
            passive_layers = [l for l in BLayers if l.type =='LAYER' and l !=active_layer]

        true_layers = [l for l in BLayers if l !=active_layer and l.type =='LAYER' and getattr(l,prop)]
        toogle = False if len(true_layers)==len(passive_layers) else True

        groups = [g for g in BLayers if g.type =='GROUP' and g.id != active_layer.id]
        #scene.layers[active_index] = True

        setattr(active_layer,prop,False)

        for g in groups :
            setattr(g,prop,toogle)

        for l in passive_layers:
            if l.type == 'LAYER' :
                setattr(l,prop,toogle)


        return {'FINISHED'}


class ToogleLayerHide(bpy.types.Operator):
    """Remove Parent"""
    bl_idname = "blayers.toogle_layer_hide"
    bl_label = "Toggle Layer Hide"

    def execute(self, context):
        scene = context.scene

        layers_from,BLayers,BLayersSettings,layers,objects,selected,nb_layers = source_layers()

        active_layer = BLayers[BLayersSettings.active_index]
        active_index = active_layer.index

        if active_layer.type == 'GROUP' :
            layers_index = [l.index for l in BLayers if l.type =='LAYER' and l.index !=active_index and l.id != active_layer.id]
        else :
            layers_index = [l.index for l in BLayers if l.type =='LAYER' and l.index !=active_index]

        hide_layers = [i for i in layers_index if not layers_from.layers[i]]

        toogle = True if len(hide_layers)==len(layers_index) else False

        groups = [g for g in BLayers if g.type =='GROUP' and g.id != active_layer.id]
        layers[active_index] = True

        for index in layers_index:
            layers[index] = toogle

        for g in groups :
            g.visibility = toogle

        return {'FINISHED'}


class MoveLayer(bpy.types.Operator):
    """Remove Parent"""
    bl_idname = "blayers.layer_move"
    bl_label = "Move Layer"

    step = bpy.props.IntProperty()

    def execute(self, context):
        scene = context.scene
        ob = context.object

        layers_from,BLayers,BLayersSettings,layers,objects,selected,nb_layers = source_layers()

        col_index = BLayersSettings.active_index
        active_layer = BLayers[col_index]

        same_group = same_prop(BLayers,col_index,'id')

        if active_layer.type == 'LAYER' :
            if col_index == max(same_group) and self.step > 0 or col_index == min(same_group)+1 and self.step < 0:
                active_layer.id = -1

        if self.step > 0 : #DOWN
            new_index = move_layer_down(BLayers,col_index)

            if active_layer.type == 'LAYER' or (active_layer.type == 'GROUP' and len(same_group)==1):
                BLayers.move(col_index,new_index)

            else : # it's a group with layers
                j=0
                for i in reversed(same_group) :
                    layers.move(i,new_index+j)
                    j-=1

                new_index = new_index+j+1
        elif self.step < 0 : #UP
            new_index = move_layer_up(BLayers,col_index)
            if active_layer.type == 'LAYER' or (active_layer.type == 'GROUP' and len(same_group)==1):
                BLayers.move(col_index,new_index)

            else  :
                for i in range(len(same_group)) :
                    BLayers.move(max(same_group),new_index)

                    #new_index = move_layer_up(collection,i)
                #new_index = move_group_up(BLayers.layers,col_index)

        BLayersSettings.active_index = new_index

        redraw_areas()
        return {'FINISHED'}


class RemoveLayer(bpy.types.Operator):
    """Remove Parent"""
    bl_idname = "blayers.remove_layer"
    bl_label = "Remove Gpencil Layer"

    def execute(self, context):
        scene = context.scene
        ob = context.object

        layers_from,BLayers,BLayersSettings,layers,objects,selected,nb_layers = source_layers()

        col_index = BLayersSettings.active_index
        layer = BLayers[col_index]

        if layer.type == 'GROUP' or not [o for o in objects if o.layers[layer.index]] :
            if layer.type == 'GROUP' :
                for l in [l for l in BLayers if l.id == layer.id] :
                    l.id = -1
            BLayers.remove(col_index)
            BLayersSettings.active_index = col_index-1

        else :
            self.report({'ERROR'},'You only can delete empty layer')

        redraw_areas()
        return {'FINISHED'}

'''
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
        redraw_areas()

        return {'FINISHED'}
    '''

class MoveInGroup(bpy.types.Operator):
    """Remove Parent"""
    bl_idname = "blayers.move_in_group"
    bl_label = "Add Gpencil Layer"

    index = bpy.props.IntProperty()

    def execute(self, context):
        scene = context.scene
        ob = context.object

        layers_from,BLayers,BLayersSettings,layers,objects,selected,nb_layers = source_layers()

        col_index = BLayers.active_index
        layer = BLayers.layers[col_index]

        if layer.type =='LAYER' :
            group = BLayers.layers[self.index]
            offset = 1 if col_index > self.index else 0
            layer.id = group.id
            BLayers.layers.move(col_index,self.index+offset)
            BLayers.active_index = self.index+offset
        redraw_areas()

        return {'FINISHED'}

class AddLayer(bpy.types.Operator):
    """Remove Parent"""
    bl_idname = "blayers.add_layer"
    bl_label = "Add Gpencil Layer"

    type = bpy.props.StringProperty()

    def execute(self, context):
        scene = context.scene
        ob = context.object

        layers_from,BLayers,BLayersSettings,layers,objects,selected,nb_layers = source_layers()

        existing_indexes = [l.index for l in BLayers if l.type =='LAYER']

        if self.type == 'GROUP' :
            group = BLayers.layers.add()

            existing_number = [int(l.name[-2:]) for l in BLayers if l.name.startswith('GROUP_') and l.name[-2:].isnumeric()]
            free_number = max(existing_number)+1 if existing_number else 1
            for i in existing_number :
                if not i+1 in existing_number :
                    free_number = i+1
                    break

            group.name = 'GROUP_%02d'%free_number
            group.type = 'GROUP'
            scene.BLayers.id_count +=1
            group.id = scene.BLayers.id_count
            BLayers.active_index = len(BLayers)-1

        else :
            if len(existing_indexes)<nb_layers+1 :
                free_index =  0
                for i in range(nb_layers) :
                    if not i in existing_indexes :
                        free_index = i
                        break

                layer = BLayers.add()
                existing_number = [int(l.name[-2:]) for l in BLayers if l.name.startswith('Layer_') and l.name[-2:].isnumeric()]
                free_number = max(existing_number)+1 if existing_number else 1
                for i in existing_number :
                    if not i+1 in existing_number :
                        free_number = i+1
                        break


                layer.name = 'Layer_%02d'%free_number
                layer.index = free_index
                layer.type = 'LAYER'
                BLayersSettings.active_index = len(BLayers)-1
                layers[free_index] = True

                if self.type == 'LAYER_FROM_SELECTED' :
                    empty_layers = [False]*20
                    empty_layers[free_index] = True
                    for ob in selected :
                        ob.layers = empty_layers

        redraw_areas()

        return {'FINISHED'}
