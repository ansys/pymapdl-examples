# %matplotlib inline

# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# ref_example_td_062:
#
# Inverse-Solving Analysis of a Cardiovascular Structure
# ---------------------------------------------------------------------------------------
#
# Problem description:
#  - This example problem demonstrates the capabilities and advantages of using a
#    nonlinear static analysis with inverse solving to investigate the biomechanics
#    of a cardiovascular system.
#
#    Finite element models of cardiovascular system components (such as the heart
#    valve or blood vessels) are based on in vivo organ geometries obtained from
#    3D imaging systems such as computed tomography (CT) or magnetic resonance
#    imaging (MRI).
#
#    Although medical imaging techniques offer accurate in vivo visualization of 3D
#    patient-specific geometries, the geometries are under a loaded state
#    (for example, in the presence of blood pressure) and lack in vivo stress/strain
#    field information. Therefore, a nonlinear analysis performed directly on the
#    geometry to simulate additional loading leads to inaccurate results.
#
#    In such cases, an inverse-solving analysis uses input geometry consisting of images
#    where the models are already in a deformed shape under applied loads. The material
#    properties and applied loads are known. The analysis can then determine the following:
#
#   - The organ geometries at zero-pressure state (zero-pressure configuration).
#   - The stress and strain fields on the in vivo organ geometries (the input geometries).
#   - The behavior and response of the organ geometries when increasing the loading
#     and taking accounting for prestressed effects.
#

# Importing the `launch_mapdl` function from the `ansys.mapdl.core` module

from ansys.mapdl.core import launch_mapdl
from ansys.mapdl.core.examples.downloads import download_tech_demo_data

# Start MAPDL as a service.

mapdl = launch_mapdl(loglevel="WARNING", print_com=True)

# Download the CDB file of aortic lumen.

aorta_mesh_file = download_tech_demo_data(
    "td-62", "inverse_analysis_cardiovascular_structure.cdb"
)

# Entering the PREP7 processor in MAPDL instance.

mapdl.prep7()

# Reads a CDB file of solid model and database information into the database.

mapdl.cdread("comb", fname=aorta_mesh_file)

# Selects all entities with a single command.

mapdl.allsel("all", "all")

# The model is meshed mostly with the higher-order hexahedral SOLID186 elements
# (about 99.4 percent of the total mesh), as shown in the following figure. However, it
# also has relatively a small number of tetrahedral SOLID187
# elements (about 0.6 percent of the total mesh).
#
# Mesh of the Abdominal Aorta Model

mapdl.eplot(background="w")

# The mesh consists of 62123 elements with 4 elements to represent the wall thickness and
# at least 52 elements (or more) in the circumferential direction at most locations.
# Mixed u-P element formulation is enabled (KEYOPT(6) = 1).

# Finish
# ~~~~~~
# Exits from a pre-processor.

mapdl.finish()

# Analysis and Solution Controls
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Enter solution processor and specify solution controls.

mapdl.slashsolu()

# The analysis for this problem is performed in two load steps:
#
# Load Step 1 (Inverse-Solving) – A nonlinear static analysis with inverse solving (INVOPT,ON)
# is performed on the input geometry of the model (at end-diastolic pressure (80 mm Hg)) to
# determine the zero-pressure geometry of the model and to obtain the stress/strain results
# on the input geometry.
#
# After an inverse-solving load step, the solver generally allows an analysis to continue
# as forward-solving in a new load step. You can modify existing loads or apply new loads
# in the forward-solving step. For more information, see Reverting to Forward Solving and
# Continuing the Analysis as a New Load Step in the Structural Analysis Guide.
#
# Load Step 2 (Forward-Solving) – To solve the model for end-systolic pressure (120 mm Hg),
# the solution continues using forward solving (INVOPT,OFF). The pressure load is increased
# from 80 mm Hg to 120 mm Hg. Continuing the solution as a new load step following the
# inverse-solving load step eliminates a step in the simulation, allowing for a more
# efficient analysis.

mapdl.antype(0)

# Turn on large deflection effects.

mapdl.nlgeom("on")

# Define "Sparse" solver option.

# +
mapdl.eqslv("sparse", keepfile="1")

mapdl.cntr(
    "print", 1
)  # print out contact info and also make no initial contact an error
mapdl.dmpoption("emat", "no")  # Don't combine emat file for DANSYS
mapdl.dmpoption("esav", "no")  # Don't combine esav file for DANSYS
# -

# Turn on "Inverse-Solving" option for Initial Steps.

mapdl.run("invopt,on")

# Controls file writing for multiframe restarts.

mapdl.nldiag("cont", "iter")  # print out contact info each equilibrium iteration
mapdl.rescontrol("define", "last", "last", "", "dele")  # Program Controlled

# Specify surface "pressures" loads.

mapdl.esel("u", "ename", "", 153, 156)
mapdl.sf("_CM968PRES", "pres", "%_loadvari968 %")
mapdl.esel("all")
mapdl.nopr()
mapdl.gopr()

