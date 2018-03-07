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

import bpy
import os
from mathutils import Matrix, Vector
import math
from math import radians
import time
from point_cloud_import_export.stop_watch import StopWatch
import numpy as np
from point_cloud_import_export.point import Point


def add_obj(data, obj_name, deselect_others=False):
    scene = bpy.context.scene

    if deselect_others:
        for obj in scene.objects:
            obj.select = False

    new_obj = bpy.data.objects.new(obj_name, data)
    scene.objects.link(new_obj)
    new_obj.select = True

    if scene.objects.active is None or scene.objects.active.mode == 'OBJECT':
        scene.objects.active = new_obj
    return new_obj

def set_object_parent(child_object_name, parent_object_name, keep_transform=False):
    child_object_name.parent = parent_object_name
    if keep_transform:
        child_object_name.matrix_parent_inverse = parent_object_name.matrix_world.inverted()

def add_empty(empty_name):
    empty_obj = bpy.data.objects.new(empty_name, None)
    bpy.context.scene.objects.link(empty_obj)
    return empty_obj

def add_points_as_mesh(points, add_points_as_particle_system, mesh_type, point_extent, default_point_color):
    print("Adding Points: ...")
    stop_watch = StopWatch()
    name = "Point_Cloud"
    mesh = bpy.data.meshes.new(name)
    mesh.update()
    mesh.validate()

    point_world_coordinates = [tuple(point.coord) for point in points]

    mesh.from_pydata(point_world_coordinates, [], [])
    meshobj = add_obj(mesh, name)

    if add_points_as_particle_system or add_meshes_at_vertex_positions:
        print("Representing Points in the Point Cloud with Meshes: True")
        print("Mesh Type: " + str(mesh_type))

        # The default size of elements added with 
        #   primitive_cube_add, primitive_uv_sphere_add, etc. is (2,2,2)
        point_scale = point_extent * 0.5 

        bpy.ops.object.select_all(action='DESELECT')
        if mesh_type == "PLANE":
            bpy.ops.mesh.primitive_plane_add(radius=point_scale)
        elif mesh_type == "CUBE":
            bpy.ops.mesh.primitive_cube_add(radius=point_scale)
        elif mesh_type == "SPHERE":
            bpy.ops.mesh.primitive_uv_sphere_add(radius=point_scale)
        else:
            bpy.ops.mesh.primitive_uv_sphere_add(radius=point_scale)
        viz_mesh = bpy.context.object

        if add_points_as_particle_system:
            
            if not viz_mesh.data.materials:
                material_name = "PointCloudMaterial"
                material = bpy.data.materials.get(material_name)
                if material is None:
                    material = bpy.data.materials.new(name=material_name)
                material.diffuse_color = (default_point_color[0] / 255.0, default_point_color[1] / 255.0, default_point_color[2] / 255.0) 
                viz_mesh.data.materials.append(material)
                
                # enable cycles, otherwise the material has no nodes
                bpy.context.scene.render.engine = 'CYCLES'
                material = bpy.data.materials['PointCloudMaterial']
                material.use_nodes = True
                node_tree = material.node_tree
                if 'Material Output' in node_tree.nodes:
                    material_output_node = node_tree.nodes['Material Output']
                else:
                    material_output_node = node_tree.nodes.new('ShaderNodeOutputMaterial')
                if 'Diffuse BSDF' in node_tree.nodes:
                    diffuse_node = node_tree.nodes['Diffuse BSDF']
                else:
                    diffuse_node = node_tree.nodes.new("ShaderNodeBsdfDiffuse")
                node_tree.links.new(diffuse_node.outputs['BSDF'], material_output_node.inputs['Surface'])
                
                if 'Image Texture' in node_tree.nodes:
                    image_texture_node = node_tree.nodes['Image Texture']
                else:
                    image_texture_node = node_tree.nodes.new("ShaderNodeTexImage")
                node_tree.links.new(image_texture_node.outputs['Color'], diffuse_node.inputs['Color'])
                
                vis_image_height = 1
                
                # To view the texture we set the height of the texture to vis_image_height 
                image = bpy.data.images.new('ParticleColor', len(point_world_coordinates), vis_image_height)
                
                print('len(points): ' + str(len(points)))
                print(type(image.pixels))
                
                # working on a copy of the pixels results in a MASSIVE performance speed
                local_pixels = list(image.pixels[:])
                print(type(local_pixels))
                
                num_points = len(points)
                
                for j in range(vis_image_height):
                    for point_index, point in enumerate(points):
                        column_offset = point_index * 4     # (R,G,B,A)
                        row_offset = j * 4 * num_points
                        color = point.color 
                        # Order is R,G,B, opacity
                        local_pixels[row_offset + column_offset] = color[0] / 255.0
                        local_pixels[row_offset + column_offset + 1] = color[1] / 255.0
                        local_pixels[row_offset + column_offset + 2] = color[2] / 255.0
                        # opacity (0 = transparent, 1 = opaque)
                        #local_pixels[row_offset + column_offset + 3] = 1.0    # already set by default   
                    
                image.pixels = local_pixels[:]  
                
                image_texture_node.image = image
                particle_info_node = node_tree.nodes.new('ShaderNodeParticleInfo')
                divide_node = node_tree.nodes.new('ShaderNodeMath')
                divide_node.operation = 'DIVIDE'
                node_tree.links.new(particle_info_node.outputs['Index'], divide_node.inputs[0])
                divide_node.inputs[1].default_value = num_points
                shader_node_combine = node_tree.nodes.new('ShaderNodeCombineXYZ')
                node_tree.links.new(divide_node.outputs['Value'], shader_node_combine.inputs['X'])
                node_tree.links.new(shader_node_combine.outputs['Vector'], image_texture_node.inputs['Vector'])
            
            if len(meshobj.particle_systems) == 0:
                meshobj.modifiers.new("particle sys", type='PARTICLE_SYSTEM')
                particle_sys = meshobj.particle_systems[0]
                settings = particle_sys.settings
                settings.type = 'HAIR'
                settings.use_advanced_hair = True
                settings.emit_from = 'VERT'
                settings.count = len(point_world_coordinates)
                # The final object extent is hair_length * obj.scale 
                settings.hair_length = 100           # This must not be 0
                settings.use_emit_random = False
                settings.render_type = 'OBJECT'
                settings.dupli_object = viz_mesh
            
        bpy.context.scene.update
    else:
        print("Representing Points in the Point Cloud with Meshes: False")
    print("Duration: " + str(stop_watch.get_elapsed_time()))
    print("Adding Points: Done")





