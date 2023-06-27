"""
VM295 Force on the Boundary of a Semi-Infinite Body (Boussinesq Problem)
========================================================================

Description:
The test case is to simulate a one-dimensional Terzaghi's problem with
permeability as a function of the soil depth. A pressure P is applied
on the top surface of the soil with depth H and width W. The top
surface of the soil is fully permeable and the permeability decreases
linearly with depth. The excess pore water pressure
for 0.1, 0.2, 0.3, 0.4, and 0.5 day is calculated and compared
against the reference results obtained using the PIM method.

"""
import os

# Importing the `launch_mapdl` function from the `ansys.mapdl.core` module
from ansys.mapdl.core import launch_mapdl

# Launch MAPDL with specified options
mapdl = launch_mapdl(loglevel="WARNING", print_com=True, remove_temp_dir_on_exit=True)
# Clear the current database
mapdl.clear()

# Run the FINISH command to exists normally from a processor
mapdl.run("FINISH")

# Set the ANSYS version
mapdl.com("ANSYS MEDIA REL. 2022R2 (05/13/2022) REF. VERIF. MANUAL: REL. 2022R2")

# Run the /VERIFY command for VM295
mapdl.run("/VERIFY,VM295")

# Set the title of the analysis
mapdl.title(
    "VM2951D TERZAGHI'S CONSOLIDATION PROBLEM WITH PERMEABILITY AS FUNCTION OF DEPTH"
)

# Comment line: Providing additional information about the analysis
mapdl.com("REFERENCE: A POINT INTERPOLATION METHOD FOR SIMULATING DISSIPATION PROCESS")
mapdl.com("OF CONSOLIDATION, J.G.WANG, G.R.LIU, Y.G.WU, COMPUTER METHODS")
mapdl.com("IN APPLIED MECHANICS AND ENGINEERING 190 (2001),PG: 5907-5922")

# Entering the PREP7 environment in MAPDL
mapdl.prep7()

# Set Parameters
mapdl.run("DAY=24*3600   ")  # SECONDS IN ONE DAY
mapdl.run("H = 16    ")  # TOTAL DEPTH OF SOIL IN METERS
mapdl.run("W = 1    ")  # WIDTH OF SOIL IN METERS
mapdl.run("R = 1E4    ")  # PRESSURE IN PA
mapdl.run("E = 4E7    ")  # YOUNG'S MODULUS IN PA
mapdl.run("TT = 1*DAY")

# Define element definition
mapdl.et(1, "CPT212")  # 2D 4 NODE COUPLED PORE PRESSURE ELEMENT
mapdl.keyopt(1, 12, 1)
mapdl.keyopt(1, 3, 2)  # Set Keyopt(3)=2, PLANE STRAIN Formulation

# Create geometry and mesh
mapdl.run("RECT,0,W,0,H")  # Generate rectangle
# Specifies the divisions and spacing ratio on unmeshed lines
mapdl.lesize(4, "", "", 16)
mapdl.lesize(3, "", "", 1)
# For elements that support multiple shapes, specifies the element shape, set mshape=2D
mapdl.mshape(0, "2D")
mapdl.mshkey(1)  # Key(1) = Specifies mapped meshing should be used to mesh
mapdl.amesh(1)  # CREATING CPT212 ELEMENTS

# Define material properties
mapdl.mp("EX", 1, "E")
mapdl.mp("NUXY", 1, 0.3)

# Set parameters
mapdl.run("FPX = 1.728E-3/DAY/1E4  ")  # PERMEABILITY FROM REFERENCE
mapdl.run("ONE = 1.0")

# Define TB material properties
mapdl.tb("PM", 1, "", "", "PERM")  # DEFINING PERMEABILITY FOR THE SOIL
mapdl.tbfield("YCOR", 0)  # LOCATION Y = 0
mapdl.tbdata(1, "FPX", "FPX", "FPX")  # PERMEABILITY VALUES AT LOCATION Y=0
mapdl.tbfield("YCOR", "H")  # LOCATION Y=16
# PERMEABILITY VALUES AT LOCATION Y=16, LINEAR VARIABLE PERMEABILITY
mapdl.tbdata(1, "FPX*100", "FPX*100", "FPX*100")
mapdl.tb("PM", 1, "", "", "BIOT")  # DEFINING BIOT COEFFICINET FOR SOIL
mapdl.tbdata(1, "ONE")  # BIOT COEFFICIENT

