"""
Code to executed the first time in each techdemo which uses jupyter-execute directive.

It homogenize style and settings. If needed, you can change the configuration locally per plot.
"""

import warnings

import numpy as np  # noqa: F401
import pandas as pd  # noqa: F401

warnings.filterwarnings("ignore")

# jupyterlab boilerplate setup
import plotly.graph_objects as go  # noqa: F401
import pyvista

pyvista.set_plot_theme("document")
pyvista.global_theme.background = "white"
pyvista.global_theme.font.size = 22
pyvista.global_theme.font.label_size = 22
pyvista.global_theme.font.title_size = 22
pyvista.global_theme.window_size = [400, 400]
pyvista.global_theme.axes.show = True
pyvista.global_theme.show_scalar_bar = True
pyvista.global_theme.return_cpos = False

pyvista.set_jupyter_backend("trame")

mytheme = pyvista.global_theme


from ansys.mapdl.core import examples
from ansys.mapdl.core.examples.downloads import download_vtk_rotor, download_tech_demo_data

cdbfile = download_tech_demo_data("td-28", "fsw.cdb")
# Generating geometry, just for plotting purposes.
# The elements and nodes are going to be taken from the cdb file.

from ansys.mapdl.core import launch_mapdl

mapdl = launch_mapdl()
print(mapdl)

mapdl.clear()
mapdl.prep7()
mapdl.cdread('db', cdbfile)
# ***** Problem parameters ********
l = 76.2e-03     # Length of each plate,m
w = 31.75e-03    # Width of each plate,m
t = 3.18e-03     # Thickness of each plate,m
r1 = 7.62e-03    # Shoulder radius of tool,m
h = 15.24e-03    # Height of tool, m
l1 = r1          # Starting location of tool on weldline
l2 = l-l1
tcc1 = 2e06      # Thermal contact conductance b/w plates,W/m^2'C
tcc2 = 10        # Thermal contact conductance b/w tool &
# workpiece,W/m^2'C
fwgt = 0.95      # weight factor for distribution of heat b/w tool
# & workpiece
fplw = 0.8       # Fraction of plastic work converted to heat
uz1 = t/4000     # Depth of penetration,m
nr1 = 3.141593*11  # No. of rotations in second load step
nr2 = 3.141593*45  # No. of rotations in third load step
uy1 = 60.96e-03  # Travelling distance along weld line
tsz = 0.01       # Time step size   
# ==========================================================
# * Geometry
# ==========================================================
# * Node for pilot node
mapdl.n(1, 0, 0, h)
# * Workpiece geometry (two rectangular plates)
mapdl.block(0, w, -l1, l2, 0, -t)
mapdl.block(0, -w, -l1, l2, 0, -t)
# * Tool geometry
mapdl.cyl4(0, 0, r1, 0, r1, 90, h)
mapdl.cyl4(0, 0, r1, 90, r1, 180, h)
mapdl.cyl4(0, 0, r1, 180, r1, 270, h)
mapdl.cyl4(0, 0, r1, 270, r1, 360, h)
mapdl.vglue(3, 4, 5, 6);

# Plotting geometry
mapdl.geometry.areas.plot()

    
# Plotting mesh
mapdl.allsel()
pl = pyvista.Plotter()
pl.add_mesh(mapdl.mesh.grid, show_edges=True, color='gray')
pl.show()
pl.close()

mapdl.allsel("all")

# Plotting geometry
pl = pyvista.Plotter()
for elem, color in zip((170, 174),('red', 'blue')):
    mapdl.esel("s", "ename","", elem)
    esurf = mapdl.mesh._grid.linear_copy().extract_surface().clean()
    print(color)
    pl.add_mesh(
        mesh=esurf,
        label=None,
        show_edges=True,
        show_scalar_bar=False,
        style='surface',
        color=color
    )

pl.show()

## figure 28.5
mapdl.allsel("all")
mapdl.esel('s', 'mat', '', 2)
mapdl.nsle('s')

pl = mapdl.eplot(
    plot_bc=True,
    bc_glyph_size=0.002,
    return_plotter=True,
    show_axes=False,
    theme=mytheme
)

for elem, color in zip((170, 174), ('red', 'blue')):

    mapdl.esel('s', 'mat', '', 2)
    mapdl.esel("r", "ename", "", elem)
    esurf = mapdl.mesh._grid.linear_copy().extract_surface().clean()
    if mapdl.mesh.n_elem != 1:
        print("True")
        pl.add_mesh(
            meshes= mapdl.mesh.grid,
            points=esurf,
            show_edges=True, 
            show_scalar_bar=False,
            style='surface', 
            color=color
        )

pl.show()