# Turned on automatic time stepping.

mapdl.autots("on")

# Specifies the number of substeps to be taken this load step.
# Note: Please be aware that the number of substeps is decreased to reduce the computational effort.

# mapdl.nsubst(nsbstp='10', nsbmx='1000', nsbmn='5', carry="OFF")
mapdl.nsubst(nsbstp="2", nsbmx="2", nsbmn="2", carry="OFF")

# Sets the time for a first load step.

mapdl.time(time="1.0")

# Controls the solution data written to the database.

mapdl.outres("erase")
mapdl.outres("all", "none")
mapdl.outres("nsol", "all")
mapdl.outres("rsol", "all")
mapdl.outres("eangl", "all")
mapdl.outres("etmp", "all")
mapdl.outres("veng", "all")
mapdl.outres("strs", "all")
mapdl.outres("epel", "all")
mapdl.outres("eppl", "all")
mapdl.outres("cont", "all")

# Solve
# ~~~~~
# Solve the load step 1 (inverse-solving).

# mapdl.solve()

# Solution Control for the load step 2 (forward-solving).

# Turned on automatic time stepping.

mapdl.autots("on")

# Specifies the number of substeps to be taken this load step.
# Note: Please be aware that the number of substeps is decreased to reduce the computational effort.

# mapdl.nsubst(nsbstp='10', nsbmx='1000', nsbmn='5', carry="OFF")
mapdl.nsubst(nsbstp="2", nsbmx="2", nsbmn="2", carry="OFF")

# Sets the time for the second load step.

mapdl.time(time="2.0")

# Turn off "Inverse-Solving" option for the second steps.

mapdl.run("invopt,off")

# Controls the solution data written to the database.

mapdl.outres("erase")
mapdl.outres("all", "none")
mapdl.outres("nsol", "all")
mapdl.outres("rsol", "all")
mapdl.outres("eangl", "all")
mapdl.outres("etmp", "all")
mapdl.outres("veng", "all")
mapdl.outres("strs", "all")
mapdl.outres("epel", "all")
mapdl.outres("eppl", "all")
mapdl.outres("cont", "all")

# Solve
# ~~~~~
# Solve the load step 2 (forward-solving).

# mapdl.solve()

# Finish
# ~~~~~~
# Exits from a solution processor.

mapdl.finish()

# Post-processing
# ~~~~~~~~~~~~~~~
# Enter post-processor to compute results quantities.

mapdl.post1()

# Settings for reverse video plot

mapdl.rgb("index", 100, 100, 100, 0)
mapdl.rgb("index", 80, 80, 80, 13)
mapdl.rgb("index", 60, 60, 60, 14)
mapdl.rgb("index", 0, 0, 0, 15)

# Defines the type of graphics display. Activate "Power" graphics.

mapdl.graphics("power")

# Defines the data set to be read from the results file.

mapdl.set(lstep="1")

mapdl.show("png", "rev")

# The deformed shape of the abdominal aorta model after the first load step
# is the zero-pressure geometry:
#
# Total Deformation (USUM) After Inverse Solving (First Load Step)

mapdl.plnsol("u", "sum", 1, 1)
mapdl.get("max_usum_first_loadstep", "plnsol", 0, "max")

# In addition to the zero-pressure geometry, the inverse-solving load step
# also gives the stress/strain results of the input geometry at end-diastolic pressure (80 mm Hg):

# Maximum Principal Stress After Inverse Solving (First Load Step)

mapdl.plnsol("s", 1)
mapdl.get("max_s1_first_loadstep", "plnsol", 0, "max")

# Maximum Principal Strain After Inverse Solving (First Load Step)

mapdl.plnsol("epel", 1)
mapdl.get("max_epel1_first_loadstep", "plnsol", 0, "max")

mapdl.show("close")

# Defines the data set to be read from the results file.

mapdl.set(lstep="last")

mapdl.show("png", "rev")

# In the second load step, the analysis is continued via forward solving (INVOPT,OFF)
# and the pressure load is increased until it reaches end-systolic pressure (120 mm Hg):
#
# Total Deformation (USUM) After Forward Solving (Second Load Step)

mapdl.plnsol("u", "sum", 1, 1)
mapdl.get("max_usum_second_loadstep", "plnsol", 0, "max")

# Maximum Principal Stress After Forward Solving (Second Load Step)

mapdl.plnsol("s", 1)
mapdl.get("max_s1_second_loadstep", "plnsol", 0, "max")

# Maximum Principal Strain Plot of the Abdominal Aorta Model at End-Systolic Pressure (120 mm Hg)

mapdl.plnsol("epel", 1)
mapdl.get("max_epel1_second_loadstep", "plnsol", 0, "max")

mapdl.show("close")

# Lists the parameters.

mapdl.starstatus()

# Finish
# ~~~~~~
# Exits from a post-processor.

mapdl.finish()

# Exit
# ~~~~
# Exit MAPDL instance.

mapdl.exit()
