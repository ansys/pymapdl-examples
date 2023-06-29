r""".. _ref_vm13:

Cylindrical Shell Under Pressure
---------------------------------
Problem description:
- A long cylindrical pressure vessel of mean diameter d and wall thickness t has closed
  ends and is subjected to an internal pressure P. Determine the axial stress
  :math:`/sigma _y` and the hoop stress :math:`/sigma _z` in the vessel at the
  midthickness of the wall.

Reference:
The references for the analysis can be found here:
  - STR. OF MATL., TIMOSHENKO, PART 1, 3RD ED., PAGE 45, ART. 11
  - UGURAL AND FENSTER, ADV. STRENGTH AND APPL. ELAS., 1981

Analysis type(s):
 - Static Analysis ``ANTYPE=0``

Element type(s):
 - 	Elastic Tapered Unsymmetric Beam Elements (BEAM188)

.. image:: ../_static/vm13_setup.png
   :width: 400
   :alt: VM13 Problem Sketch

Material properties
 - :math:`E = 30 \cdot 10^6 psi`

Geometric properties:
 - :math:`t = 0.1 in`
 - :math:`d = 120 in`

Loading:
 - :math:`P = 500 psi`

Analysis Assumptions and Modeling Notes:
- An arbitrary axial length of 10 inches is selected.
  Nodal coupling is used in the radial direction. An axial
  force of 5654866.8 lb (:math:`(Pπd^2)/4`) is applied to
  simulate the closed-end effect.

"""
# sphinx_gallery_thumbnail_path = '_static/vm13_setup.png'

# Importing the `launch_mapdl` function from the `ansys.mapdl.core` module
from ansys.mapdl.core import launch_mapdl
import numpy as np

# Launch MAPDL with specified settings
mapdl = launch_mapdl(loglevel="WARNING", print_com=True, remove_temp_dir_on_exit=True)

# Clear any existing database
mapdl.clear()

# Set the ANSYS version
mapdl.com("ANSYS MEDIA REL. 2022R2 (05/13/2022) REF. VERIF. MANUAL: REL. 2022R2")

# Run the FINISH command to exists normally from a processor
mapdl.finish()

# Run the /VERIFY command for VM13
mapdl.verify("vm13")

# Set the title of the analysis
mapdl.title("VM13 CYLINDRICAL SHELL UNDER PRESSURE")

# Enter the model creation preprocessor
mapdl.prep7(mute=True)

# Define element type and section properties
mapdl.et(1, "SHELL208")  # Element type SHELL208
mapdl.sectype(1, "SHELL")  # Section type SHELL
mapdl.secdata(1)  # Define section data
mapdl.secnum(1)  # Assign section number

# Define material properties
mapdl.mp("EX", 1, 30e6)  # Young's modulus
mapdl.mp("NUXY", 1, 0.3)  # Poisson's ratio

# Define nodal coordinates
mapdl.n(1, 60)  # Node 1, 60 degrees
mapdl.n(2, 60, 10)  # Node 2, 60 degrees and 10 units in Z-direction

# Define element connectivity
mapdl.e(1, 2)  # Element 1 with nodes 1 and 2

# Apply coupling and boundary conditions
mapdl.cp(1, "UX", 1, 2)  # Couple radial direction (rotation around Z-axis)
mapdl.d(1, "UY", "", "", "", "", "ROTZ")  # Fix UY displacement for node 1
mapdl.d(2, "ROTZ")  # Fix ROTZ (rotation around Z-axis) for node 2

# Apply nodal force and elemental surface pressure
mapdl.f(2, "FY", 5654866.8)  # Apply a concentrated force FY to node 2
mapdl.sfe(1, 1, "PRES", "", 500)  # Apply internal pressure of 500 psi to element 1

# Selects all entities
mapdl.allsel()
mapdl.eplot()

# Finish the pre-processing processor
mapdl.finish()

# Enter the solution processor
mapdl.slashsolu()

# Set the analysis type to STATIC
mapdl.antype("STATIC")

# Controls the solution printout
mapdl.outpr("ALL", 1)

# Solve the analysis
mapdl.solve()

# Finish the solution processor
mapdl.finish()

# Enter post-processing processor
mapdl.post1()

# Create element tables for stress components
mapdl.etable("STRS_Y", "S", "Y")
mapdl.etable("STRS_Z", "S", "Z")

# Retrieve element stresses from the element tables using *Get
stress_y = mapdl.get("STRSS_Y", "ELEM", 1, "ETAB", "STRS_Y")
stress_z = mapdl.get("STRSS_Z", "ELEM", 1, "ETAB", "STRS_Z")

# Fill the Target Result Values in array
Target_values = np.array([15000, 29749])

message = f"""
------------------- VM13 RESULTS COMPARISON ---------------------
   RESULT      |  TARGET     |   Mechanical APDL   |   RATIO
Stress, Y (psi)  {Target_values[0]:.5f}    {stress_y:.5f}       {abs(stress_y/Target_values[0]):.5f}
Stress, Z (psi)  {Target_values[1]:.5f}    {stress_z:.5f}       {abs(stress_z/Target_values[1]):.5f}
-----------------------------------------------------------------
"""
print(message)

mapdl.gopr()

# Finish the post-processing processor
mapdl.finish()

# Exit MAPDL
mapdl.exit()