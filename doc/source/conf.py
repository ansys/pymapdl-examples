"""Sphinx documentation configuration file."""
from datetime import datetime
import warnings

from ansys_sphinx_theme import ansys_favicon, pyansys_logo_black
import pyvista

# Ensure that offscreen rendering is used for docs generation
pyvista.OFF_SCREEN = True

# Project information
project = "pymapdl-examples"
copyright = f"(c) {datetime.now().year} ANSYS, Inc. All rights reserved"
author = "ANSYS, Inc."
release = version = "0.1.dev0"

# Favicon
html_favicon = ansys_favicon

# Select desired logo, theme, and declare the html title
html_logo = pyansys_logo_black
html_theme = "ansys_sphinx_theme"
html_short_title = html_title = "PyMAPDL Examples"

# specify the location of your github repo
html_theme_options = {
    "github_url": "https://github.com/pyansys/pymapdl-examples",
    "show_prev_next": False,
    "show_breadcrumbs": True,
    "collapse_navigation": True,
    "use_edit_page_button": True,
    "additional_breadcrumbs": [
        ("PyAnsys", "https://docs.pyansys.com/"),
        ("PyMAPDL", "https://mapdl.docs.pyansys.com/"),
        ("Examples", "https://mapdl.docs.pyansys.com/dev/examples/"),
    ],
    "icon_links": [
        {
            "name": "Support",
            "url": "https://github.com/pyansys/pymapdl-examples/discussions",
            "icon": "fa fa-comment fa-fw",
        },
    ],
}

html_context = {
    "display_github": True,  # Integrate GitHub
    "github_user": "pyansys",
    "github_repo": "pymapdl-example",
    "github_version": "main",
    "doc_path": "doc/source",
}

# Sphinx extensions
extensions = [
    "jupyter_sphinx",
    "notfound.extension",
    "numpydoc",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_gallery.gen_gallery",
    "sphinxemoji.sphinxemoji",
]

# -- Sphinx Gallery Options ---------------------------------------------------
sphinx_gallery_conf = {
    # convert rst to md for ipynb
    "pypandoc": True,
    # path to your examples scripts
    "examples_dirs": [],
    # path where to save gallery generated examples
    "gallery_dirs": [""],
    # Pattern to search for example files
    "filename_pattern": r"\.py",
    # Remove the "Download all examples" button from the top level gallery
    "download_all_examples": False,
    # directory where function granular galleries are stored
    "backreferences_dir": None,
    # Modules for which function level galleries are created.  In
    "doc_module": "ansys-mapdl-core",
    "image_scrapers": ("pyvista", "matplotlib"),
    "ignore_pattern": "flycheck*",
    "thumbnail_size": (350, 350),
}

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/dev", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/reference", None),
    "numpy": ("https://numpy.org/devdocs", None),
    "matplotlib": ("https://matplotlib.org/stable", None),
    "pyvista": ("https://docs.pyvista.org/", None),
    # kept here as an example
    # "pandas": ("https://pandas.pydata.org/pandas-docs/stable", None),
    # "grpc": ("https://grpc.github.io/grpc/python/", None),
}

# suppress annoying matplotlib bug
warnings.filterwarnings("ignore", category=UserWarning)

suppress_warnings = ["label.*"]
# supress_warnings = ["ref.option"]

# numpydoc configuration
numpydoc_show_class_members = False
numpydoc_xref_param_type = True

# Image referencing
numfig = True

# Consider enabling numpydoc validation. See:
# https://numpydoc.readthedocs.io/en/latest/validation.html#
numpydoc_validate = True
numpydoc_validation_checks = {
    "GL06",  # Found unknown section
    "GL07",  # Sections are in the wrong order.
    "GL08",  # The object does not have a docstring
    "GL09",  # Deprecation warning should precede extended summary
    "GL10",  # reST directives {directives} must be followed by two colons
    "SS01",  # No summary found
    "SS02",  # Summary does not start with a capital letter
    # "SS03", # Summary does not end with a period
    "SS04",  # Summary contains heading whitespaces
    # "SS05", # Summary must start with infinitive verb, not third person
    "RT02",  # The first line of the Returns section should contain only the
    # type, unless multiple values are being returned"
}


# static path
html_static_path = ["_static"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "links.rst",
]

# make rst_epilog a variable, so you can add other epilog parts to it
rst_epilog = ""
# Read link all targets from file
with open("links.rst") as f:
    rst_epilog += f.read()
