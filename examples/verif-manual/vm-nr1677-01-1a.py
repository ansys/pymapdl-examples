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

r""".. _ref_VM-NR1677-01-1:

Nuclear Regulatory Commission Piping Benchmarks
-----------------------------------------------
Problem description:
 - The example problem contains Mechanical APDL solutions to
   Nuclear Regulatory Commission (NRC) piping benchmark problems
   taken from publications NUREG/CR-1677, Volumes 1, Problem 1.

 - The piping benchmark solutions given in NRC publications were obtained
   by using a computer program EPIPE which is a modification of the widely
   available program SAP IV specifically prepared to perform piping analyses.

 - This benchmark problem contains three straight sections, two bends,
   and two fixed anchors. The total mass of the system is represented
   by structural mass element (MASS21) specified at individual nodes.

 - Modal and response spectrum analysis is performed on the piping model.
   Frequencies obtained from modal solve and the nodal/element solution
   obtained from spectrum solve are compared against reference results.

 - For response spectrum analysis, acceleration response spectrum
   curve defined by ``SV`` and ``FREQ`` commands.

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
   :alt: vm-nr1677-01-1a: FE Model of Benchmark Problem


Model description:
 - The model consists of a piping system with straight pipes and elbows.
 - The system is subjected to uniform support motion in three spatial
   directions.
 - The model is meshed using ``PIPE289`` and ``ELBOW290`` elements for
   the piping components and ``MASS21`` elements for point mass representation.

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
import numpy as np
from tabulate import tabulate

# Launch MAPDL with a specific log level and print command output
# Here, we set loglevel to "WARNING" to reduce verbosity and print_com to True to see commands
mapdl = launch_mapdl(loglevel="WARNING", print_com=True)

"""
Preprocessing: Modeling of NRC Piping Benchmark Problems using ``PIPE289`` and ``ELBOW290`` elements
-----------------------------------------------------------------------------------------------------

