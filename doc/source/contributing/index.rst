Contribute
==========

Overall guidance on contributing to a PyAnsys library appears in the
`Contributing <dev_guide_contributing_>`_ topic
in the *PyAnsys Developer's Guide*. Ensure that you are thoroughly familiar
with this guide before attempting to contribute to PyMAPDL Examples.

The following contribution information is specific to PyMAPDL Examples.

Clone the repository
--------------------

Run this code to clone and install the latest version of PyMAPDL Examples in development mode::

    git clone https://github.com/ansys/pymapdl-examples
    cd pymapdl-examples

Post issues
-----------

Use the `PyMAPDL Examples Issues <pymapdl_examples_issues_>`_ page to submit questions,
report bugs, and request new features. When possible, use these issue
templates:

* Bug report template
* Feature request template

If your issue does not fit into one of these categories, create your own issue.

To reach the project support team, email `pyansys.core@ansys.com <pyansys.core@ansys.com>`_.


Python virtual environment
--------------------------

The use of Python virtual environment is recommended. To create one, run the following commands::

    python -m venv .venv
     .\.venv\Scripts\activate


To deactivate it, run::
    
    deactivate


Build documentation
-------------------

To build the PyMAPDL Examples documentation locally, in the root directory of the repository, run::
    
    pip install -r .\requirements\requirements_doc.txt
    .\doc\make.bat html

Documentation for the latest stable release of PyMAPDL Examples is hosted at
`PyMAPDL Examples Documentation <pymapdl_examples_docs_>`_.

Adhere to code style
--------------------

PyMAPDL Examples follows the PEP8 standard as outlined in the `PyAnsys Development Guide
<dev_guide_pyansys_>`_ and implements style checking using
`pre-commit <precommit_>`_.

To ensure your code meets minimum code styling standards, first, you need to install
the ``pre-commit`` library::

  pip install pre-commit

Once done, code styling standards can be checked with the following code::

  pre-commit run --all-files

You can also install this as a pre-commit hook by running this code::

  pre-commit install

This way, it is not possible for you to push code that fails the style checks::

  $ pre-commit install
  $ git commit -am "added my cool feature"
  black....................................................................Passed
  blacken-docs.............................................................Passed
  isort....................................................................Passed
  flake8...................................................................Passed
  codespell................................................................Passed
  check for merge conflicts................................................Passed
  debug statements (python)................................................Passed
  Validate GitHub Workflows................................................Passed


.. toctree::
    :hidden:
    :includehidden:

    write_examples.rst