# Define Constraints
mapdl.d("ALL", "UX", 0)  # CONSTRAINING ALL UX DOF
mapdl.nsel("S", "LOC", "Y", 0)
mapdl.d("ALL", "UY", 0)  # CONSTRAINING UY DOF AT LOCATION Y=0
mapdl.nsel("ALL")
mapdl.nsel("S", "LOC", "Y", "H")
mapdl.d("ALL", "PRES", 0)  # DEFINING THE TOP PORTION OF SOIL AS PERMEABLE
# selects all nodes
mapdl.nsel("ALL")

# Finish pre-processing processor
mapdl.finish()

# Enter the solution processor to define solution controls
mapdl.slashsolu()

mapdl.run("ANTYPE,STATIC   ")  # Performing static analysis
mapdl.nropt("UNSYM")  # UNSYMMETRIC NEWTON RAPHSON OPTION
mapdl.time("TT")  # END TIME

mapdl.nsel("S", "LOC", "Y", "H")
# APPLYING Surface PRESSURE LOAD AT TOP OF THE SOIL
mapdl.sf("ALL", "PRES", "R")
# selects all nodes
mapdl.nsel("ALL")
mapdl.run("NSUBS,350,1000,150  ")  # Specify number of SUBSTEPS
# Controls the solution data written to the database.
mapdl.outres("ALL", "ALL")
mapdl.kbc(1)  # STEPPED LOADING

# Enter non-interactive mode
with mapdl.non_interactive:
    # redirects solver output to a file named "SCRATCH"
    mapdl.run("/OUT,SCRATCH")
    # SOLVE STATIC ANALYSIS
    mapdl.solve()
    # exists solution processor
    mapdl.finish()

    # Enter POST1 module (Post-processing processor)
    mapdl.post1()
    # Set the current results set to the last set to be read from result file
    mapdl.set("LAST")
    # redirects output to the default system output file
    mapdl.run("/OUT")
    # reactivates suppressed printout
    mapdl.run("/GOPR")

# Specify Reference Solution
mapdl.com("")
mapdl.com("EXCESS PORE PRESSURE IN KILOPASCALS AT LOCATION X=1,Y=6")
mapdl.com("FOR 0.1 DAY (8640 SECONDS),0.2 DAY (17280 SECONDS)")
mapdl.com("0.3 DAY (25920 SECONDS), 0.4 DAY (34560 SECONDS)")
mapdl.com("AND 0.5 DAY (43200 SECONDS) ARE COMPUTED AND COMPARED")
mapdl.com("AGAINST REFERENCE SOLUTION")
mapdl.com("")

