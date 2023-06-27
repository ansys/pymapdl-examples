"""
VM13 Cylindrical Shell Under Pressure
=========================================

Description:
A long cylindrical pressure vessel of mean diameter d and wall thickness t has closed
ends and is subjected to an internal pressure P. Determine the axial stress 
:math:`/sigma _y` and the hoop stress :math:`/sigma _z` in the vessel at the midthickness of the wall.

"""
import os

# Importing the `launch_mapdl` function from the `ansys.mapdl.core` module
from ansys.mapdl.core import launch_mapdl

# Launch MAPDL with specified settings
mapdl = launch_mapdl(loglevel="WARNING", print_com=True, remove_temp_dir_on_exit=True)

# Clear any existing database
mapdl.clear()

# Set the ANSYS version
mapdl.com("ANSYS MEDIA REL. 2022R2 (05/13/2022) REF. VERIF. MANUAL: REL. 2022R2")

# Run the FINISH command to exists normally from a processor
mapdl.run("FINISH")

# Run the /VERIFY command for VM13
mapdl.verify("vm13")

# Set the title of the analysis
mapdl.title("VM13 CYLINDRICAL SHELL UNDER PRESSURE")

"""
The references for the analysis can be found here: 
  - STR. OF MATL., TIMOSHENKO, PART 1, 3RD ED., PAGE 45, ART. 11
  - UGURAL AND FENSTER, ADV. STRENGTH AND APPL. ELAS., 1981
"""

# Enter the model creation preprocessor
mapdl.prep7()

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

# Defines an array parameter and its dimensions of output quantities.
mapdl.dim("LABEL", "CHAR", 2, 2)
mapdl.dim("VALUE", "", 2, 3)

# Set labels for output variables
mapdl.run("LABEL(1,1) = 'STRESS,Y ','STRESS,Z'")
mapdl.run("LABEL(1,2) = ' (psi)  ',' (psi)  '")

# Fill the VALUE table with data
mapdl.vfill("VALUE(1", "1)", "DATA", 15000, 29749)
mapdl.vfill("VALUE(1", "2)", "DATA", "STRSS_Y", "STRSS_Z")
mapdl.vfill("VALUE(1", "3)", "DATA", "ABS(STRSS_Y/15000 )", "ABS(STRSS_Z/29749 )")

# Run non-interactive commands
with mapdl.non_interactive:
    mapdl.run("/OUT,vm13,vrt")  # Output to a file named vm13.vrt
    mapdl.com("------------------- VM13 RESULTS COMPARISON ---------------------")
    mapdl.com("")
    mapdl.com("|   TARGET   |   Mechanical APDL   |   RATIO")
    mapdl.com("")
    mapdl.run("*VWRITE,LABEL(1,1),LABEL(1,2),VALUE(1,1),VALUE(1,2),VALUE(1,3)")
    mapdl.run("(1X,A8,A8,'   ',F10.0,'  ',F12.0,'   ',1F15.3)")
    mapdl.com("-----------------------------------------------------------------")
    mapdl.run("/OUT")

# Get the mapdl temporary working directory
vrt_file_path = os.path.join(mapdl.directory, "vm13.vrt")

# read the vm14.vrt file to print the results
f = open(vrt_file_path, "r")
for x in f:
    print(x)

message = f"""
------------------- VM13 RESULTS COMPARISON ---------------------
   RESULT      |  TARGET     |   ANSYS       |   RATIO
Stress, Y (psi)   {15000:.5f}     {stress_y:.5f}   {abs(stress_y/15000):.5f}
Stress, Z (psi)   {29749:.5f}     {stress_z:.5f}   {abs(stress_z/29749):.5f}
-----------------------------------------------------------------
"""
print(message)

mapdl.run("/GOPR")

# Finish the post-processing processor
mapdl.finish()
mapdl.starlist("vm13", "vrt")

# Exit MAPDL
mapdl.exit()