"""

###############################################################################
# Specify material properties, real constants and Element types

# Clear any previous data in MAPDL

mapdl.clear()

mapdl.title("NRC Piping Benchmark Problems, Volume 1, Problem 1")

mapdl.prep7(mute=True)

# Define Material Properties for pipe elements in :math:``psi``

mapdl.mp("ex", 1, 24e6)
mapdl.mp("nuxy", 1, 0.3)

# PIPE289 using cubic shape function and Thick pipe theory.

mapdl.et(1, "pipe289")
mapdl.keyopt(1, 4, 2)

# ELBOW290 using cubic shape function and number of Fourier terms = 6.

mapdl.et(2, "elbow290", "", 6)

# Real Constants for straight and bend pipe elements in :math:``in``

mapdl.sectype(1, "pipe")
mapdl.secdata(7.289, 0.241, 24)

# MASS21, 3-D Mass without Rotary Inertia

mapdl.et(3, "mass21")
mapdl.keyopt(3, 3, 2)

# Define real constants for mass elements, 3-D mass in :math:``lb-sec^2/in``

mapdl.r(12, 0.03988)  # Mass @ node 2
mapdl.r(13, 0.05032)  # Mass @ node 6
mapdl.r(14, 0.02088)  # Mass @ node 28
mapdl.r(15, 0.01698)  # Mass @ node 10
mapdl.r(16, 0.01307)  # Mass @ node 11
mapdl.r(17, 0.01698)  # Mass @ node 15
mapdl.r(18, 0.01044)  # Mass @ node 35
mapdl.r(19, 0.01795)  # Mass @ node 19
mapdl.r(20, 0.01501)  # Mass @ node 20

###############################################################################
# Geometry modeling of nuclear piping system

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

# Straight Pipe system

mapdl.l(1, 2)
mapdl.l(2, 3)
mapdl.l(5, 6)
mapdl.l(6, 7)
mapdl.l(9, 10)
mapdl.l(10, 11)  # Line number 6

# Bend Pipe system

mapdl.larc(3, 4, 12)  # Line number 7
mapdl.larc(4, 5, 13)
mapdl.larc(7, 8, 14)
mapdl.larc(8, 9, 15)  # line number 10

###############################################################################
# Meshing of nuclear piping system using pipe and elbow elements

# Meshing for straight pipe using PIPE289 elements

mapdl.type(1)
mapdl.mat(1)
mapdl.secnum(1)
mapdl.real(1)

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

###############################################################################
# The total system mass of nuclear piping system is represented by structural
# mass element ``MASS21`` specified at individual nodes.

# Specify mass elements with real constants at respective nodes

mapdl.type(3)
mapdl.real(12)
mapdl.e(2)  # Mass element at node 2

mapdl.real(13)
mapdl.e(6)  # Mass element at node 6

mapdl.real(14)
mapdl.e(28)  # Mass element at node 28

mapdl.real(15)
mapdl.e(10)  # Mass element at node 10

mapdl.real(16)
mapdl.e(11)  # Mass element at node 11

mapdl.real(17)
mapdl.e(15)  # Mass element at node 15

mapdl.real(18)
mapdl.e(35)  # Mass element at node 35

mapdl.real(19)
mapdl.e(19)  # Mass element at node 19

mapdl.real(20)
mapdl.e(20)  # Mass element at node 20

###############################################################################
# Using ``ELBOW``, to convert some ``PIPE289`` into ``ELBOW290``

mapdl.elbow("on", "", "", "sect")
mapdl.allsel("all", "all")

###############################################################################
# Display the nuclear piping system model

mapdl.eplot()

###############################################################################
# Define constraints

mapdl.dk(1, "all", 0)
mapdl.dk(11, "all", 0)
mapdl.allsel("all", "all")

###############################################################################
# Finish preprocessing aspects of nuclear piping system.

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

###############################################################################
# Solve the spectrum analysis along X direction
# ---------------------------------------------
# Excitation along X direction

mapdl.sed(1)

mapdl.freq()  # Erase frequency values

mapdl.freq(3.1, 4, 5, 5.81, 7.1, 8.77, 10.99, 14.08, 17.24)
mapdl.freq(25, 28.5, 30, 34.97, 55, 80, 140, 162, 588.93)
mapdl.sv(0.02, 400, 871, 871, 700, 1188, 1188, 440, 775, 775)
mapdl.sv(0.02, 533.2, 467.2, 443.6, 380, 289, 239.4, 192.6, 184.1, 145)

mapdl.solve()

###############################################################################
# Solve the spectrum analysis along Y direction
# ---------------------------------------------
# Excitation along Y direction

mapdl.sed("", 1)

mapdl.freq()  # Erase frequency values

mapdl.freq(3.1, 4, 5, 5.81, 7.1, 8.77, 10.99, 14.08, 17.24)
mapdl.freq(25, 28.5, 30, 34.97, 55, 80, 140, 162, 588.93)
mapdl.sv(0.02, 266.7, 580.7, 580.7, 466.7, 792, 792, 293.3, 516.7, 516.7)
mapdl.sv(0.02, 355.5, 311.5, 295.7, 253.3, 192.7, 159.6, 128.4, 122.7, 96.7)

mapdl.solve()

###############################################################################
# Solve the spectrum analysis along Z direction
# ---------------------------------------------

# Excitation along Z direction

mapdl.sed("", "", 1)

mapdl.freq()  # Erase frequency values

mapdl.freq(3.1, 4, 5, 5.81, 7.1, 8.77, 10.99, 14.08, 17.24)
mapdl.freq(25, 28.5, 30, 34.97, 55, 80, 140, 162, 588.93)
mapdl.sv(0.02, 400, 871, 871, 700, 1188, 1188, 440, 775, 775)
mapdl.sv(0.02, 533.2, 467.2, 443.6, 380, 289, 239.4, 192.6, 184.1, 145)

mapdl.solve()

###############################################################################
# Finish the spectrum analysis

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

adisx = mapdl.get("AdisX", "NODE", 10, "U", "X")
adisy = mapdl.get("AdisY", "NODE", 36, "U", "Y")
adisz = mapdl.get("AdisZ", "NODE", 28, "U", "Z")
arotx = mapdl.get("ArotX", "NODE", 9, "ROT", "X")
aroty = mapdl.get("ArotY", "NODE", 18, "ROT", "Y")
arotz = mapdl.get("ArotZ", "NODE", 9, "ROT", "Z")

###############################################################################
# Element Forces and Moments obtained from spectrum solution for Node "I"

elems = [12, 14]

# Output labels
# px = section axial force at node I and J.
# vy = section shear forces along Y direction at node I and J.
# vz = section shear forces along Z direction at node I and J.
# tx = section torsional moment at node I and J
# my = section bending moments along Y direction at node I and J.
# mz = section bending moments along Z direction at node I and J.
labels = ["px", "vy", "vz", "tx", "my", "mz"]

# SMISC mapping
# To obtain the SMISC values for each element
SMISC = {
    # Element number 12
    12: {
        # Obtained from the Element reference for PIPE289
        "i": [1, 6, 5, 4, 2, 3],
        "j": [14, 19, 18, 17, 15, 16],
    },
    # Element number 14
    14: {
        # Obtained from the Element reference for ELBOW290
        "i": [1, 6, 5, 4, 2, 3],
        "j": [36, 41, 40, 39, 37, 38],
    },
}

for elem in elems:
    mapdl.esel("s", "elem", "", elem)

    for node in ["i", "j"]:
        for label, id_ in zip(labels, SMISC[elem][node]):
            label_ = f"{label}{node}_{elem}"
            mapdl.etable(label_, "smisc", id_)

mapdl.allsel("all")
mapdl.run("/GOPR")

###############################################################################
# Reaction forces from spectrum solution

reaction_force = mapdl.prrsol()

###############################################################################
# Finish postprocessing of response spectrum analysis.

mapdl.finish()

###############################################################################
# Verify the results
# ------------------

###############################################################################
# Frequencies Obtained from Modal Solution
# =======================
#
# The results obtained from the modal solution are compared against target values.
# The target values are defined based on the reference results from the NRC publication.

# Set target values
target_freq = np.array([28.515, 56.441, 82.947, 144.140, 166.260])  # in Hz

# Fill result values
sim_freq_res = [freq[1] for freq in freq_list]

# Store ratio
value_ratio = []
for i in range(len(target_freq)):
    con = sim_freq_res[i] / target_freq[i]
    value_ratio.append(np.abs(con))

print("Frequencies Obtained Modal Solution \n")

# Prepare data for tabulation
data_freq = [
    [i + 1, target_freq[i], sim_freq_res[i], value_ratio[i]]
    for i in range(len(target_freq))
]

# Define headers
headers = ["Mode", "Target", "Mechanical APDL", "Ratio"]

# Print table
print(
    f"""------------------- VM-NR1677-01-1-a.1 RESULTS COMPARISON ---------------------
{tabulate(data_freq, headers=headers, tablefmt="grid")}
"""
)

""
# Set target values
target_res = np.array(
    [7.830e-03, 2.648e-03, 1.748e-02, 1.867e-04, 2.123e-04, 7.217e-05]
)

# Fill result values
# adisx, adisy, adisz, arotx, aroty, arotz = 7.8e-03, 2.6e-03, 1.75e-02, 1.9e-04, 2.1e-04, 7.2e-05
sim_res = np.array([adisx, adisy, adisz, arotx, aroty, arotz])

# Output labels
labels = [
    "UX at node10",
    "UY at node36",
    "UZ at node28",
    "ROTX at node9",
    "ROTY at node18",
    "ROTZ at node9",
]

# Store ratio
value_ratio = []
for i in range(len(target_res)):
    con = sim_res[i] / target_res[i]
    value_ratio.append(np.abs(con))

print("Maximum nodal displacements and rotations obtained from spectrum solution:")

# Prepare data for tabulation
data_freq = [
    [labels[i], target_res[i], sim_res[i], value_ratio[i]]
    for i in range(len(target_res))
]

# Define headers
headers = ["Result Node", "Target", "Mechanical APDL", "Ratio"]

# Print table
print(
    f"""
{tabulate(data_freq, headers=headers, tablefmt="grid")}
"""
)

###############################################################################
# Element forces and moments obtained from spectrum solution for specific elements
# =======================
#

# For Node# 12:

# Set target values
TARGET = {
    12: {
        "i": np.array([24.019, 7.514, 34.728, 123.39, 2131.700, 722.790]),
        "j": np.array([24.018, 7.514, 34.728, 123.39, 2442.700, 786.730]),
    },
    14: {
        "i": np.array([5.1505, 7.2868, 7.9178, 450.42, 675.58, 314.970]),
        "j": np.array([6.006, 6.6138, 7.9146, 157.85, 858.09, 302.940]),
    },
}

sections = [
    "Axial force",
    "Shear force Y",
    "Shear force Z",
    "Torque",
    "Moment Y",
    "Moment Z",
]


for node, element in zip([12, 14], ["Pipe289", "Elbow290"]):
    print("\n\n===================================================")
    print(f"Element forces and moments at element {node} ({element})")
    print("===================================================")

    etab_i = [
        f"pxi_{node}",
        f"vyi_{node}",
        f"vzi_{node}",
        f"txi_{node}",
        f"myi_{node}",
        f"mzi_{node}",
    ]
    etab_j = [
        f"pxj_{node}",
        f"vyj_{node}",
        f"vzj_{node}",
        f"txj_{node}",
        f"myj_{node}",
        f"mzj_{node}",
    ]
    targets_i = TARGET[node]["i"]
    targets_j = TARGET[node]["j"]

    for each_section, each_tab_i, each_tab_j, target_i, target_j in zip(
        sections, etab_i, etab_j, targets_i, targets_j
    ):

        print(f"\n{each_section}")
        print("=" * len(each_section))

        # Element forces and moments at element, node "i"
        values_i = ["Node i"]

        values_i.append(mapdl.get_array("ELEM", "", "ETAB", each_tab_i)[node - 1])
        values_i.append(target_i)
        values_i.append(values_i[1] / target_i)

        # Element forces and moments at element , node "j"
        values_j = ["Node j"]

        values_j.append(mapdl.get_array("ELEM", "", "ETAB", each_tab_j)[node - 1])
        values_j.append(target_j)
        values_j.append(values_j[1] / target_j)

        headers = ["Node", "Mechanical APDL", "Target", "Ratio"]
        print(tabulate([values_i, values_j], headers=headers))

###############################################################################
# Reaction forces
# =======================
#
print("\n\nReaction forces")
print("===============")

headers = reaction_force.get_columns()
values = reaction_force.to_list()

print(tabulate(values, headers=headers))

################################################################################
# Stop MAPDL.

mapdl.exit()
