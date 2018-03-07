# Blender-Import-Point-Cloud-Addon
Blender addon to import point clouds from PLY files.

Tested for Blender 2.78 and 2.79 as well as Ubuntu 14.04 and Windows 10.


Import
=====
In Blender use File/Import/Point Cloud PLY Import (.ply) to import the PLY file. 
There is an option to represent each vertex position with an object using a particle system. This allows you to render the point cloud. A single texture is used to store the color of all particles. The color of the points are shown, if the 3D view is set to "Material".


Installation
============
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


License
=====
Blender-Import-Point-Cloud-Addon
Copyright (C) 2018  Sebastian Bullinger

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
