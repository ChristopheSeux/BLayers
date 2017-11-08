import bpy

class BLayersList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        item = item

        # check for lock camera and layer is active
        view_3d = context.area.spaces.active  # Ensured it is a 'VIEW_3D' in panel's poll(), weak... :/
        use_spacecheck = False if view_3d.lock_camera_and_layers else True

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            # view operators
            icon = 'RESTRICT_VIEW_OFF' if context.scene.layers[item.index] else 'RESTRICT_VIEW_ON'
            #op = row.prop(item,"hide", text="", emboss=False, icon=icon)
            row.prop(context.scene,"layers",index = item.index, text="", emboss=False, icon=icon)

            row.prop(item, "name", text="", emboss=False)
            #row.label(str(item.index))
            # lock operator
            if context.object and context.object.layers[item.index] :
                row.label(icon='LAYER_ACTIVE')

            icon = 'LOCKED' if item.lock else 'UNLOCKED'
            op = row.prop(item,"lock", text="", emboss=False, icon=icon)



        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'

class GPLayerPanel(bpy.types.Panel) :
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Layer Management"
    bl_category = "Layers"
    bl_context = "objectmode"

    @classmethod
    def poll(self, context):
        EDIT_MODES = {'EDIT_MESH', 'EDIT_CURVE', 'EDIT_SURFACE', 'EDIT_METABALL', 'EDIT_TEXT', 'EDIT_ARMATURE'}
        return ((getattr(context, "mode", 'EDIT_MESH') not in EDIT_MODES) and
                (context.area.spaces.active.type == 'VIEW_3D'))

    @staticmethod
    def draw(self, context):
        layout = self.layout
        BLayers = context.scene.BLayers
        col = layout.column()

        ob = context.object


        if not BLayers.layers  :
            layout.operator("blayers.add_layer", text="New Layer")
        else:
            self.draw_layers(context, layout)


    def draw_layers(self, context, layout):
        BLayers = context.scene.BLayers
        row = layout.row()

        col = row.column(align = True)



        col.template_list("BLayersList", "", BLayers, "layers", BLayers, "active_index", rows=6)

        rightCol = row.column()

        sub = rightCol.column(align=True)
        add = sub.operator("blayers.add_layer", icon='ZOOMIN', text="")
        remove = sub.operator("blayers.remove_layer", icon='ZOOMOUT', text="")

        if len(BLayers.layers) > 1:
            rightCol.separator()

            sub = rightCol.column(align=True)
            sub.operator("blayers.layer_move", icon='TRIA_UP', text="").step = -1
            sub.operator("blayers.layer_move", icon='TRIA_DOWN', text="").step = 1

            rightCol.separator()

            sub = rightCol.column(align=True)
            #add = sub.operator("blayers.add_remove_layer", icon='FILE_FOLDER', text="")
            #add.operation,add.layer,add.type = "ADD", repr(gpl),'GROUP'

            sub.operator("blayers.toogle_layer_lock", icon='LOCKED', text="")
            sub.operator("blayers.toogle_layer_hide", icon='RESTRICT_VIEW_OFF', text="")