from bpy.props import (CollectionProperty,
                       StringProperty,
                       BoolProperty,
                       EnumProperty,
                       FloatProperty,
                       IntProperty,
                       IntVectorProperty
                       )

from bpy_extras.io_utils import (ImportHelper,
                                 ExportHelper,
                                 axis_conversion)

class ImportPLY(bpy.types.Operator, ImportHelper):
    """Load a PLY file"""
    bl_idname = "import_scene.ply"
    bl_label = "Import PLY"
    bl_options = {'UNDO'}

    files = CollectionProperty(
        name="File Path",
        description="File path used for importing the PLY file",
        type=bpy.types.OperatorFileListElement)

    directory = StringProperty()

    import_points = BoolProperty(
        name="Import Points",
        description = "Import Points", 
        default=True)
    add_points_as_particle_system = BoolProperty(
        name="Add Points as Particle System (Recommended)",
        description="Use a particle system to represent vertex position with an object",
        default=True)
    mesh_items = [
        ("CUBE", "Cube", "", 1),
        ("SPHERE", "Sphere", "", 2),
        ("PLANE", "Plane", "", 3)
        ]
    mesh_type = EnumProperty(
        name="Mesh Type",
        description = "Select the vertex representation mesh type.", 
        items=mesh_items)
    default_point_color = IntVectorProperty(
        name="Default Color", 
        description = "Color",
        default=(255,255,255),
        min=0,
        max=255)

    point_extent = FloatProperty(
        name="Initial Point Extent (in Blender Units)", 
        description = "Initial Point Extent for meshes at vertex positions",
        default=0.01)

    filename_ext = ".ply"
    filter_glob = StringProperty(default="*.ply", options={'HIDDEN'})

    def execute(self, context):
        paths = [os.path.join(self.directory, name.name)
                 for name in self.files]
        if not paths:
            paths.append(self.filepath)

        from point_cloud_import_export.ply_file_handler import PLYFileHandler

        for path in paths:

            points = PLYFileHandler.parse_ply_file(path)

            print("Number points: " + str(len(points)))
            if self.import_points:
                add_points_as_mesh(points, self.add_points_as_particle_system, self.mesh_type, self.point_extent, self.default_point_color)

        return {'FINISHED'}
