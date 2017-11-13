import bpy
import bpy.utils.previews
from os.path import join,basename,dirname,splitext
from os import listdir

def redraw_areas():
    for area in bpy.context.screen.areas :
        area.tag_redraw()

def get_icons():
    get_icons.custom_icons = bpy.utils.previews.new()
    icons_dir = join(dirname(__file__),'icons')
    for icon in listdir(icons_dir) :
        get_icons.custom_icons.load(splitext(icon)[0].upper(), join(icons_dir, icon), 'IMAGE',force_reload=True)

    get_icons.custom_icons.update()
