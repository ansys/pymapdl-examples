PyMAPDL Examples
================

This repository holds examples for PyMAPDL.


Code Style
----------
Code style can be checked by running:

.. code-block:: text

    tox -e style

Previous command will run `pre-commit`_ for checking code quality.


Documentation
-------------
Documentation can be rendered by running:

Windows

.. code-block:: text

    tox -e doc-win

MacOS/Linux (requires make)

.. code-block:: text

    tox -e doc-linux

The resultant HTML files can be inspected using your favorite web browser:

.. code-block:: text

    <browser> .tox/doc_out_html/index.html

*Previous command will open the rendered documentation in the desired browser.*


.. LINKS AND REFERENCES
.. _black: https://github.com/psf/black
.. _flake8: https://flake8.pycqa.org/en/latest/
.. _isort: https://github.com/PyCQA/isort
.. _PyAnsys Developer's guide: https://dev.docs.pyansys.com/
.. _pre-commit: https://pre-commit.com/
.. _pytest: https://docs.pytest.org/en/stable/
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _pip: https://pypi.org/project/pip/
.. _tox: https://tox.wiki/
.. _venv: https://docs.python.org/3/library/venv.html
