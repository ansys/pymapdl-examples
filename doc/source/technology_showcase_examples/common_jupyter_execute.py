"""
Code to executed the first time in each techdemo which uses jupyter-execute directive.

It homogenize style and settings. If needed, you can change the configuration locally per plot.
"""

# Because of a bug in 'jupyter-execute' directive this file can only be located at one level above
# the techdemos files or at each techdemo directory.

import numpy as np
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

# jupyterlab boilerplate setup
import plotly.graph_objects as go
import pyvista

pyvista.set_plot_theme("document")
pyvista.global_theme.background = 'white'
pyvista.global_theme.font.size = 22
pyvista.global_theme.font.label_size = 22
pyvista.global_theme.font.title_size = 22
pyvista.global_theme.window_size = [400, 400]
pyvista.global_theme.axes.show = True
pyvista.global_theme.show_scalar_bar = True
pyvista.global_theme.return_cpos = False

pyvista.set_jupyter_backend("panel")

mytheme = pyvista.global_theme
