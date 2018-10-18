# Blender-Import-Point-Cloud-Addon
Blender addon to import point clouds from PLY files.

Tested for Blender 2.78 and 2.79 as well as Ubuntu 14.04 and Windows 10.

This addon uses the https://github.com/dranjan/python-plyfile library to parse plyfiles.

## Import
In Blender use File/Import/Point Cloud PLY Import (.ply) to import the PLY file. 
There is an option to represent each vertex position with an object using a particle system. This allows you to render the point cloud. A single texture is used to store the color of all particles. The color of the points are shown, if the 3D view is set to "Material".


## Example
This repository contains an example PLY file. The imported result looks as follows.
![alt text](https://github.com/SBCV/Blender-Import-Point-Cloud-Addon/blob/master/import_ply.jpg)

## Adjust Scale of Points (after importing)
For each imported point cloud two objects are created. The first object represents the structure of the point cloud and the second object defines the shape of the points in the point cloud. Rescaling of the second object will also update the size of the points in the point cloud.

## Installation
Clone the addon:
```
git clone https://github.com/SBCV/Blender-Import-Point-Cloud-Addon.git
```
Compress the folder "point_cloud_import_export" in "Blender-Import-Point-Cloud-Addon" to a zip archive. 
The final structure must look as follows:
- point_cloud_import_export.zip/  
	- point_cloud_import_export/  
		- ply_file_handler.py  
		- __init__.py  
		- import_ply_op.py  
		- ...  


