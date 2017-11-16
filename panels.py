import bpy
from . import utils

def render_layer_draw(self, context):
    layout = self.layout
    #main_col = layout.column(align = True)
    scene = context.scene
    BLayers = scene.BLayers
    rd = scene.render
    rl = rd.layers.active

    if BLayers.layers :
        layers = [l for l in BLayers.layers if l.type == 'LAYER']
        row = layout.row()

        col = row.column(align = True)
        col.label('Layer : ')
        for layer in layers :
            col.prop(context.scene.render.layers.active,'layers',index = layer.index,toggle = True,text = layer.name)

        col = row.column(align = True)
        col.label('Mask Layer: ')
        for layer in layers :
            col.prop(context.scene.render.layers.active,'layers_zmask',index = layer.index,toggle = True,text = layer.name)

        col = row.column(align = True)
        col.label('Exclude : ')
        for layer in layers :
            col.prop(context.scene.render.layers.active,'layers_exclude',index = layer.index,toggle = True,text = layer.name)

        #split = layout.split()
        layout.separator()
    #col = split.column()
    #col.prop(scene, "layers", text="Scene")
    #col.prop(rl, "layers_exclude", text="Exclude")

    #col = split.column()

    split = layout.split()

    col = split.column()
    col.label(text="Material:")
    col.prop(rl, "material_override", text="")
    col.separator()
    col.prop(rl, "samples")

    col = split.column()
    col.prop(rl, "use_sky", "Use Environment")
    col.prop(rl, "use_ao", "Use AO")
    col.prop(rl, "use_solid", "Use Surfaces")
    col.prop(rl, "use_strand", "Use Hair")

class BLayersList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        item = item

        # check for lock camera and layer is active
        view_3d = context.area.spaces.active  # Ensured it is a 'VIEW_3D' in panel's poll(), weak... :/
        use_spacecheck = False if view_3d.lock_camera_and_layers else True

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            if item.lock :
                row.active = False
            else :
                row.active = True

            # view operators
            icon = 'RESTRICT_VIEW_OFF' if context.scene.layers[item.index] else 'RESTRICT_VIEW_ON'
            #op = row.prop(item,"hide", text="", emboss=False, icon=icon)

            if item.type == 'GROUP' :
                visibility_icon = 'VISIBLE_IPO_ON' if item.visibility else 'VISIBLE_IPO_OFF'
                expand_icon = utils.custom_icons["GROUP_OPEN"].icon_id if item.expand else utils.custom_icons["GROUP_CLOSED"].icon_id
                row.prop(item,'visibility',icon =visibility_icon ,text='', emboss=False)

                row.prop(item,'expand',icon_value =expand_icon ,text='', emboss=False)
                row.prop(item, "name", text="", emboss=False )
                row.separator()
                row.operator("blayers.move_in_group",icon_value =utils.custom_icons["IN_GROUP"].icon_id ,text='',emboss= False).index = index

            else :
                row.prop(context.scene,"layers",index = item.index, text="", emboss=False, icon=icon)
                #row.prop(item,'visibility',icon ='RENDER_STILL' ,text='', emboss=False)
                if item.id in [l.id for l in context.scene.BLayers.layers if l.type == 'GROUP'] :
                    row.label(icon_value=utils.custom_icons["GROUP_TREE"].icon_id)
                    #row.separator()

                row.prop(item, "name", text="", emboss=False)
                if context.object and context.object.layers[item.index] :
                    row.label(icon='LAYER_ACTIVE')

                elif [o for o in context.scene.objects if o.layers[item.index]]:
                    row.label(icon='LAYER_USED')

            icon = "LOCKED" if item.lock else "UNLOCKED"
            op = row.prop(item,"lock", text="", emboss=False, icon=icon)
            render_icon =  'RESTRICT_RENDER_ON' if item.hide_render else  'RESTRICT_RENDER_OFF'
            row.prop(item,'hide_render',icon =render_icon ,text='', emboss=False)



        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'

    def filter_items(self, context, data, propname):
        BLayers = context.scene.BLayers
        layers = getattr(data, propname)
        helper_funcs = bpy.types.UI_UL_list

        # Default return values.
        flt_flags = []
        flt_neworder = []

        # Filtering by name
        if self.filter_name:
            flt_flags = helper_funcs.filter_items_by_name(self.filter_name, self.bitflag_filter_item, layers, "name",
                                                          reverse=self.use_filter_name_reverse)
        if not flt_flags:
            flt_flags = [self.bitflag_filter_item] * len(layers)

        #flt_flags = []
        for i,layer in enumerate(layers):
            groups = [l for l in BLayers.layers if l.type=='GROUP' and l.id == layer.id]
            if layer.type == 'LAYER' and groups and not groups[0].expand:
                flt_flags[i] = 0
            #else :
            #    flt_flags.append(self.bitflag_filter_item)



        # Reorder by name or average weight.
        if self.use_filter_sort_alpha:
            flt_neworder = helper_funcs.sort_items_by_name(layers, "name")


        #return flt_flags, flt_neworder
        return flt_flags,[]


class GPLayerPanel(bpy.types.Panel) :
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Layer Management"
    bl_category = "Layers"

    @staticmethod
    def draw(self, context):
        layout = self.layout
        BLayers = context.scene.BLayers
        #col = layout.column()

        ob = context.object


        if not BLayers.layers  :
            layout.operator("blayers.add_layer", text="New Layer")
        else:
            self.draw_layers(context, layout)


    def draw_layers(self, context, layout):
        BLayers = context.scene.BLayers
        #row = layout.row()

        main_row = layout.row()
        #box_row = box.row(align = True)
        left_col = main_row.column()
        right_col = main_row.column(align= True)

        #col = row.column(align = False)

        left_col.template_list("BLayersList", "", BLayers, "layers", BLayers, "active_index", rows=6)

        add_remove_row=  left_col.row(align=True)
        add_remove_row.label('')
        bin_icon = utils.custom_icons["BIN"].icon_id
        add_remove_row.operator("blayers.remove_layer", icon_value =bin_icon, text="")
        add_remove_row.separator()
        add_remove_row.operator("blayers.add_group", icon='NEWFOLDER', text="")
        bin_icon = utils.custom_icons["NEW_LAYER_OBJECT"].icon_id
        add_remove_row.operator("blayers.add_layer", icon_value=bin_icon, text="")
        add_remove_row.operator("blayers.add_layer", icon='NEW', text="")

        #sub = row.column(align=True)
        right_col.separator()
        right_col.separator()
        right_col.operator("blayers.layer_move", icon='TRIA_UP', text="").step = -1
        right_col.operator("blayers.layer_move", icon='TRIA_DOWN', text="").step = 1

        right_col.separator()



        right_col.operator("blayers.toogle_layer", icon='LOCKED', text="").prop = 'lock'
        right_col.operator("blayers.toogle_layer_hide", icon='RESTRICT_VIEW_OFF', text="")
        right_col.operator("blayers.toogle_layer", icon='RESTRICT_RENDER_OFF', text="").prop = 'hide_render'
        right_col.separator()
        right_col.operator("blayers.select_objects", icon='RESTRICT_SELECT_OFF', text="")
