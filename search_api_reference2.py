import bpy
from bpy.types import Operator
from bpy.props import (
    EnumProperty,StringProperty
)
import os

bl_info = {
    "name": "Search Online Reference",
    "description": "Search Online reference",
    "author": "tintwotin",
    "version": (1, 1),
    "blender": (2, 83, 0),
    "location": "Text Editor > Edit > Search API Reference",
    "wiki_url": "https://github.com/tin2tin/Search-API-Reference",
    "tracker_url": "",
    "category": "Text Editor"}

def addToClipBoard(text):
    command = 'echo | set /p nul=' + text.strip() + '| clip'
    os.system(command)

class TEXT_OT_online_reference(Operator):
    '''Search for current word or selection online'''
    bl_idname = "text.online_reference"
    bl_label = "Search Online"
    bl_options = {"REGISTER", "UNDO"}

    type: EnumProperty(
        name="Search Online",
        description="Search for current word or selection online",
        options={'ENUM_FLAG'},
        items=(
             ('API', "API Reference", "Search the API reference"),
             ('PYTHON', "Python Reference", "Search the Python reference"),
             ('STACKEXCHANGE', "Stack Exchange", "Search Stack Exchange"),
             ('SOURCECODE', "Source Code", "Blender Source Code"),
             ('GITHUB', "Github", "Github"),
             ),
             default={'API'},
        )
    s: StringProperty(default='')


    def execute(self, context):

        addToClipBoard('') ##empty clipboard     

        if context.area.type == 'TEXT_EDITOR':
            text=context.space_data.text

            current_character = text.current_character
            select_end_character = text.select_end_character

            if current_character == select_end_character:            
                bpy.ops.text.select_word()
                bpy.ops.text.copy()
            else:
                bpy.ops.text.copy()

        if context.area.type == 'CONSOLE':            
            sc=context.space_data      

            if sc.select_start==sc.select_end:
                self.report({'WARNING'}, "Selection is missing")

                return {'CANCELLED'}
            else:
                bpy.ops.console.copy() 


        self.s = bpy.context.window_manager.clipboard


        if self.type == {'API'}:
            bpy.ops.wm.url_open(url="https://docs.blender.org/api/2.80/search.html?q="+self.s)
        if self.type == {'STACKEXCHANGE'}:
            bpy.ops.wm.url_open(url="https://blender.stackexchange.com/search?q="+self.s)
        if self.type == {'PYTHON'}:
            bpy.ops.wm.url_open(url="https://docs.python.org/3/search.html?q="+self.s)
        if self.type == {'SOURCECODE'}:
            bpy.ops.wm.url_open(url="https://developer.blender.org/diffusion/B/browse/master/?grep="+self.s)
        if self.type == {'GITHUB'}:
            bpy.ops.wm.url_open(url="https://www.google.com/search?q=intext%3A%22"+self.s+"%22+ext%3Apy+bpy+site%3Agithub.com")

        return {'FINISHED'}


def panel_append(self, context):
    self.layout.separator()
    self.layout.operator_menu_enum("text.online_reference", "type")


def register():
    bpy.utils.register_class(TEXT_OT_online_reference)
    bpy.types.TEXT_MT_edit.append(panel_append)
    bpy.types.TEXT_MT_context_menu.append(panel_append)
    bpy.types.CONSOLE_MT_console.append(panel_append)

def unregister():
    bpy.utils.unregister_class(TEXT_OT_online_reference)
    bpy.types.TEXT_MT_edit.remove(panel_append)
    bpy.types.TEXT_MT_context_menu.remove(panel_append)
    bpy.types.CONSOLE_MT_console.remove(panel_append)


if __name__ == "__main__":
    register()