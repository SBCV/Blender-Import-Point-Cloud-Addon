'''
Copyright (C) 2018 Sebastian Bullinger


Created by Sebastian Bullinger

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "Point Cloud Import Addon (PLY)",
    "description": "Allows to import point clouds (.ply).",
    "author": "Sebastian Bullinger",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "View3D",
    "warning": "",
    "wiki_url": "",
    "category": "Import-Export" }


import bpy


# load and reload submodules
##################################

import importlib
from . import developer_utils
importlib.reload(developer_utils)
modules = developer_utils.setup_addon_modules(__path__, __name__, "bpy" in locals())

# The root dir is blenders addon folder, 
# therefore we need the "nvm_import_export" specifier for this addon  
from point_cloud_import_export.import_ply_op import ImportPLY

# register
##################################

def menu_func_import(self, context):
    self.layout.operator(ImportPLY.bl_idname, text="Point Cloud PLY Import (.ply)")


def register():
    bpy.utils.register_class(ImportPLY)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    print("Registered {} with {} modulse".format(bl_info["name"], len(modules)))

def unregister():
    bpy.utils.unregister_class(ImportPLY)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    print("Unregistered {}".format(bl_info["name"]))

if __name__ == '__main__':
    print('main called')
    register()
