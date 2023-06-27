"""
VM299 Sound Diffusion in a Flat Room
========================================================================

Description:
Sound diffusion is modeled in a flat room of size 30x30x3 m3.
A sound source is placed at (2,2,1) with a sound power level of 1x10-2 W.
The wall absorption coefficient is equal to 0.1.
The coefficient of atmospheric attenuation is 0.01 m-1.

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

# Run the /VERIFY command for VM299
mapdl.run("/VERIFY,VM299")

# Set the title of the analysis
mapdl.title("VM299SOUND PRESSURE LEVEL IN A FLAT ROOM")

# Comment line: Providing additional information about the analysis
mapdl.com("")
mapdl.com("REFERENCE: A.BILLON,J.PICAUT,'INTRODUCING ATMOSPHERIC ATTENUATION")
mapdl.com("WITHIN A DIFFUSION MODEL FOR ROOM-ACOUSTIC PREDICTIONS'")
mapdl.com("MARCH 2008.")
mapdl.com("")

# Entering the PREP7 environment in MAPDL
mapdl.prep7()

# It is not recommended to use '/NOPR' in a normal PyMAPDL session.
mapdl._run("/NOPR")

# Set parameters for ROOM SIZE
mapdl.run("LX=30")
mapdl.run("LY=30")
mapdl.run("LZ=3")
mapdl.run("VOL=LX*LY*LZ")
mapdl.run("SURF=2*(LX*LY+LY*LZ+LX*LZ)")
mapdl.run("MFP=4*VOL/SURF")

# set parameters for MATERIAL PROPERTIES
mapdl.run("C0 = 343")
mapdl.run("RHO = 1.21")
mapdl.run("ROOMD=MFP*C0/3")
mapdl.run("ATTN=0.01")
mapdl.run("ROOMDP=ROOMD/(1.+ATTN*MFP)")
mapdl.run("ALPHA=0.1")
mapdl.run("WS=1.E-2")
# DEFINE MATERIALS
mapdl.mp("DENS", 1, "RHO")
mapdl.mp("SONC", 1, "C0")
mapdl.tb("AFDM", 1, "", "", "ROOM")
mapdl.tbdata(1, "ROOMDP", "ATTN")
# GENERATE GEOMETRY
mapdl.run("H=0.5")
mapdl.dim("A", "ARRAY", 3)
mapdl.dim("B", "ARRAY", 3)
mapdl.dim("C", "ARRAY", 3)
mapdl.run("A(1)=0")
mapdl.run("A(2)=2.")
mapdl.run("A(3)=LX")
mapdl.run("B(1)=0")
mapdl.run("B(2)=2.")
mapdl.run("B(3)=LY")
mapdl.run("C(1)=0")
mapdl.run("C(2)=1.")
mapdl.run("C(3)=LZ")

# Enter non-interactive mode
with mapdl.non_interactive:
    mapdl.run("*DO,I,1,2")
    mapdl.run("*DO,J,1,2")
    mapdl.run("*DO,K,1,2")
    mapdl.block("A(I)", "A(I+1)", "B(J)", "B(J+1)", "C(K)", "C(K+1)")
    mapdl.run("*ENDDO")
    mapdl.run("*ENDDO")
    mapdl.run("*ENDDO")

# Generates new volumes by “gluing” volumes.
mapdl.vglue("ALL")
# Define element, 3-D Acoustic Fluid 20-Node Solid Element
mapdl.et(1, 220, 3, 4)
mapdl.type(1)  # set element type, Type=1
mapdl.mat(1)  # set material type, MAT=1
mapdl.esize("H")  # Specifies the element size.

# Generates nodes and volume elements within volumes.
mapdl.vmesh(9, 15, 1)
# mapdl.type(1)
# mapdl.mat(1)
# mapdl.esize("H")

# For elements that support multiple shapes, specifies the element shape, set mshape=3D
mapdl.mshape(0, "3D")
# Generates nodes and volume elements within volumes.
mapdl.vmesh(1)
# select nodes of specified location
mapdl.nsel("S", "LOC", "X", 0)
mapdl.nsel("A", "LOC", "X", "LX")
mapdl.nsel("A", "LOC", "Y", 0)
mapdl.nsel("A", "LOC", "Y", "LY")
mapdl.nsel("A", "LOC", "Z", 0)
mapdl.nsel("A", "LOC", "Z", "LZ")

# Define Absorption coefficient and transmission loss
mapdl.sf("ALL", "ATTN", "ALPHA")
# Selects all entities
mapdl.run("ALLS")
# select nodes of specified location
mapdl.nsel("S", "LOC", "X", "A(2)")
mapdl.nsel("R", "LOC", "Y", "B(2)")
mapdl.nsel("R", "LOC", "Z", "C(2)")

# Define Mass source; mass source rate; or power source
# in an energy diffusion solution for room acoustics
mapdl.bf("ALL", "MASS", "WS")

# Selects all entities
mapdl.run("ALLS")
# Finish pre-processing processor
mapdl.finish()

# Enter the solution processor to define solution controls
mapdl.slashsolu()

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
    # Defines a path name and establishes parameters for the path
    mapdl.path("X_SPL", 2, "", 15)
    mapdl.ppath(1, "NODE", 0, 15, 1)
    mapdl.ppath(2, "NODE", 30, 15, 1)
    # Interpolates an item onto a path.
    mapdl.pdef("UX", "U", "X", "NOAV")
    mapdl.pdef("SPLX", "SPL", "", "NOAV")

    # redirects output to the default system output file
    mapdl.run("/OUT")
    # reactivates suppressed printout
    mapdl.run("/GOPR")

# Prints path items along a geometry path.
mapdl.prpath("UX", "SPLX")

# Enter non-interactive mode
with mapdl.non_interactive:
    # redirects solver output to a file named "SCRATCH"
    mapdl.run("/OUT,SCRATCH")
    # Sets various line graph display options
    # DIVX: Determines the number of divisions (grid markers) that will be plotted on the X
    mapdl.gropt("DIVX", 15)
    # Specifies a linear ordinate (Y) scale range.
    mapdl.yrange(71, 82)
    # DIVY: Determines the number of divisions (grid markers) that will be plotted on the Y
    mapdl.gropt("DIVY", 11)
    # Specifies the device and other parameters for graphics displays.
    # Creates PNG (Portable Network Graphics) files that are named Jobnamennn.png
    mapdl.show("PNG")

    mapdl.plpath("UX", "SPLX")  # Displays path items on a graph.
    mapdl.show("CLOSE")  # This option purges the graphics file buffer.

    mapdl.run("N1=NODE(5,15,1)")
    mapdl.run("N2=NODE(10,15,1)")
    mapdl.run("N3=NODE(15,15,1)")
    mapdl.run("N4=NODE(20,15,1)")
    mapdl.run("N5=NODE(25,15,1)")
    mapdl.run("*GET,EN_1,NODE,N1,ENKE")
    mapdl.run("*GET,EN_2,NODE,N2,ENKE")
    mapdl.run("*GET,EN_3,NODE,N3,ENKE")
    mapdl.run("*GET,EN_4,NODE,N4,ENKE")
    mapdl.run("*GET,EN_5,NODE,N5,ENKE")
    mapdl.run("PREF=2E-5")
    mapdl.run("PI=ACOS(-1)")
    mapdl.run("SPL_1=10*LOG10((RHO*EN_1*C0**2)/PREF**2)")
    mapdl.run("SPL_2=10*LOG10((RHO*EN_2*C0**2)/PREF**2)")
    mapdl.run("SPL_3=10*LOG10((RHO*EN_3*C0**2)/PREF**2)")
    mapdl.run("SPL_4=10*LOG10((RHO*EN_4*C0**2)/PREF**2)")
    mapdl.run("SPL_5=10*LOG10((RHO*EN_5*C0**2)/PREF**2)")
    # Define dimensions for output
    mapdl.dim("LABEL", "CHAR", 5)
    mapdl.dim("VALUE", "ARRAY", 5, 3)
    mapdl.dim("VALUE_REF", "ARRAY", 5, 3)
    mapdl.dim("VALUE_RATIO", "ARRAY", 5, 3)
    # Define labels for output
    mapdl.run("LABEL(1,1)='X = 5 m','X = 10 m','X = 15 m','X = 20 m','X = 25 m'")

    # Fill in the values for the first case
    mapdl.vfill(
        "VALUE(1", "1)", "DATA", "%SPL_1%", "%SPL_2%", "%SPL_3%", "%SPL_4%", "%SPL_5%"
    )
    mapdl.vfill("VALUE_REF(1", "2)", "DATA", 80.0, 79.0, 77.5, 76.0, 74.5)
    mapdl.vfill(
        "VALUE_RATIO(1",
        "3)",
        "DATA",
        "ABS(SPL_1/80.0)",
        "ABS(SPL_2/79.0)",
        "ABS(SPL_3/77.5)",
        "ABS(SPL_4/76.0)",
        "ABS(SPL_5/74.5)",
    )
    mapdl.run("/OUT,vm299,vrt")
    mapdl.com("")
    mapdl.com("------------ vm299 RESULTS COMPARISON --------------")
    mapdl.com("")
    mapdl.com("|  TARGET  |  MECHANICAL APDL  | RATIO")
    mapdl.com("")
    mapdl.run("*VWRITE,LABEL(1,1),VALUE_REF(1,2),VALUE(1,1),VALUE_RATIO(1,3)")
    mapdl.run("(1X,A8,'   ',F7.3,'  ',F7.3,'   ',F7.3)")
    mapdl.com("")
    # redirects output to the default system output file
    mapdl.run("/OUT")
    # reactivates suppressed printout
    mapdl.run("/GOPR")

# Get the mapdl temporary working directory
vrt_file_path = os.path.join(mapdl.directory, "vm299.vrt")

# read the vm299.vrt file to print the results
f = open(vrt_file_path, "r")
for x in f:
    print(x)

# Finish the post-processing processor
mapdl.finish()
# Displays/Lists the contents of an external file
mapdl.starlist("vm299", "vrt")

# Exit MAPDL session
mapdl.exit()
