RST file for testing purposes


.. jupyter-execute::
   :hide-code:

   from ansys.mapdl.core import launch_mapdl
   
   mapdl = launch_mapdl()
   print(mapdl)

   mapdl.exit()