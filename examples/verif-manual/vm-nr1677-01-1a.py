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

r""".. _ref_VM-NR6645-01-1-a:

Nuclear Regulatory Commission Piping Benchmarks
-----------------------------------------------
Problem description:
 - The example problem contains Mechanical APDL solutions to
   Nuclear Regulatory Commission piping
   benchmark problems taken from publications NUREG/CR-1677, Volumes 1.

 - The piping benchmark solutions given in NRC publications were obtained
   by using a computer program EPIPE which is a modification of the widely
   available program SAP IV specifically prepared to perform piping analyses.

 - The dynamic loading in this problem is induced by uniform earthquake
   type excitation in the three spatial directions. The solutions are
   determined by using the response spectrum method.

Reference:
 - P.Bezler, M. Hartzman & M. Reich,"Dynamic Analysis of Uniform Support
   Motion Response Spectrum Method", (NUREG/CR-1677), Brookhaven National
   Laboratory, August 1980, Problem 1, Pages 24-47.

Analysis type(s):
 - Modal Analysis ``ANTYPE=2``
 - Spectral Analysis ``ANTYPE=8``

Element type(s):
 - Structural Mass Element (``MASS21``)
 - 3-D 3-Node Pipe Element (``PIPE289``)
 - 3-D 3-Node Elbow Element (``ELBOW290``)

.. figure: ../_static/vm-nr1677-01-1a_setup.png
   :align: center
   :figclass: align-center
   :width: 500
   :alt: vm-nr1677-01-1a Finite Element Model of NRC Piping Benchmark Problems, Volume 1, Problem 1


Model description:
 - The model consists of a piping system with straight pipes and elbows.
 - The system is subjected to uniform support motion in three spatial directions.
 - The model is meshed using ``PIPE289`` and ``ELBOW290`` elements for the piping components
   and MASS21 elements for point mass representation.

Postprocessing:
 - Frequencies obtained from modal solution.
 - Maximum nodal displacements and rotations are extracted.
 - Element forces and moments are calculated for specific elements.
 - Reaction forces from the spectrum solution are obtained.
"""  # noqa:E501

# sphinx_gallery_thumbnail_path = '_static/vm-nr1677-01-1a_setup.png'

""
# Import the MAPDL module
from ansys.mapdl.core import launch_mapdl

# Launch MAPDL with a specific log level and print command output
# Here, we set loglevel to "WARNING" to reduce verbosity and print_com to True to see commands
mapdl = launch_mapdl(loglevel="WARNING", print_com=True)

