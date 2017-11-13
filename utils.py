import bpy

def redraw_areas():
    for area in bpy.context.screen.areas :
        area.tag_redraw()
