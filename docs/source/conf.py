# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from os.path import dirname

PROJECT_DIR = dirname(os.path.abspath('..'))
sys.path.insert(0, PROJECT_DIR)

print(PROJECT_DIR)

# -- Project information -----------------------------------------------------

project = 'Britecore Assignment'
copyright = '2019, Rajat Mhetre'
author = 'Rajat Mhetre'

# -- General configuration ---------------------------------------------------

source_suffix = '.rst'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc', 'sphinxcontrib.httpdomain',
    'sphinxcontrib.autohttp.flask', 'sphinxcontrib.autohttp.flaskqref',
    'sphinxcontrib.httpexample'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# HTTP Domain
http_strict_mode = True
http_index_localname = "Britecore Assignment API"
http_index_shortname = 'api'
http_index_ignore_prefixes = ['/internal', '/_proxy']
http_headers_ignore_prefixes = ['X-']

# HTTP Example
httpexample_scheme = 'http'
