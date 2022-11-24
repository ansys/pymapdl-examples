""".. _ref_cardiovascular_stent_simulation:

Cardiovascular Stent Simulation
===============================

This example problem shows how to simulate stent-artery interaction during and
after stent placement in an occluded artery.

The analysis exposes advanced modeling techniques using PyMAPDL such as:

* Contact
* Element birth and death
* Mixed u-P formulation
* Nonlinear stabilization

This example is inspired from the model and analysis defined in Chapter 25 of
the Mechanical APDL Technology Showcase Manual.

Additional Packages Used
------------------------

* `Matplotlib <https://matplotlib.org>`_ is used for plotting purposes.

"""

###############################################################################
# Setting up model
# ----------------
#
# Test
#
# Starting MAPDL as a service and importing an external model
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from ansys.mapdl.core import launch_mapdl

# start MAPDL as a service
mapdl = launch_mapdl()
print(mapdl)


###############################################################################
# Defining material properties
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# define 316L Stainless steel
mapdl.prep7()
mapdl.mptemp()
mapdl.mptemp(sloc="1", t1="0")
mapdl.mpdata(lab="EX", mat="1", c1="200e3")
mapdl.mpdata(lab="PRXY", mat="1", c1="0.3")
mapdl.mptemp()
mapdl.mptemp(sloc="1", t1="0")
mapdl.mpdata(lab="DENS", mat="1", c1="8000e-9")


###############################################################################
# Defining material properties
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# define 316L Stainless steel
mapdl.prep7()
mapdl.mptemp()
mapdl.mptemp(sloc="1", t1="0")
mapdl.mpdata(lab="EX", mat="1", c1="200e3")
mapdl.mpdata(lab="PRXY", mat="1", c1="0.3")
mapdl.mptemp()
mapdl.mptemp(sloc="1", t1="0")
mapdl.mpdata(lab="DENS", mat="1", c1="8000e-9")


###############################################################################
# Defining element types
# ~~~~~~~~~~~~~~~~~~~~~~

# for straight line segments
mapdl.et(itype="1", ename="beam189")
mapdl.sectype(secid="1", type_="beam", subtype="csolid")
mapdl.secdata(val1=0.05)

# for arcs
mapdl.et(itype="2", ename="beam189")
mapdl.sectype(secid="2", type_="beam", subtype="csolid")
mapdl.secdata(val1=0.05)


###############################################################################
# Defining 5-parameter Mooney-Rivlin hyperelastic artery material model
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

c10 = 18.90e-3
c01 = 2.75e-3
c20 = 590.43e-3
c11 = 857.2e-3
nu1 = 0.49
dd = 2 * (1 - 2 * nu1) / (c10 + c01)

mapdl.tb(lab="hyper", mat="2", npts="5", tbopt="mooney")
mapdl.tbdata(stloc="1", c1="c10", c2="c01", c3="c20", c4="c11", c6="dd")


###############################################################################
# Defining linear elastic material model for stiff calcified plaque
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

mapdl.mp(lab="EX", mat="3", c0="00219e3")
mapdl.mp(lab="NUXY", mat="3", c0="0.49")

###############################################################################
# Define Solid185 element type to mesh both the artery and plaque
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# For artery
mapdl.et(itype="9", ename="SOLID185")
mapdl.keyopt(
    itype="9", knum="6", value="1"
)  # Use mixed u-P formulation to avoid locking
mapdl.keyopt(itype="9", knum="2", value="3")  # Use Simplified Enhanced Strain
# method

# For plaque
mapdl.et(itype="16", ename="SOLID185")
mapdl.keyopt(itype="16", knum="2", value="0")  # Use B-bar

###############################################################################
# Defining settings to model the stent, the artery and the plaque
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Use force-distributed boundary constraints on 2 sides of artery wall to allow
# for radial expansion of tissue without rigid body motion.


# Settings for MPC Surface-based, force-distributed contact on proximal plane
# parallel to x-y plane

