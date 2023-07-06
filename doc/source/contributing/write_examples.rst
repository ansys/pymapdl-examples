How to write a good example?
============================

Here are some tips for writing a good example.

Use ``mapdl.convert_script``
----------------------------

If you want to translate a MAPDL script into a PyMAPDL one, you can first
run the following commands:: 

    from ansys.mapdl.core import convert_script
    convert_script(path_MAPDL_script)

.. warning::

    The ``mapdl.convert_script`` function is still on beta state, hence it is advised you check its output.
    Please, double-check if there are easier ways to write some commands.

    For example, prefer using ``mapdl.eplot()`` rather than ``mapdl.run("EPLOT")``.


Use Python libraries as much as possible
----------------------------------------
The aim of PyMAPDL is to make possible the creation of workflows combining
MAPDL and the Python environment.
Some MAPDL workflows can be very efficient but mixing it with Python libraries
can simplify the code and make it more visual with new plots.

Do not hesitate to have a look at the `Python Package Index <pypi_org_>`_
to discover new Python libraries.


Graphics and plots
------------------

The more visual your example is, the better.
Python facilitates the creation of colorful figures: take advantage
of that.

Libraries like `matplotlib <matplotlib_org_>`_, `pandas <pandas_org_>`_
or `pyvista <pandas_org_>`_ can help you create nice graphics, tables, or plots .
