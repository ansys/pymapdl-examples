"""
VM291 Force on the Boundary of a Semi-Infinite Body (Boussinesq Problem)
========================================================================

Description:
A point force is applied at the origin of a half-space 2-D axisymmetric
solid modeled with far-field domain. Determine the displacement in the
Y-direction on nodes along the radial direction (at location Y = 0)
and vertical direction (at location X = 0).

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

# Run the /VERIFY command for VM291
mapdl.run("/VERIFY,VM291")

# Set the title of the analysis
mapdl.title("VM291FORCE ON BOUNDARY OF A SEMI-INFINITE BODY (BOUSSINESQ PROBLEM)")

# Comment line: Providing additional information about the analysis
mapdl.com("")
mapdl.com("REFERENCE: 'TIMOSHENKO,S.P.,AND J.N.GOODIER,THEORY OF ELASTICITY")
mapdl.com("MCGRAW-HILL,NEW YORK, PP 398-402, 1970")
mapdl.com("******************************************")
mapdl.com("USING PLANE182 AND INFIN257 ELEMENTS")
mapdl.com("*******************************************")

# Entering the PREP7 environment in MAPDL
mapdl.prep7()

# Constant value of PI
mapdl.run("PI=ACOS(-1)")

# 2D 4-NODE STRUCTURAL SOLID
mapdl.et(1, "PLANE182")
# Set keyopt(3)=1, AXISYMMETRIC
mapdl.keyopt(1, 3, 1)

# DEFINE MATERIAL MODEL
# YOUNG'S MODULUS
mapdl.run("Exx=1.0                 ")
mapdl.mp("EX", 1, "Exx")
# POISSON'S RATIO
mapdl.run("NUxy=0.1                ")
mapdl.mp("PRXY", 1, "NUxy")

# DEFINE NODES
mapdl.n(1, 0, 0)
mapdl.n(2, 1, 0)
mapdl.n(3, 0.75, -0.75)
mapdl.n(4, 0, -1)
mapdl.n(5, 2, 0)
mapdl.n(6, 1.75, -0.75)
mapdl.n(7, 1.5, -1.5)
mapdl.n(8, 0.75, -1.75)
mapdl.n(9, 0, -2)
mapdl.n(10, 3, 0)
mapdl.n(11, 2.5833, -1.0833)
mapdl.n(12, 2.1667, -2.1667)
mapdl.n(13, 1.0833, -2.5833)
mapdl.n(14, 0, -3)
mapdl.n(15, 4, 0)
mapdl.n(16, 3.4167, -1.4167)
mapdl.n(17, 2.8333, -2.8333)
mapdl.n(18, 1.4167, -3.4167)
mapdl.n(19, 0, -4)

# Define Mat =1 and Type = 1
mapdl.mat(1)
mapdl.type(1)

# FORM 2D 4 NODE STRUCTURAL SOLID ELEMENTS
mapdl.e(4, 3, 2, 1)
mapdl.e(6, 5, 2, 3)
mapdl.e(7, 6, 3, 8)
mapdl.e(9, 8, 3, 4)
mapdl.e(11, 10, 5, 6)
mapdl.e(12, 11, 6, 7)
mapdl.e(13, 12, 7, 8)
mapdl.e(14, 13, 8, 9)
mapdl.e(16, 15, 10, 11)
mapdl.e(17, 16, 11, 12)
mapdl.e(18, 17, 12, 13)
mapdl.e(19, 18, 13, 14)

# select node located at (0,0,0) and assign it to variable "NPOLE"
mapdl.run("NPOLE=NODE(0,0,0)")

# selects nodes
mapdl.nsel("S", "", "", 15, 19)

# GENERATE SEMI-INFINITE SOLID ELEMENTS
mapdl.einfin("", "NPOLE")

# Selects all entities
mapdl.run("ALLS")

# Selects nodes using location x=0
mapdl.nsel("S", "LOC", "X", 0)

# CONSTRAINT UX DOF AT LOCATION X=0
mapdl.d("ALL", "UX", 0)

# Selects all entities
mapdl.run("ALLS")

# FORCE magnitude
p=-1
# APPLY FORCE ALONG Y DIRECTION AT NODE1 having magnitude "p"
mapdl.f(1, "FY", "P")

# Finish pre-processing processor
mapdl.finish()

# Enter the solution processor to define solution controls
mapdl.slashsolu()

# Performing static analysis
mapdl.antype("STATIC")

# Controls the solution data written to the database.
mapdl.outres("ALL", "ALL")

# Sets the time for a load step, time=1
mapdl.time(1)

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

# Set constant parameters
r1=1
z1=1

# UY AT NODE (1,0,0)
uy1=p*(1-nuxy**2)/(pi*exx*r1)
# UY AT NODE (0,1,0)
up1=p/(2*pi*exx*z1)*(1+nuxy+2-2*nuxy**2)
# MAPDL UY AT NODE(1,0,0)
uya1 = mapdl.get("UYA1", "NODE", 2, "U", "Y")
# MADPL UY AT NODE(0,1,0)
upa1 = mapdl.get("UPA1", "NODE", 4, "U", "Y")

# Set constant parameters
r2=2
z2=2

# UY AT NODE (2,0,0)
uy2=p*(1-nuxy**2)/(pi*exx*r2)
# UY AT NODE (0,2,0)
up2=p*(2*pi*exx*z2)*(1+nuxy+2-2*nuxy**2)
# MAPDL UY AT NODE(2,0,0)
uya2 = mapdl.get("UYA2", "NODE", 5, "U", "Y")
# MADPL UY AT NODE(0,2,0)
upa2 = mapdl.get("UPA2", "NODE", 9, "U", "Y")

# Set constant parameters, R3=3 and Z3=3
r3=3
z3=3

# UY AT NODE (3,0,0)
uy3=p*(1-nuxy**2)/(pi*exx*r3)
# UY AT NODE (0,3,0)
up3=p/(2*pi*exx*z3)*(1+nuxy+2-2*nuxy**2)
# MAPDL UY AT NODE(3,0,0)
uya3 = mapdl.get("UYA3", "NODE", 10, "U", "Y")
# MADPL UY AT NODE(0,3,0)
upa3 = mapdl.get("UPA3", "NODE", 14, "U", "Y")

# Set constant parameters, R4=4 and Z4=4
r4 = 4
z4 = 4

# UY AT NODE (4,0,0)
uy4=p*(1-nuxy**2)/(pi*exx*r4)
# UY AT NODE (0,4,0)
up4=p/(2*pi*exx*z4)*(1+nuxy+2-2*nuxy**2)
# MAPDL UY AT NODE(4,0,0)
uya4 = mapdl.get("UYA4", "NODE", 15, "U", "Y")
# MADPL UY AT NODE(0,4,0)
upa4 = mapdl.get("UPA4", "NODE", 19, "U", "Y")

# Enter non-interactive mode
with mapdl.non_interactive:
    # redirects output to the default system output file
    mapdl.run("/OUT,SCRATCH")

    # Define dimensions for output
    mapdl.dim("VALUE", "", 3, 6)
    mapdl.dim("LABEL", "CHAR", 3, 2)
    # Define labels for output
    mapdl.run("VALUE(1,1)=UY2")
    mapdl.run("VALUE(2,1)=UY3")
    mapdl.run("VALUE(3,1)=UY4")
    mapdl.run("VALUE(1,2)=UYA2")
    mapdl.run("VALUE(2,2)=UYA3")
    mapdl.run("VALUE(3,2)=UYA4")
    mapdl.run("VALUE(1,3)=UP2")
    mapdl.run("VALUE(2,3)=UP3")
    mapdl.run("VALUE(3,3)=UP4")
    mapdl.run("VALUE(1,4)=UPA2")
    mapdl.run("VALUE(2,4)=UPA3")
    mapdl.run("VALUE(3,4)=UPA4")
    mapdl.run("VALUE(1,5)=UY2/UYA2")
    mapdl.run("VALUE(2,5)=UY3/UYA3")
    mapdl.run("VALUE(3,5)=UY4/UYA4")
    mapdl.run("VALUE(1,6)=UP2/UPA2")
    mapdl.run("VALUE(2,6)=UP3/UPA3")
    mapdl.run("VALUE(3,6)=UP4/UPA4")
    mapdl.run("LABEL(1,1)='NODE5'")
    mapdl.run("LABEL(2,1)='NODE10'")
    mapdl.run("LABEL(3,1)='NODE15'")
    mapdl.run("LABEL(1,2)='NODE9'")
    mapdl.run("LABEL(2,2)='NODE14'")
    mapdl.run("LABEL(3,2)='NODE19'")

    # Save the result table
    mapdl.save("TABLE_1")
    # exists post-processing processor
    mapdl.finish()

    # Clears the database without restarting
    mapdl.run("/CLEAR,NOSTART")
    # redirects output to the default system output file
    mapdl.run("/OUT")
    # reactivates suppressed printout
    mapdl.run("/GOPR")

mapdl.com("***************************************")
mapdl.com("USING PLANE183 AND INFIN257 ELEMENTS")
mapdl.com("***************************************")

# Enter PREP7 module for the new analysis
mapdl.prep7()

# Constant value of PI
mapdl.run("PI=ACOS(-1)")

# YOUNG'S MODULUS
mapdl.run("Exx=1.0                 ")
# POISSON'S RATIO
mapdl.run("NUxy=0.1                ")

# DEFINE MATERIAL MODEL
mapdl.mp("EX", 1, "Exx")
mapdl.mp("PRXY", 1, "NUxy")

# 2D 8-NODE STRUCTURAL SOLID
mapdl.et(1, "PLANE183")
# Set keyopt(3)=1, AXISYMMETRIC
mapdl.keyopt(1, 3, 1)

# DEFINE NODES
mapdl.com("DEFINE NODES")
mapdl.n(1, 0.0000, -1.0000, 0.0000)
mapdl.n(2, 0.75000, -0.75000, 0.0000)
mapdl.n(3, 0.37500, -0.87500, 0.0000)
mapdl.n(4, 1.0000, 0.0000, 0.0000)
mapdl.n(5, 0.87500, -0.37500, 0.0000)
mapdl.n(6, 0.0000, 0.0000, 0.0000)
mapdl.n(7, 0.50000, 0.0000, 0.0000)
mapdl.n(8, 0.0000, -0.50000, 0.0000)
mapdl.n(9, 1.7500, -0.75000, 0.0000)
mapdl.n(10, 2.0000, 0.0000, 0.0000)
mapdl.n(11, 1.8750, -0.37500, 0.0000)
mapdl.n(12, 1.5000, 0.0000, 0.0000)
mapdl.n(13, 1.2500, -0.75000, 0.0000)
mapdl.n(14, 1.5000, -1.5000, 0.0000)
mapdl.n(15, 1.6250, -1.1250, 0.0000)
mapdl.n(16, 0.75000, -1.7500, 0.0000)
mapdl.n(17, 0.75000, -1.2500, 0.0000)
mapdl.n(18, 1.1250, -1.6250, 0.0000)
mapdl.n(19, 0.0000, -2.0000, 0.0000)
mapdl.n(20, 0.37500, -1.8750, 0.0000)
mapdl.n(21, 0.0000, -1.5000, 0.0000)
mapdl.n(22, 2.5833, -1.0833, 0.0000)
mapdl.n(23, 3.0000, 0.0000, 0.0000)
mapdl.n(24, 2.7917, -0.54165, 0.0000)
mapdl.n(25, 2.5000, 0.0000, 0.0000)
mapdl.n(26, 2.1667, -0.91665, 0.0000)
mapdl.n(27, 2.1667, -2.1667, 0.0000)
mapdl.n(28, 2.3750, -1.6250, 0.0000)
mapdl.n(29, 1.8334, -1.8334, 0.0000)
mapdl.n(30, 1.0833, -2.5833, 0.0000)
mapdl.n(31, 1.6250, -2.3750, 0.0000)
mapdl.n(32, 0.91665, -2.1667, 0.0000)
mapdl.n(33, 0.0000, -3.0000, 0.0000)
mapdl.n(34, 0.54165, -2.7917, 0.0000)
mapdl.n(35, 0.0000, -2.5000, 0.0000)
mapdl.n(36, 3.4167, -1.4167, 0.0000)
mapdl.n(37, 4.0000, 0.0000, 0.0000)
mapdl.n(38, 3.7083, -0.70835, 0.0000)
mapdl.n(39, 3.5000, 0.0000, 0.0000)
mapdl.n(40, 3.0000, -1.2500, 0.0000)
mapdl.n(41, 2.8333, -2.8333, 0.0000)
mapdl.n(42, 3.1250, -2.1250, 0.0000)
mapdl.n(43, 2.5000, -2.5000, 0.0000)
mapdl.n(44, 1.4167, -3.4167, 0.0000)
mapdl.n(45, 2.1250, -3.1250, 0.0000)
mapdl.n(46, 1.2500, -3.0000, 0.0000)
mapdl.n(47, 0.0000, -4.0000, 0.0000)
mapdl.n(48, 0.70835, -3.7083, 0.0000)
mapdl.n(49, 0.0000, -3.5000, 0.0000)

# Define Mat =1 and Type = 1
mapdl.mat(1)
mapdl.type(1)

# DEFINE ELEMENTS
mapdl.com("DEFINE ELEMENTS")
mapdl.e(1, 2, 4, 6, 3, 5, 7, 8)
mapdl.e(9, 10, 4, 2, 11, 12, 5, 13)
mapdl.e(14, 9, 2, 16, 15, 13, 17, 18)
mapdl.e(19, 16, 2, 1, 20, 17, 3, 21)
mapdl.e(22, 23, 10, 9, 24, 25, 11, 26)
mapdl.e(27, 22, 9, 14, 28, 26, 15, 29)
mapdl.e(30, 27, 14, 16, 31, 29, 18, 32)
mapdl.e(33, 30, 16, 19, 34, 32, 20, 35)
mapdl.e(36, 37, 23, 22, 38, 39, 24, 40)
mapdl.e(41, 36, 22, 27, 42, 40, 28, 43)
mapdl.e(44, 41, 27, 30, 45, 43, 31, 46)
mapdl.e(47, 44, 30, 33, 48, 46, 34, 49)

# select node located at (0,0,0) and assign it to variable "NPOLE"
mapdl.run("NPOLE=NODE(0,0,0)")

# select nodes
mapdl.nsel("S", "NODE", "", 36, 38, 1)
mapdl.nsel("A", "NODE", "", 41, 42, 1)
mapdl.nsel("A", "NODE", "", 44, 45, 1)
mapdl.nsel("A", "NODE", "", 47, 48, 1)

# GENERATE SEMI-INFINITE SOLID ELEMENTS
mapdl.einfin("", "NPOLE")

# Selects all entities
mapdl.run("ALLS")

# Selects nodes using location x=0
mapdl.nsel("S", "LOC", "X", 0)

# CONSTRAINT UX DOF AT LOCATION X=0
mapdl.d("ALL", "UX", 0)
# Selects all entities
mapdl.run("ALLS")

# FORCE magnitude
mapdl.run("P=-1                    ")
# APPLY FORCE ALONG Y DIRECTION AT NODE6
mapdl.f(6, "FY", "P")

# Finish pre-processing processor
mapdl.finish()

# Enter the solution processor to define solution controls
mapdl.run("/SOLUTION")

# Specify static analysis type
mapdl.run("ANTYPE,STATIC")

# Controls the solution data written to the database.
mapdl.outres("ALL", "ALL")

# Sets the time for a load step, time=1
mapdl.time(1)

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

# Set constant parameters, R1=1 and Z1=1
mapdl.run("R1=1")
mapdl.run("Z1=1")
# UY AT NODE (1,0,0)
mapdl.run("UY1=P*(1-NUxy**2)/(PI*Exx*R1)               ")
# UY AT NODE (0,1,0)
mapdl.run("UP1=P/(2*PI*Exx*Z1)*(1+NUxy+2-2*NUxy**2)    ")
# MAPDL UY AT NODE(1,0,0)
mapdl.get("UYA1", "NODE", 4, "U", "Y")
# MADPL UY AT NODE(0,1,0)
mapdl.get("UPA1", "NODE", 1, "U", "Y")

# Set constant parameters, R2=2 and Z2=2
mapdl.run("R2=2")
mapdl.run("Z2=2")

# UY AT NODE (2,0,0)
mapdl.run("UY2=P*(1-NUxy**2)/(PI*Exx*R2)               ")
# UY AT NODE (0,2,0)
mapdl.run("UP2=P/(2*PI*Exx*Z2)*(1+NUxy+2-2*NUxy**2)    ")
# MAPDL UY AT NODE(2,0,0)
mapdl.get("UYA2", "NODE", 10, "U", "Y")
# MADPL UY AT NODE(0,2,0)
mapdl.get("UPA2", "NODE", 19, "U", "Y")

# Set constant parameters, R3=3 and Z3=3
mapdl.run("R3=3")
mapdl.run("Z3=3")
# UY AT NODE (3,0,0)
mapdl.run("UY3=P*(1-NUxy**2)/(PI*Exx*R3)               ")
# UY AT NODE (0,3,0)
mapdl.run("UP3=P/(2*PI*Exx*Z3)*(1+NUxy+2-2*NUxy**2)    ")
# MAPDL UY AT NODE(3,0,0)
mapdl.get("UYA3", "NODE", 23, "U", "Y")
# MADPL UY AT NODE(0,3,0)
mapdl.get("UPA3", "NODE", 33, "U", "Y")

# Set constant parameters, R4=4 and Z4=4
mapdl.run("R4=4")
mapdl.run("Z4=4")
# UY AT NODE (4,0,0)
mapdl.run("UY4=P*(1-NUxy**2)/(PI*Exx*R4)               ")
# UY AT NODE (0,4,0)
mapdl.run("UP4=P/(2*PI*Exx*Z4)*(1+NUxy+2-2*NUxy**2)    ")
# MAPDL UY AT NODE(4,0,0)
mapdl.get("UYA4", "NODE", 37, "U", "Y")
# MADPL UY AT NODE(0,4,0)
mapdl.get("UPA4", "NODE", 47, "U", "Y")

# Enter non-interactive mode
with mapdl.non_interactive:
    # redirects output to the default system output file
    mapdl.run("/OUT,SCRATCH")

    # Define dimensions for output
    mapdl.dim("VALUE1", "", 3, 6)
    mapdl.dim("LABEL1", "CHAR", 3, 2)
    # Define labels for output
    mapdl.run("VALUE1(1,1)=UY2")
    mapdl.run("VALUE1(2,1)=UY3")
    mapdl.run("VALUE1(3,1)=UY4")
    mapdl.run("VALUE1(1,2)=UYA2")
    mapdl.run("VALUE1(2,2)=UYA3")
    mapdl.run("VALUE1(3,2)=UYA4")
    mapdl.run("VALUE1(1,3)=UP2")
    mapdl.run("VALUE1(2,3)=UP3")
    mapdl.run("VALUE1(3,3)=UP4")
    mapdl.run("VALUE1(1,4)=UPA2")
    mapdl.run("VALUE1(2,4)=UPA3")
    mapdl.run("VALUE1(3,4)=UPA4")
    mapdl.run("VALUE1(1,5)=UY2/UYA2")
    mapdl.run("VALUE1(2,5)=UY3/UYA3")
    mapdl.run("VALUE1(3,5)=UY4/UYA4")
    mapdl.run("VALUE1(1,6)=UP2/UPA2")
    mapdl.run("VALUE1(2,6)=UP3/UPA3")
    mapdl.run("VALUE1(3,6)=UP4/UPA4")
    mapdl.run("LABEL1(1,1)='NODE10'")
    mapdl.run("LABEL1(2,1)='NODE23'")
    mapdl.run("LABEL1(3,1)='NODE37'")
    mapdl.run("LABEL1(1,2)='NODE19'")
    mapdl.run("LABEL1(2,2)='NODE33'")
    mapdl.run("LABEL1(3,2)='NODE47'")

    # Save the result table
    mapdl.save("TABLE_2")
    # exists post-processing processor
    mapdl.finish()
    # Resume table "TABLE_1"
    mapdl.resume("TABLE_1")
    mapdl.run("/OUT,vm291,vrt")
    mapdl.com("")
    mapdl.com("--------------VM291 RESULTS COMPARISON--------------------")
    mapdl.com("")
    mapdl.com("")
    mapdl.com("|   TARGET   |   Mechanical APDL   | RATIO")
    mapdl.com("")
    mapdl.com("")
    mapdl.com("**************************************")
    mapdl.com("USING PLANE182 AND INFIN257 ELEMENTS")
    mapdl.com("**************************************")
    mapdl.com("")
    mapdl.com("VERTICAL DISPLACEMENT(UY) ON THE SURFACE (Y=0)")
    mapdl.com("")
    mapdl.run("*VWRITE,LABEL(1,1),VALUE(1,1),VALUE(1,2),VALUE(1,5)")
    mapdl.run("(4X,A10'  ',F10.4,'       ',F10.4,'        ',1F5.3)")
    mapdl.com("")
    mapdl.com("")
    mapdl.com("")
    mapdl.com("VERTICAL DISPLACEMENT(UY) BELOW THE POINT LOAD (X=0)")
    mapdl.com("")
    mapdl.run("*VWRITE,LABEL(1,2),VALUE(1,3),VALUE(1,4),VALUE(1,6)")
    mapdl.run("(4X,A10'  ',F10.4,'       ',F10.4,'        ',1F5.3)")
    mapdl.com("")
    mapdl.com("")

    # It is not recommended to use '/NOPR' in a normal PyMAPDL session.
    mapdl._run("/NOPR")
    # Resume table "TABLE_1"
    mapdl.resume("TABLE_2")

    mapdl.gopr()
    mapdl.com("")
    mapdl.com("**************************************")
    mapdl.com("USING PLANE183 AND INFIN257 ELEMENTS")
    mapdl.com("**************************************")
    mapdl.com("")
    mapdl.com("VERTICAL DISPLACEMENT(UY) ON THE SURFACE (Y=0)")
    mapdl.com("")
    mapdl.run("*VWRITE,LABEL1(1,1),VALUE1(1,1),VALUE1(1,2),VALUE1(1,5)")
    mapdl.run("(4X,A10'  ',F10.4,'       ',F10.4,'        ',1F5.3)")
    mapdl.com("")
    mapdl.com("")
    mapdl.com("")
    mapdl.com("VERTICAL DISPLACEMENT(UY) BELOW THE POINT LOAD (X=0)")
    mapdl.com("")
    mapdl.run("*VWRITE,LABEL1(1,2),VALUE1(1,3),VALUE1(1,4),VALUE1(1,6)")
    mapdl.run("(4X,A10'  ',F10.4,'       ',F10.4,'        ',1F5.3)")
    mapdl.com("")
    mapdl.com("")
    mapdl.com("")
    mapdl.com("----------------------------------------------------------")
    # redirects output to the default system output file
    mapdl.run("/OUT")
    # reactivates suppressed printout
    mapdl.run("/GOPR")

# Get the mapdl temporary working directory
vrt_file_path = os.path.join(mapdl.directory, "vm291.vrt")

# read the vm291.vrt file to print the results
f = open(vrt_file_path, "r")
for x in f:
    print(x)

# Finish the post-processing processor
mapdl.finish()
# Displays/Lists the contents of an external file
mapdl.starlist("vm291", "vrt")

# Exit MAPDL session
mapdl.exit()