mapdl.mat("2")
mapdl.r(nset="3")
mapdl.real(nset="3")
mapdl.et(itype="3", ename="170")
mapdl.et(itype="4", ename="174")
mapdl.keyopt(itype="4", knum="12", value="5")
mapdl.keyopt(itype="4", knum="4", value="1")
mapdl.keyopt(itype="4", knum="2", value="2")
mapdl.keyopt(itype="3", knum="2", value="1")
mapdl.keyopt(itype="3", knum="4", value="111111")
mapdl.type(itype="3")

mapdl.mat("2")
mapdl.r(nset="4")
mapdl.real(nset="4")
mapdl.et(itype="5", ename="170")
mapdl.et(itype="6", ename="174")
mapdl.keyopt(itype="6", knum="12", value="5")
mapdl.keyopt(itype="6", knum="4", value="1")
mapdl.keyopt(itype="6", knum="2", value="2")
mapdl.keyopt(itype="5", knum="2", value="1")
mapdl.keyopt(itype="5", knum="4", value="111111")
mapdl.type(itype="5")


# Settings for standard contact between stent and inner plaque wall contact
# surface

mapdl.mp(lab="MU", mat="1", c0="0")
mapdl.mat("1")
mapdl.mp(lab="EMIS", mat="1", c0="7.88860905221e-31")
mapdl.r(nset="6")
mapdl.real(nset="6")
mapdl.et(itype="10", ename="170")
mapdl.et(itype="11", ename="177")
mapdl.r(nset="6", r3="1.0", r4="1.0", r5="0")
mapdl.rmore(r9="1.0E20", r10="0.0", r11="1.0")
mapdl.rmore(r7="0.0", r8="0", r9="1.0", r10="0.05", r11="1.0", r12="0.5")
mapdl.rmore(r7="0", r8="1.0", r9="1.0", r10="0.0")
mapdl.keyopt(itype="11", knum="5", value="0")
mapdl.keyopt(itype="11", knum="7", value="1")
mapdl.keyopt(itype="11", knum="8", value="0")
mapdl.keyopt(itype="11", knum="9", value="0")
mapdl.keyopt(itype="11", knum="10", value="2")
mapdl.keyopt(itype="11", knum="11", value="0")
mapdl.keyopt(itype="11", knum="12", value="0")
mapdl.keyopt(itype="11", knum="2", value="3")
mapdl.keyopt(itype="10", knum="5", value="0")

# Settings for MPC based, force-distributed constraint on proximal stent nodes

mapdl.mat("1")
mapdl.r(nset="7")
mapdl.real(nset="7")
mapdl.et(itype="12", ename="170")
mapdl.et(itype="13", ename="175")
mapdl.keyopt(itype="13", knum="12", value="5")
mapdl.keyopt(itype="13", knum="4", value="1")
mapdl.keyopt(itype="13", knum="2", value="2")
mapdl.keyopt(itype="12", knum="2", value="1")
mapdl.keyopt(itype="12", knum="4", value="111111")
mapdl.type(itype="12")

# Settings for MPC based, force-distributed constraint on distal stent nodes

mapdl.mat("1")
mapdl.r(nset="8")
mapdl.real(nset="8")
mapdl.et(itype="14", ename="170")
mapdl.et(itype="15", ename="175")
mapdl.keyopt(itype="15", knum="12", value="5")
mapdl.keyopt(itype="15", knum="4", value="1")
mapdl.keyopt(itype="15", knum="2", value="2")
mapdl.keyopt(itype="14", knum="2", value="1")
mapdl.keyopt(itype="14", knum="4", value="111111")
mapdl.type(itype="14")


###############################################################################
# Reading the geometry file
# ~~~~~~~~~~~~~~~~~~~~~~~~~

mapdl.cdread(option="db", fname="stent", ext="cdb")
mapdl.allsel(labt="all")
mapdl.finish()


