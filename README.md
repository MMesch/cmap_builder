# blender colormap builder

## Overview
This is a blender script that allows to generate colormaps in the uniform
colorspace CAM02-UCS (thank you colorspacious) by drawing a 3d spline path
or a 3d spline surface in blender.

## Installation
1. clone the git repository somewhere on your system: `git clone ...`
2. install a python version that is compatible with blender (e.g. python 3.5.1 for
   blender 2.77a) and install the
   `colorspacious` module with `pip install colorspacious`.
   This is straightforward with anaconda python: first make a virtual
   environment with `conda create -n blender python=3.5`. 
   Then do `source activate blender` to activate the environment and install
   colorspacious with `pip install colorspacious`

## Instruction, generate Gamut surface mesh
1. open the project `colormaps.blend` with blender.
2. in the python script `Add_Gamut` (can be selected on in the footline
   of the text window on the right), change the path to point to your
   colorspacious module. 
   E.g.: `sys.path.append('home/myname/anaconda2/envs/blender/lib/python3.5/site-packages'')`
3. run the script with `alt + p` when the text window is active or click
   the `run script` button in the footline of the text editor window. A new Gamut surface is generated.

## Instructions, 1d colormap
1. open the project `colormaps.blend` with blender.
2. in the python script `path_to_colormap` (can be selected on in the footline
   of the text window on the right), change the path to point to your
   colorspacious module. 
   E.g.: `sys.path.append('home/myname/anaconda2/envs/blender/lib/python3.5/site-packages'')`
3. you can now edit the control points of the bezier curves in the 3d window.
   Make sure that your window is in `edit mode` to do this. You might want to
   delete the surface and bezier curves that you don't need to make some space.
   If you are done positioning your curve,
   make sure that it is selected and run the python script by pushing on `run script`
   or pressing `alt + p` when the script window is active. The colormap on
   the bottom left should now update.

## Instructions, 2d colormap

1. open the existing project `colormaps.blend` with blender.
2. in the python script `nurbs_to_colormap`, change the path to point to your
   colorspacious module. E.g.: `sys.path.append('home/myname/anaconda2/envs/blender/lib/python3.5/site-packages'')`
3. you can now edit the control points of the nurbs surface in the 3d window
   (make sure that your window is in `edit mode` to do this), or you can add
   a new nurbs surface in `object mode`. The u and v resolution parameters
   control the axial and angular sampling of the cylinder and can be reduced
   while editing. The spline order controls the smoothness of the surface.
4. If you are done positioning the surface,
   make sure that it is selected and run the python script by pushing on `run script`
   or pressing `alt + p` when the script window is active. Be careful, the script
   generates a duplicate of the nurbs surface that you can delete after the
   colormap has been generated. The colormap on the bottom left should now update.


## Gallery:
![blender interface surface](blender_example2.png)
![blender interface path](blender_example.png)


## included colormaps
Colorsurfaces need to make a few compromises To use the maximum extend of the
Gamut colorspace while at the same time remaining as smooth as possible.
Especially at convergent points around black (zero lightness) and white (max
lightness), the topology of the color surfaces has to be as smooth as possible,
meaning the lightness of different hues should vary as little as possible. This
ensures that maximum and minimums in displayed functions remain round and don't
become star-shaped or shifted towards darker colors like blue and red. At 0.5,
the color surfaces can vary a in lightness to make use of strongy saturated
colors.

### rendering:
Wheel2d is a 2d colormap that goes from black to white with maximum saturated
colors around 0.5.
![wheel2d](wheel2d.png)

Darkwheel2d is a 2d colormap that goes from black to light and saturated colors.
Exclusion of white allows for better coverage of the saturated corners of the
Gamut cube.
![darkwheel2d](darkwheel2d.png)

### comparison with:
![2d colormaps](comparison.png)
