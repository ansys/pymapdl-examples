r""".. _ref_vm14:

Large Deflection Eccentric Compression of Slender Column
--------------------------------------------------------
Problem description:
 - Find the deflection :math:`/delta` at the middle and the maximum tensile and compressive stresses
   in an eccentrically compressed steel strut of length L. The cross-section is a channel
   with the dimensions shown in the diagram. The ends are pinned at the point of load application.
   The distance between the centroid and the back of the channel is e, and the compressive force F
   acts in the plane of the back of the channel and in the symmetry plane of the channel.

Reference:
 - S. Timoshenko, Strength of Materials, Part I, Elementary Theory and
   Problems, 3rd Edition, D. Van Nostrand Co., Inc., New York, NY, 1955,
   pg. 263, problem 1.

Analysis type(s):
 - Static, Large Deflection Analysis ``ANTYPE=0``

Element type(s):
 - 2-Node Finite Strain Axisymmetric Shell (SHELL208)

.. image:: ../_static/vm14_setup.png
   :width: 400
   :alt: VM14 Slender Column Problem Sketch

Material properties
 - :math:`E = 30 \cdot 10^6 psi`
 - :math:`u = 0.3`

Geometric properties:
 - :math:`L = 10 ft`
 - :math:`h = 8 in`
 - :math:`s = 0.22 in`
 - :math:`t = 0.39 in`
 - :math:`e = 0.6465 in`
 - :math:`b = 2.26 in`

Loading:
 - :math:`F = 4000 lb`

Analysis Assumptions and Modeling Notes:
 - Only one-half of the structure is modeled because of symmetry.
   The boundary conditions for the equivalent half model become fixed-free.
   Large deflection is needed since the stiffness of the structure and the
   loading change significantly with deflection. The offset e is defined in
   the element coordinate system.

"""
# sphinx_gallery_thumbnail_path = '_static/vm14_setup.png'

# Importing the `launch_mapdl` function from the `ansys.mapdl.core` module
from ansys.mapdl.core import launch_mapdl
import pandas

# Launch MAPDL with specified settings
mapdl = launch_mapdl(loglevel="WARNING", print_com=True, remove_temp_dir_on_exit=True)

# Clear any existing database
mapdl.clear()

# Set the ANSYS version
mapdl.com("ANSYS MEDIA REL. 2022R2 (05/13/2022) REF. VERIF. MANUAL: REL. 2022R2")

# Run the FINISH command to exists normally from a processor
mapdl.finish()

# Run the /VERIFY command for VM14
mapdl.run("/VERIFY,VM14")

# Set the title of the analysis
mapdl.title("VM14 LARGE DEFLECTION ECCENTRIC COMPRESSION OF SLENDER COLUMN")

# Enter the model creation preprocessor
mapdl.prep7(mute=True)

# Define element type and properties
mapdl.et(1, "BEAM188", "", "", 3)  # Element type BEAM188
mapdl.sectype(1, "BEAM", "CHAN")  # Section type BEAM CHAN
mapdl.secdata(2.26, 2.26, 8, 0.39, 0.39, 0.22)  # Section data
mapdl.secoffset("USER", "", 0.6465)  # Section offset

# Define material properties
mapdl.mp("EX", 1, 30e6)  # Young's modulus
mapdl.mp("PRXY", 1, 0.3)  # Poisson's ratio

# Define nodes and element connectivity
mapdl.n(1)  # Node 1
mapdl.n(5, "", 60)  # Node 5 at 60 degrees

# Generate additional nodes
mapdl.fill()

# Define element connectivity
mapdl.e(1, 2)  # Element 1 with nodes 1 and 2

# Generates elements from an existing pattern
mapdl.egen(4, 1, 1)

# Apply load and boundary conditions
mapdl.d(1, "ALL")  # Fix all degrees of freedom for node 1
mapdl.f(5, "FY", -4000)  # Apply a negative force FY to node 5
mapdl.dsym("SYMM", "Z")  # Apply symmetry boundary condition in Z-direction

# select all entities
mapdl.allsel()
# element plot
mapdl.eplot()

# Finish the pre-processing processor
mapdl.finish()

# Enter the solution processor to define solution controls
mapdl.slashsolu()

# Activate large deflections
mapdl.nlgeom("ON")

# Set convergence tolerances
mapdl.cnvtol("F", "", 1e-4)
mapdl.cnvtol("M", "", 1e-4)

# Controls the solution printout
mapdl.outpr("", "LAST")

mapdl.run("/OUT,SCRATCH")  # redirects solver output to a file named "SCRATCH"
mapdl.solve()  # starts a solution
mapdl.finish()  # exists solution processor

mapdl.post1()  # enter post-processing processor
mapdl.run("/OUT")  # redirects output to the default system output file
mapdl.gopr()  # reactivates suppressed printout

# Retrieve nodal deflection and section stresses
mapdl.run("END_NODE = NODE (0,120/2,0)")
# Retrieve nodal deflection and section stresses
mapdl.run("END_NODE = NODE (0,120/2,0)")
deflection = mapdl.get("DEF", "NODE", "END_NODE", "U", "X")  # Nodal deflection
strss_tens = float(
    mapdl.get("STS_TENS", "SECR", 1, "S", "X", "MAX")[:11]
)  # Maximum section tensile stress
strss_comp = float(
    mapdl.get("STS_COMP", "SECR", 1, "S", "X", "MIN")[:11]
)  # Minimum section compressive stress

target_def = 0.1086
target_tens = 1803.63
target_comp = -2394.53

data = [
    [target_def, deflection, target_def / deflection],
    [target_tens, strss_tens, target_tens / strss_tens],
    [target_comp, strss_comp, target_comp / strss_comp],
]
col_headers = ["TARGET", "Mechanical APDL", "RATIO"]
row_headers = ["DEFLECTION (in)", "STRSS_TENS (psi)", "STRSS_COMP (psi)"]

print(pandas.DataFrame(data, row_headers, col_headers))

# Finish the post-processing processor
mapdl.finish()
# mapdl.starlist("vm14", "vrt")

# Exit MAPDL
mapdl.exit()