###############################################################################
# Static Analysis
# --------------
#
# Run static analysis
# ~~~~~~~~~~~~~~~~~~

# enter solution processor and define analysis settings
mapdl.run("/solu")
mapdl.antype(antype="0")
mapdl.nlgeom(key="on")

###############################################################################
# Apply Load Step 1: Balloon angioplasty of the artery to expand it past the
# radius of the stent - IGNORE STENT
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

mapdl.nsubst(nsbstp="20", nsbmx="20")
mapdl.nropt(option1="full")
mapdl.cncheck(option="auto")
mapdl.esel(type_="s", item="type", vmin="11")
mapdl.cm(cname="contact2", entity="elem")
mapdl.ekill(elem="contact2")  # Kill contact elements in stent-plaque contact
# pair so that the stent is ignored in the first
# loadstep

mapdl.nsel(type_="s", item="loc", comp="x", vmin="0", vmax="0.01e-3")
mapdl.nsel(type_="r", item="loc", comp="y", vmin="0", vmax="0.01e-3")
mapdl.d(node="all", lab="all")
mapdl.allsel()

mapdl.sf(
    nlist="load", lab="pres", value="10e-2"
)  # Apply 0.1 Pa/mm^2 pressure to inner plaque wall
mapdl.allsel()
mapdl.nldiag(label="cont", key="iter")
mapdl.solve()
mapdl.save()

################################################################
# Apply Load Step 2: Reactivate contact between stent and plaque
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

mapdl.ealive(elem="contact2")
mapdl.allsel()

mapdl.nsubst(nsbstp="2", nsbmx="2")
mapdl.save()
mapdl.solve()


###################
# Apply Load Step 3
# ~~~~~~~~~~~~~~~~~

mapdl.nsubst(nsbstp="1", nsbmx="1", nsbmn="1")
mapdl.solve()

###############################################################################
# Apply Load Step 4: Apply blood pressure (13.3 kPa) load to inner wall of
# plaque and allow the stent to act as a scaffold
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

mapdl.nsubst(nsbstp="300", nsbmx="3000", nsbmn="30")
mapdl.sf(nlist="load", lab="pres", value="13", value2="3e-3")
mapdl.allsel()

########################################
# Apply stabilization with energy option
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

mapdl.stabilize(key="const", method="energy", value="0.1")


#################
# Solve the model
# ~~~~~~~~~~~~~~~

mapdl.solve()
mapdl.save()
mapdl.finish()


###############################################################################
# Exit MAPDL
mapdl.exit()


###############################################################################
# Work in process after this section
# ----------------------------------

###############################################################################
# Post-processing the modal results
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This sections illustrates different methods to post-process the results of the
# modal analysis : PyMAPDL method, PyMAPDL result reader, PyDPF-Post
# and PyDPF-Core. All methods lead to the same result and are just given as an
# example of how each module can be used.

# using MAPDL methods
mapdl.post1()
mapdl.set(1, 1)
mapdl.plnsol("u", "sum")


###############################################################################
# Using PyMAPDL result reader
# ***************************
#
# *Not recommended* - PyMAPDL reader library is in process to being deprecated.
# It is recommended to use `DPF Post <https://postdocs.pyansys.com/>`_.
#

mapdl_result = mapdl.result
mapdl_result.plot_nodal_displacement(0)

###############################################################################
# Using DPF-Post
# **************
#

from ansys.dpf import post

solution_path = mapdl.result_file
solution = post.load_solution(solution_path)
print(solution)
displacement = solution.displacement(time_scoping=1)
total_deformation = displacement.norm
total_deformation.plot_contour(show_edges=True, background="w")

###############################################################################
# Using DPF-Core
# **************
#

from ansys.dpf import core

model = core.Model(solution_path)
results = model.results
print(results)
displacements = results.displacement()
total_def = core.operators.math.norm_fc(displacements)
total_def_container = total_def.outputs.fields_container()
mesh = model.metadata.meshed_region
mesh.plot(total_def_container.get_field_by_time_id(1))