# Enter non-interactive mode
with mapdl.non_interactive:
    # redirects solver output to a file named "SCRATCH"
    mapdl.run("/OUT,SCRATCH")
    # Define dimensions for output
    mapdl.dim("P", "", 5)
    # Specify load set to read from the result file, load step =1, sub-step=16
    mapdl.set(1, 16)
    mapdl.run("*GET,P11,NODE,NODE(1,6,0),PRES")
    mapdl.run("*GET,T11,ACTIVE,0,SET,TIME")
    # Specify load set to read from the result file, load step =1, sub-step=17
    mapdl.set(1, 17)
    mapdl.run("*GET,P12,NODE,NODE(1,6,0),PRES")
    mapdl.run("*GET,T12,ACTIVE,0,SET,TIME")
    mapdl.run("T1=DAY*0.1")
    mapdl.com("")
    mapdl.com("INTERPOLATE THE RESULTS AT LOCATION (1,6,0) FOR TIME=0.1DAY")
    mapdl.com("")
    mapdl.run("P(1)=(P11+(T1-T11)/(T12-T11)*(P12-P11))/1E3")
    # Specify load set to read from the result file, load step =1, sub-step=31
    mapdl.set(1, 31)
    mapdl.run("*GET,P21,NODE,NODE(1,6,0),PRES")
    mapdl.run("*GET,T21,ACTIVE,0,SET,TIME")
    # Specify load set to read from the result file, load step =1, sub-step=32
    mapdl.set(1, 32)
    mapdl.run("*GET,P22,NODE,NODE(1,6,0),PRES")
    mapdl.run("*GET,T22,ACTIVE,0,SET,TIME")
    mapdl.run("T2=DAY*0.2")
    mapdl.com("")
    mapdl.com("INTERPOLATE THE RESULTS AT LOCATION (1,6,0) FOR TIME=0.2DAY")
    mapdl.com("")
    mapdl.run("P(2)=(P21+(T2-T21)/(T22-T21)*(P22-P21))/1E3")
    # Specify load set to read from the result file, load step =1, sub-step=46
    mapdl.set(1, 46)
    mapdl.run("*GET,P31,NODE,NODE(1,6,0),PRES")
    mapdl.run("*GET,T31,ACTIVE,0,SET,TIME")
    # Specify load set to read from the result file, load step =1, sub-step=47
    mapdl.set(1, 47)
    mapdl.run("*GET,P32,NODE,NODE(1,6,0),PRES")
    mapdl.run("*GET,T32,ACTIVE,0,SET,TIME")
    mapdl.run("T3=DAY*0.3")
    mapdl.com("")
    mapdl.com("INTERPOLATE THE RESULTS AT LOCATION (1,6,0) FOR TIME=0.3DAY")
    mapdl.com("")
    mapdl.run("P(3)=(P31+(T3-T31)/(T32-T31)*(P32-P31))/1E3")
    # Specify load set to read from the result file, load step =1, sub-step=61
    mapdl.set(1, 61)
    mapdl.run("*GET,P41,NODE,NODE(1,6,0),PRES")
    mapdl.run("*GET,T41,ACTIVE,0,SET,TIME")
    # Specify load set to read from the result file, load step =1, sub-step=62
    mapdl.set(1, 62)
    mapdl.run("*GET,P42,NODE,NODE(1,6,0),PRES")
    mapdl.run("*GET,T42,ACTIVE,0,SET,TIME")
    mapdl.run("T4=DAY*0.4")
    mapdl.com("")
    mapdl.com("INTERPOLATE THE RESULTS AT LOCATION (1,6,0) FOR TIME=0.4DAY")
    mapdl.com("")
    mapdl.run("P(4)=(P41+(T4-T41)/(T42-T41)*(P42-P41))/1E3")
    # Specify load set to read from the result file, load step =1, sub-step=76
    mapdl.set(1, 76)
    mapdl.run("*GET,P51,NODE,NODE(1,6,0),PRES")
    mapdl.run("*GET,T51,ACTIVE,0,SET,TIME")
    # Specify load set to read from the result file, load step =1, sub-step=77
    mapdl.set(1, 77)
    mapdl.run("*GET,P52,NODE,NODE(1,6,0),PRES")
    mapdl.run("*GET,T52,ACTIVE,0,SET,TIME")
    mapdl.run("T5=DAY*0.5")
    mapdl.com("")
    mapdl.com("INTERPOLATE THE RESULTS AT LOCATION (1,6,0) FOR TIME=0.5DAY")
    mapdl.com("")
    mapdl.run("P(5)=(P51+(T5-T51)/(T52-T51)*(P52-P51))/1E3")
    mapdl.dim("CP", "", 5)
    # REFERENCE RESULTS, FIGURE 5, PG 5916
    mapdl.run("CP(1)=5.230,2.970,1.769,1.043,0.632  ")
    mapdl.dim("RT", "", 5)
    mapdl.run("*DO,I,1,5")
    mapdl.run("RT(I)=P(I)/CP(I)")
    mapdl.run("*ENDDO")
    mapdl.dim("LABEL", "CHAR", 5)
    mapdl.run("LABEL(1)='0.1','0.2','0.3','0.4','0.5'")
    mapdl.com("")
    mapdl.run("/OUT,vm295,vrt")
    mapdl.com("------------ vm295 RESULTS COMPARISON --------------")
    mapdl.com("")
    mapdl.com("Time     |  TARGET   |  Mechanical APDL  |  RATIO")
    mapdl.com("")
    mapdl.run("*VWRITE,LABEL(1),CP(1),P(1),RT(1)")
    mapdl.run("(8X,A4,'       ',F10.3,'       ',F10.3,'    ',F10.2)")
    mapdl.com("")
    mapdl.com("------------------------------------------------------")
    # redirects output to the default system output file
    mapdl.run("/OUT")
    # reactivates suppressed printout
    mapdl.run("/GOPR")

# Get the mapdl temporary working directory
vrt_file_path = os.path.join(mapdl.directory, "vm295.vrt")

# read the vm295.vrt file to print the results
f = open(vrt_file_path, "r")
for x in f:
    print(x)

# Finish the post-processing processor
mapdl.finish()
# Displays/Lists the contents of an external file
mapdl.starlist("vm295", "vrt")

# Exit MAPDL session
mapdl.exit()