# ###############################################################################
# Preprocessing: Modeling of NRC Piping Benchmark Problems using ``PIPE289`` and ``ELBOW290`` elements
# -----------------------------------------------------------------------------------------------------
#
"""

# Clear any previous data in MAPDL

mapdl.clear()

mapdl.title("NRC Piping Benchmark Problems, Volume 1, Problem 1")

mapdl.prep7(mute=True)

# PIPE289 using cubic shape function and Thick pipe theory.

mapdl.et(1, "pipe289")
mapdl.keyopt(1, 4, 2)

# ELBOW290 using cubic shape function and number of Fourier terms = 6.

mapdl.et(2, "elbow290", "", 6)

# MASS21, 3-D Mass without Rotary Inertia

mapdl.et(3, "mass21")
mapdl.keyopt(3, 3, 2)

# Real Constants

mapdl.sectype(1, "pipe")
mapdl.secdata(7.289, 0.241, 24)

# Define Keypoints

mapdl.k(1, 0.0, 0.0, 0.0)
mapdl.k(2, 0.0, 54.45, 0.0)
mapdl.k(3, 0.0, 108.9, 0.0)
mapdl.k(4, 10.632, 134.568, 0.0)
mapdl.k(5, 36.3, 145.2, 0.0)
mapdl.k(6, 54.15, 145.2, 0.0)
mapdl.k(7, 72.0, 145.2, 0.0)
mapdl.k(8, 97.668, 145.2, 10.632)
mapdl.k(9, 108.3, 145.2, 36.3)
mapdl.k(10, 108.3, 145.2, 56.80)
mapdl.k(11, 108.3, 145.2, 77.3)

mapdl.k(12, 2.7631, 122.79, 0)
mapdl.k(13, 22.408, 142.44, 0)
mapdl.k(14, 85.9, 145, 2.76)
mapdl.k(15, 106, 145, 22.4)

# Straight Pipe (Tangent Elements)
mapdl.type(1)
mapdl.mat(1)
mapdl.secnum(1)
mapdl.real(1)

mapdl.l(1, 2)
mapdl.l(2, 3)
mapdl.l(5, 6)
mapdl.l(6, 7)
mapdl.l(9, 10)
mapdl.l(10, 11)  # Line number 6

# Bend Pipe Elements

mapdl.larc(3,4,12)  # Line number 7
mapdl.larc(4,5,13)
mapdl.larc(7,8,14)
mapdl.larc(8,9,15)  # line number 10

# Define Material Properties

mapdl.mp("ex", 1, 24e6)
mapdl.mp("nuxy", 1, 0.3)

# Meshing for straight pipe using PIPE289 elements

mapdl.type(1)
mapdl.secnum(1)
mapdl.mat(1)

mapdl.lsel("s", "line", "", 1, 6)
mapdl.allsel("below", "line")
mapdl.lesize("all", "", "", 2)
mapdl.lmesh("all")
mapdl.allsel("all", "all")

# Meshing for bend pipe using ELBOW290 elements

mapdl.type(2)
mapdl.secnum(1)
mapdl.mat(1)

mapdl.lsel("s", "", "", 7, 14)
mapdl.allsel("below", "line")
mapdl.lesize("all", "", "", 2)
mapdl.lmesh("all")
mapdl.allsel("all", "all")

# Real constants for mass element

mapdl.r(12, 0.03988)
mapdl.r(13, 0.05032)
mapdl.r(14, 0.02088)
mapdl.r(15, 0.01698)
mapdl.r(16, 0.01307)
mapdl.r(17, 0.01698)
mapdl.r(18, 0.01044)
mapdl.r(19, 0.01795)
mapdl.r(20, 0.01501)

# Mass Elements

mapdl.type(3)
mapdl.real(12)
mapdl.e(2)

mapdl.real(13)
mapdl.e(6)

mapdl.real(14)
mapdl.e(28)

mapdl.real(15)
mapdl.e(10)

mapdl.real(16)
mapdl.e(11)

mapdl.real(17)
mapdl.e(15)

mapdl.real(18)
mapdl.e(35)

mapdl.real(19)
mapdl.e(19)

mapdl.real(20)
mapdl.e(20)

# Using ELBOW, to convert some PIPE289 into ELBOW290

mapdl.elbow("on", "", "", "sect")

mapdl.allsel("all", "all")

# Display the model

mapdl.eplot()

# Define constraints

mapdl.dk(1, "all", 0)
mapdl.dk(11, "all", 0)

mapdl.allsel("all", "all")
mapdl.finish()

###############################################################################
# Modal analysis
# --------------
# Perform modal analysis to obtain the first five natural frequencies
# of the system. The results will be used to determine the response spectrum
# analysis. The modal analysis is performed using the LANB method.

mapdl.slashsolu()
mapdl.antype("modal")

# LANB mode extraction method

nmodes = 5
mapdl.modopt("lanb", nmodes)

# Set the number of modes to extract
mapdl.mxpand("", "", "", "yes")

###############################################################################
# Solve the modal analysis
# ------------------------

mapdl.solve()
mapdl.finish()

###############################################################################
# Postprocessing: Extracting frequencies from the modal analysis
# --------------------------------------------------------------

mapdl.post1()

# Frequencies from Modal solve

freq_list = mapdl.set("list").to_list()

print("Frequencies from Modal solve:")
for set, time_freq, load_step, substep, cumulative in freq_list:
    print(f" - {time_freq:0.3f} Hz")

mapdl.finish()

###############################################################################
# Response Spectrum Analysis
# --------------------------
# Perform spectrum analysis using the frequencies obtained from the modal analysis.
# The response spectrum analysis will be performed for a single point excitation
# response spectrum. The damping ratio is set to a constant value for all modes.
# The modes are grouped based on a significance level, and the seismic acceleration
# response loading is defined. The excitation is applied along the X, Y, and Z
# directions with specified frequencies and corresponding spectral values.
# Start the solution controls for spectrum solve

mapdl.slashsolu()

# Perform Spectrum Analysis
mapdl.antype("spectr")

# Single Point Excitation Response Spectrum
mapdl.spopt("sprs")

# specify constant damping ratio for all modes
mapdl.dmprat(0.02)

# Group Modes based on significance level
mapdl.grp(0.001)

# Seismic Acceleration Response Loading
mapdl.svtyp(2)

# Excitation along X direction
mapdl.sed(1)
mapdl.freq()
mapdl.freq(3.1, 4, 5, 5.81, 7.1, 8.77, 10.99, 14.08, 17.24)
mapdl.freq(25, 28.5, 30, 34.97, 55, 80, 140, 162, 588.93)
mapdl.sv(0.02, 400, 871, 871, 700, 1188, 1188, 440, 775, 775)
mapdl.sv(0.02, 533.2, 467.2, 443.6, 380, 289, 239.4, 192.6, 184.1, 145)
mapdl.solve()

# Excitation along Y direction
mapdl.sed("", 1)
mapdl.freq()
mapdl.freq(3.1, 4, 5, 5.81, 7.1, 8.77, 10.99, 14.08, 17.24)
mapdl.freq(25, 28.5, 30, 34.97, 55, 80, 140, 162, 588.93)
mapdl.sv(0.02, 266.7, 580.7, 580.7, 466.7, 792, 792, 293.3, 516.7, 516.7)
mapdl.sv(0.02, 355.5, 311.5, 295.7, 253.3, 192.7, 159.6, 128.4, 122.7, 96.7)
mapdl.solve()

# Excitation along Z direction
mapdl.sed("", "", 1)
mapdl.freq()
mapdl.freq(3.1, 4, 5, 5.81, 7.1, 8.77, 10.99, 14.08, 17.24)
mapdl.freq(25, 28.5, 30, 34.97, 55, 80, 140, 162, 588.93)
mapdl.sv(0.02, 400, 871, 871, 700, 1188, 1188, 440, 775, 775)
mapdl.sv(0.02, 533.2, 467.2, 443.6, 380, 289, 239.4, 192.6, 184.1, 145)

###############################################################################
# Solve the spectrum analysis
# ---------------------------

mapdl.solve()
mapdl.finish()

###############################################################################
# Postprocessing: Extracting results from the spectrum analysis
# ----------------------------------------------------------------------
# Extract maximum nodal displacements and rotations from the spectrum solution.
# The results will be stored in the MAPDL database and can be accessed using
# the `starstatus` command. The nodal displacements and rotations are obtained
# for specific nodes in the model. The element forces and moments are obtained
# for specific nodes from spectrum solution. The reaction forces from the spectrum
# solution are also extracted.

mapdl.post1()
mcom_file = mapdl.input("", "mcom")

mapdl.get("AdisX", "NODE", 10, "U", "X")
mapdl.get("AdisY", "NODE", 36, "U", "Y")
mapdl.get("AdisZ", "NODE", 28, "U", "Z")
mapdl.get("ArotX", "NODE", 9, "ROT", "X")
mapdl.get("ArotY", "NODE", 18, "ROT", "Y")
mapdl.get("ArotZ", "NODE", 9, "ROT", "Z")

###############################################################################
# Maximum nodal displacements and rotations obtained from spectrum solution

adisx = mapdl.starstatus("AdisX")
adisy = mapdl.starstatus("AdisY")
adisz = mapdl.starstatus("AdisZ")
arotx = mapdl.starstatus("ArotX")
aroty = mapdl.starstatus("ArotY")
arotz = mapdl.starstatus("ArotZ")

print("Maximum nodal displacements and rotations obtained from spectrum solution:")
print(
    f"AdisX: {adisx},\n AdisY: {adisy},\n AdisZ: {adisz}\n"
    f"ArotX: {arotx},\n ArotY: {aroty},\n ArotZ: {arotz}"
)

###############################################################################
# Element Forces and Moments obtained from spectrum solution for Node "I"

# Element results extraction for element #12 (Pipe289 elements)
mapdl.esel("s", "elem", "", 12)
mapdl.etable("pxi_12", "smisc", 1)
mapdl.etable("vyi_12", "smisc", 6)
mapdl.etable("vzi_12", "smisc", 5)
mapdl.etable("txi_12", "smisc", 4)
mapdl.etable("myi_12", "smisc", 2)
mapdl.etable("mzi_12", "smisc", 3)
mapdl.esel("all")

# Element results extraction for element #14 (Elbow 290 elements)
mapdl.esel("s", "elem", "", 14)

mapdl.etable("pxi_14", "smisc", 1)
mapdl.etable("vyi_14", "smisc", 6)
mapdl.etable("vzi_14", "smisc", 5)
mapdl.etable("txi_14", "smisc", 4)
mapdl.etable("myi_14", "smisc", 2)
mapdl.etable("mzi_14", "smisc", 3)
mapdl.esel("all")

###############################################################################
# Element Forces and Moments obtained from spectrum solution for Node "J"

# Element results extraction for element #12 (Pipe289 elements)
mapdl.esel("s", "elem", "", 12)

mapdl.etable("pxj_12", "smisc", 14)
mapdl.etable("vyj_12", "smisc", 19)
mapdl.etable("vzj_12", "smisc", 18)
mapdl.etable("txj_12", "smisc", 17)
mapdl.etable("myj_12", "smisc", 15)
mapdl.etable("mzj_12", "smisc", 16)
mapdl.esel("all")

# Element results extraction for element #14 (Elbow 290 elements)
mapdl.esel("s", "elem", "", 14)

mapdl.etable("pxj_14", "smisc", 36)
mapdl.etable("vyj_14", "smisc", 41)
mapdl.etable("vzj_14", "smisc", 40)
mapdl.etable("txj_14", "smisc", 39)
mapdl.etable("myj_14", "smisc", 37)
mapdl.etable("mzj_14", "smisc", 38)
mapdl.esel("all")

mapdl.allsel("all")
mapdl.run("/GOPR")

###############################################################################
# Element forces and moments at element 12, node "i"

elem_forces_12i = mapdl.pretab(
    "pxi_12", "vyi_12", "vzi_12", "txi_12", "myi_12", "mzi_12"
)
print("Element forces and moments at element 12, node i:", elem_forces_12i)

###############################################################################
# Element forces and moments at element 12, node "j"

elem_forces_12j = mapdl.pretab(
    "pxj_12", "vyj_12", "vzj_12", "txj_12", "myj_12", "mzj_12"
)
print("Element forces and moments at element 12, node j:", elem_forces_12j)

###############################################################################
# Element forces and moments at element 14, node "i"

elem_forces_14i = mapdl.pretab(
    "pxi_14", "vyi_14", "vzi_14", "txi_14", "myi_14", "mzi_14"
)
print("Element forces and moments at element 14, node i:", elem_forces_14i)

###############################################################################
# Element forces and moments at element 14, node "j"

elem_forces_14j = mapdl.pretab(
    "pxj_14", "vyj_14", "vzj_14", "txj_14", "myj_14", "mzj_14"
)
print("Element forces and moments at element 14, node i:", elem_forces_14j)

###############################################################################
# Reaction forces from spectrum solution

reaction_force = mapdl.prrsol()
print("Reaction forces:", reaction_force)

mapdl.finish()

################################################################################
# Stop MAPDL.

mapdl.exit()

""