###############################################################################
# Run PSD analysis
# ----------------
# The response spectrum analysis is defined, solved and post-processed.

# define PSD analysis with input spectrum
mapdl.slashsolu()
mapdl.antype("spectr")

# power spectral density
mapdl.spopt("psd")

# use input table 1 with acceleration spectrum in terms of acceleration due to
# gravity
mapdl.psdunit(1, "accg", 9.81 * 1000)

# define the frequency points in the input table 1
mapdl.psdfrq(1, "", 1, 40, 50, 70.71678, 100, 700, 900)

# define the PSD values in the input table 1
mapdl.psdval(1, 0.01, 0.01, 0.1, 1, 10, 10, 1)

# set the damping ratio as 5%
mapdl.dmprat(0.05)

# apply base excitation on the set of nodes N_BASE_EXCITE in the y-direction
# from table 1
mapdl.d("N_BASE_EXCITE", "uy", 1)

# calculate the participation factor for PSD with base excitation from input
# table 1
mapdl.pfact(1, "base")

# write the displacent solution relative to the base excitation to the results
# file from the PSD analysis
mapdl.psdres("disp", "rel")

# write the absolute velocity solution to the results file from the PSD analysis
mapdl.psdres("velo", "abs")

# write the absolute acceleration solution to the results file from the PSD
# analysis
mapdl.psdres("acel", "abs")

# combine only those modes whose significance level exceeds 0.0001
mapdl.psdcom()
output = mapdl.solve()
print(output)

###############################################################################
# Post-process PSD analysis
# ~~~~~~~~~~~~~~~~~~~~~~~~~
# The response spectrum analysis is post-processed. First, the standard
# MAPDL POST1 postprocessor is used. Then, the MAPDL time-history
# POST26 postprocessor is used to generate the response power spectral
# density.
#
# .. note::
#    The graph generated through POST26 is exported as a picture in the working
#    directory. Finally, the results from POST26 are saved to Python variables
#    to be plotted in the Python environment with the use of Matplotlib
#    library.


###############################################################################
# Post-process PSD analysis in POST1
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

mapdl.post1()
mapdl.set(1, 1)
mapdl.plnsol("u", "sum")
mapdl.set("last")
mapdl.plnsol("u", "sum")

###############################################################################
# Post-process PSD analysis in POST26 (time-history post-processing)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

mapdl.post26()

# allow storage for 200 variables
mapdl.numvar(200)
mapdl.cmsel("s", "MY_MONITOR")
monitored_node = mapdl.queries.ndnext(0)
mapdl.store("psd")

# store the psd analysis u_y data for the node MYMONITOR as the reference no 2
mapdl.nsol(2, monitored_node, "u", "y")

# compute the response power spectral density for displacement associated with
# variable 2
mapdl.rpsd(3, 2)
mapdl.show("png")

# plot the variable 3
mapdl.plvar(3)

# print the variable 3
mapdl.prvar(3)

# x-axis is set for Log X scale
mapdl.gropt("logx", 1)

# y-axis is set for Log X scale
mapdl.gropt("logy", 1)

# plot the variable 3
mapdl.plvar(3)
mapdl.show("close")

###############################################################################
# Post-process PSD analysis using Matplotlib
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# store MAPDL results to python variables
mapdl.dim("frequencies", "array", 4000, 1)
mapdl.dim("response", "array", 4000, 1)
mapdl.vget("frequencies", 1)
mapdl.vget("response", 3)
frequencies = mapdl.parameters["frequencies"]
response = mapdl.parameters["response"]

# use Matplotlib to create graph
fig = plt.figure()
ax = fig.add_subplot(111)
plt.xscale("log")
plt.yscale("log")
ax.plot(frequencies, response)
ax.set_xlabel("Frequencies")
ax.set_ylabel("Response power spectral density")

###############################################################################
# Exit MAPDL
mapdl.exit()
