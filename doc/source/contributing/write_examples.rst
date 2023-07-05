How to write a good example?
============================

Here are some tips for writing a good example:

Use ``mapdl.convert_script``
----------------------------
If you want to translate a MAPDL script into a PyMAPDL one, you can first
run the following commands:: 

    from ansys.mapdl.core import convert_script

    convert_script(path_MAPDL_script)

.. warning::

    The `convert_script` fonction is still under development.
    Please, double-check there are no easier way to write the command.

    For example, prefer using ``mapdl.eplot()`` rather than ``mapdl.run("EPLOT")``.


Use Python libraries as much as possible
----------------------------------------
The aim of PyMAPDL is to make it possible to create workflows combining
MAPDL and the Python environment.
Some MAPDL workflows can be very efficient but mixing it with Python libraries
can simplifly the code and make it more visual with new plotings.

Don't hesitate to have a look at the `Python Package Index <pypi_org_>`_
to discover new Python libraries.


Graphics and plotings
---------------------

The more visual your example, the better!
Python facilitates the creation of colorful figures: take advatange
of that!

Libraries like `matplotlib <matplotlib_org_>`_, `pandas <pandas_org_>`_
or `pyvista <pandas_org_>`_ can help you to make nice graphics, tables, or plottings .
