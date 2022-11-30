# %% [markdown]
#
# # Cardiovascular Stent Simulation

# %% [markdown]
#
# This example problem shows how to simulate stent-artery interaction during and
# after stent placement in an occluded artery.
# The analysis exposes advanced modeling techniques using PyMAPDL such as:
# * Contact
# * Element birth and death
# * Mixed u-P formulation
# * Nonlinear stabilization
#
# This example is inspired from the model and analysis defined in Chapter 25 of
# the Mechanical APDL Technology Showcase Manual.

# %% [markdown]
# ## Starting MAPDL as a service

# %%
# starting MAPDL as a service and importing an external model
from ansys.mapdl.core import launch_mapdl

# start MAPDL as a service
mapdl = launch_mapdl()
print(mapdl)

# %% [markdown]
# # Setting up the model

# %% [markdown]
# ### Defining material properties<br>

# %%
# define 316L Stainless steel
mapdl.prep7()
mapdl.mptemp()
mapdl.mptemp(sloc="1", t1="0")
mapdl.mpdata(lab="EX", mat="1", c1="200e3")
mapdl.mpdata(lab="PRXY", mat="1", c1="0.3")
mapdl.mptemp()
mapdl.mptemp(sloc="1", t1="0")
mapdl.mpdata(lab="DENS", mat="1", c1="8000e-9")

# %% [markdown]
# ### Defining element types

# %%
# for straight line segments
mapdl.et(itype="1", ename="beam189")
mapdl.sectype(secid="1", type_="beam", subtype="csolid")
mapdl.secdata(val1=0.05)

# for arcs
mapdl.et(itype="2", ename="beam189")
mapdl.sectype(secid="2", type_="beam", subtype="csolid")
mapdl.secdata(val1=0.05)

# %% [markdown]
# ### Defining 5-parameter Mooney-Rivlin hyperelastic artery material model

# %%
c10 = 18.90e-3
c01 = 2.75e-3
c20 = 590.43e-3
c11 = 857.2e-3
nu1 = 0.49
dd = 2 * (1 - 2 * nu1) / (c10 + c01)

# %%
mapdl.tb(lab="hyper", mat="2", npts="5", tbopt="mooney")
mapdl.tbdata(stloc="1", c1="c10", c2="c01", c3="c20", c4="c11", c6="dd")

# %% [markdown]
# ### Defining linear elastic material model for stiff calcified plaque

# %%
mapdl.mp(lab="EX", mat="3", c0=".00219e3")
mapdl.mp(lab="NUXY", mat="3", c0="0.49")

# %% [markdown]
# ### Define Solid185 element type to mesh both the artery and plaque

# %%
# for artery
mapdl.et(itype="9", ename="SOLID185")
mapdl.keyopt(
    itype="9", knum="6", value="1"
)  # Use mixed u-P formulation to avoid locking
mapdl.keyopt(itype="9", knum="2", value="3")  # Use Simplified Enhanced Strain method

# for plaque
mapdl.et(itype="16", ename="SOLID185")
mapdl.keyopt(itype="16", knum="2", value="0")  # Use B-bar

# %% [markdown]
# ### Defining settings to model the stent, the artery and the plaque
#
# Use force-distributed boundary constraints on 2 sides of artery wall to allow<br>
# for radial expansion of tissue without rigid body motion.

# %% [markdown]
# #### Settings for MPC Surface-based, force-distributed contact on proximal# plane
# parallel to x-y plane

# %%
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

# %% [markdown]
# #### Settings for standard contact between stent and inner plaque wall
# contact surface

# %%
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

# %% [markdown]
# #### Settings for MPC based, force-distributed constraint on proximal stent nodes

# %%
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

# %% [markdown]
# #### Settings for MPC based, force-distributed constraint on distal stent nodes

# %%
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

# %% [markdown]
# ### Reading the geometry file

# %%
mapdl.cdread(option="db", fname="stent", ext="cdb")
mapdl.allsel(labt="all")
mapdl.finish()

# %% [markdown]
# ## Static Analysis
#
# Run static analysis

# %%
# enter solution processor and define analysis settings
mapdl.run("/solu")
mapdl.antype(antype="0")
mapdl.nlgeom(key="on")

# %% [markdown]
# ### Apply Load Step 1: Balloon angioplasty of the artery to expand it past the
# radius of the stent - IGNORE STENT

# %%
mapdl.nsubst(nsbstp="20", nsbmx="20")
mapdl.nropt(option1="full")
mapdl.cncheck(option="auto")
mapdl.esel(type_="s", item="type", vmin="11")
mapdl.cm(cname="contact2", entity="elem")
mapdl.ekill(elem="contact2")  # Kill contact elements in stent-plaque contact pair
# so that the stent is ignored in the first loadstep
mapdl.nsel(type_="s", item="loc", comp="x", vmin="0", vmax="0.01e-3")
mapdl.nsel(type_="r", item="loc", comp="y", vmin="0", vmax="0.01e-3")
mapdl.d(node="all", lab="all")
mapdl.allsel()

mapdl.sf(nlist="load", lab="pres", value="10e-2")  # apply 0.1 Pa/mm^2 pressure
# to inner plaque wall
mapdl.allsel()
mapdl.nldiag(label="cont", key="iter")
mapdl.solve()
mapdl.save()

# %% [markdown]
# ### Apply Load Step 2: Reactivate contact between stent and plaque

# %%
mapdl.ealive(elem="contact2")
mapdl.allsel()

mapdl.nsubst(nsbstp="2", nsbmx="2")
mapdl.save()
mapdl.solve()

# %% [markdown]
# ### Apply Load Step 3

# %%
mapdl.nsubst(nsbstp="1", nsbmx="1", nsbmn="1")
mapdl.solve()

# %% [markdown]
# ### Apply Load Step 4: Apply blood pressure (13.3 kPa) load to inner wall of
# plaque and allow the stent to act as a scaffold

# %%
mapdl.nsubst(nsbstp="300", nsbmx="3000", nsbmn="30")
mapdl.sf(nlist="load", lab="pres", value="13.3e-3")
mapdl.allsel()

# %% [markdown]
# ### Apply stabilization with energy option

# %%
mapdl.stabilize(key="const", method="energy", value="0.1")

# %% [markdown]
# # Solve the model

# %%
mapdl.solve()
mapdl.save()
mapdl.finish()

# %% [markdown]
# # Post-processing the modal results
#
# This sections illustrates different methods to post-process the results of the
# modal analysis : PyMAPDL method, PyMAPDL result reader, PyDPF-Post and PyDPF-Core.
# All methods lead to the same result and are just given as an example of how each
# module can be used.

# %%
from ansys.dpf import core as dpf

# %% [markdown]
# ## Mesh of the model

# %%
model = dpf.Model(mapdl.result_file)
ds = dpf.DataSources(mapdl.result_file)

# %%
mesh = model.metadata.meshed_region
mesh.plot()

# %% [markdown]
# ## Computed displacements of the model

# %%
# Collecting the computed displacement
u = model.results.displacement(time_scoping=[4]).eval()
print(u[0])

u[0].plot(deform_by=u[0])

# %% [markdown]
# ## Von Mises stress

# %%
# Collecting the computed stress
s_op = model.results.stress(time_scoping=[3])
s_op.inputs.requested_location.connect(dpf.locations.nodal)
s = s_op.eval()

# Calculating Von Mises stress
s_VM = dpf.operators.invariant.von_mises_eqv_fc(fields_container=s).eval()

s_VM[0].plot(deform_by=u[0])

# %% [markdown]
# ## Computed displacements of the stent

# %%
# Creating the mesh associated to the stent
esco = mesh.named_selection("STENT")
print(esco)

# Transposing elemental location to nodal one
op = dpf.operators.scoping.transpose()
op.inputs.mesh_scoping.connect(esco)
op.inputs.meshed_region.connect(mesh)
op.inputs.inclusive.connect(1)
nsco = op.eval()
print(nsco)

# %%
# Collecting the computed displacements of the stent
u_stent = model.results.displacement(mesh_scoping=nsco, time_scoping=[4])
u_stent = u_stent.outputs.fields_container()
U = u_stent[0]

# Linking the stent mesh to the global one
op = dpf.operators.mesh.from_scoping()  # operator instantiation
op.inputs.scoping.connect(nsco)
op.inputs.inclusive.connect(1)
op.inputs.mesh.connect(mesh)
mesh_sco = op.eval()
u_stent[0].meshed_region = mesh_sco

u_stent[0].plot(deformed_by=u_stent[0])

# %% [markdown]
# ## Exit MAPDL

# %%
mapdl.exit()
